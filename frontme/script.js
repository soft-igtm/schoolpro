/**
 * script.js
 * ---------
 * SchoolBot frontend logic:
 *   1. Chat interface (send / receive messages)
 *   2. Web Speech API — Speech Recognition (voice-to-text)
 *   3. Web Speech API — Speech Synthesis (text-to-speech bot replies)
 *   4. UI helpers: typing indicator, auto-scroll, sidebar toggle
 *
 * Backend endpoint: POST http://127.0.0.1:5000/chat
 */

"use strict";

/* ═══════════════════════════════════════════════════════════════
   CONFIG
═══════════════════════════════════════════════════════════════ */
const API_URL         = "http://127.0.0.1:5000/chat";
const TYPING_DELAY_MS = 900;   // Simulated "thinking" delay
const MAX_CHARS       = 500;

/* ═══════════════════════════════════════════════════════════════
   DOM REFERENCES
═══════════════════════════════════════════════════════════════ */
const chatWindow       = document.getElementById("chatWindow");
const userInput        = document.getElementById("userInput");
const sendBtn          = document.getElementById("sendBtn");
const voiceBtn         = document.getElementById("voiceBtn");
const voiceBanner      = document.getElementById("voiceBanner");
const voiceBannerText  = document.getElementById("voiceBannerText");
const voiceCancel      = document.getElementById("voiceCancel");
const typingIndicator  = document.getElementById("typingIndicator");
const charCount        = document.getElementById("charCount");
const clearBtn         = document.getElementById("clearBtn");
const menuToggle       = document.getElementById("menuToggle");
const sidebar          = document.querySelector(".sidebar");
const sidebarOverlay   = document.getElementById("sidebarOverlay");
const noVoiceNotice    = document.getElementById("noVoiceNotice");

/* ═══════════════════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════════════════ */
let isListening     = false;
let isBotTyping     = false;
let recognition     = null;
let speechSynthesis = window.speechSynthesis || null;
let voiceEnabled    = true;   // TTS toggle (always on by default)

/* ═══════════════════════════════════════════════════════════════
   UTILITIES
═══════════════════════════════════════════════════════════════ */

/** Format current time as HH:MM */
function now() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

/** Scroll chat window to the very bottom */
function scrollToBottom() {
  chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: "smooth" });
}

/** Auto-grow textarea up to CSS max-height */
function autoGrowInput() {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 130) + "px";
}

/** Update the char counter badge */
function updateCharCount() {
  const remaining = MAX_CHARS - userInput.value.length;
  charCount.textContent = remaining;
  charCount.className   = "char-count";
  if (remaining <= 100) charCount.classList.add("warn");
  if (remaining <= 20)  charCount.classList.add("limit");
}

/* ═══════════════════════════════════════════════════════════════
   MESSAGE RENDERING
═══════════════════════════════════════════════════════════════ */

/**
 * Render a user message bubble into the chat window.
 * @param {string} text - Raw user text
 */
function renderUserMessage(text) {
  const row = document.createElement("div");
  row.classList.add("msg-row", "user-row");

  const avatar = document.createElement("div");
  avatar.classList.add("avatar", "user-avatar");
  avatar.textContent = "U";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble", "user-bubble");
  bubble.textContent = text;

  const timeEl = document.createElement("p");
  timeEl.classList.add("msg-time");
  timeEl.textContent = now();

  const wrapper = document.createElement("div");
  wrapper.appendChild(bubble);
  wrapper.appendChild(timeEl);

  row.appendChild(wrapper);
  row.appendChild(avatar);

  chatWindow.appendChild(row);
  scrollToBottom();
}

/**
 * Render a bot message bubble into the chat window.
 * @param {string} text       - Bot reply text (may contain \n)
 * @param {string} intentName - Matched intent name
 */
function renderBotMessage(text, intentName = "") {
  const row = document.createElement("div");
  row.classList.add("msg-row", "bot-row");

  // Avatar
  const avatar = document.createElement("div");
  avatar.classList.add("avatar", "bot-avatar");
  avatar.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/>
      <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="9" cy="10" r="1.2" fill="currentColor"/>
      <circle cx="15" cy="10" r="1.2" fill="currentColor"/>
    </svg>`;

  // Bubble — convert \n to <br>
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", "bot-bubble");

  const lines = text.split("\n");
  lines.forEach((line, idx) => {
    if (line.trim() === "") {
      if (idx !== 0 && idx !== lines.length - 1) bubble.appendChild(document.createElement("br"));
      return;
    }
    const p = document.createElement("p");
    p.textContent = line;
    bubble.appendChild(p);
  });

  // Optional intent badge
  if (intentName && intentName !== "unknown") {
    const badge = document.createElement("span");
    badge.classList.add("intent-badge");
    badge.textContent = `# ${intentName.replace(/_/g, " ")}`;
    bubble.appendChild(badge);
  }

  const timeEl = document.createElement("p");
  timeEl.classList.add("msg-time");
  timeEl.textContent = now();

  const wrapper = document.createElement("div");
  wrapper.appendChild(bubble);
  wrapper.appendChild(timeEl);

  row.appendChild(avatar);
  row.appendChild(wrapper);

  chatWindow.appendChild(row);
  scrollToBottom();
}

/* ═══════════════════════════════════════════════════════════════
   TYPING INDICATOR
═══════════════════════════════════════════════════════════════ */

function showTyping() {
  typingIndicator.classList.add("visible");
  scrollToBottom();
}

function hideTyping() {
  typingIndicator.classList.remove("visible");
}

/* ═══════════════════════════════════════════════════════════════
   CHAT LOGIC — API CALL
═══════════════════════════════════════════════════════════════ */

/**
 * Send a user message to the Flask backend and render the response.
 * @param {string} message
 */
async function sendMessage(message) {
  message = message.trim();
  if (!message || isBotTyping) return;

  // Render user bubble
  renderUserMessage(message);
  clearInput();

  // Disable send while waiting
  isBotTyping = true;
  sendBtn.disabled = true;

  // Show typing indicator after brief pause
  await sleep(200);
  showTyping();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    // Simulate realistic typing time
    const delay = Math.max(TYPING_DELAY_MS, data.response.length * 10);
    await sleep(Math.min(delay, 2200));

    hideTyping();
    renderBotMessage(data.response, data.intent);

    // Speak the response (TTS)
    if (voiceEnabled) {
      speakText(data.response);
    }

  } catch (error) {
    hideTyping();
    const errMsg = "⚠️ Could not connect to the server. Make sure the Flask backend is running on port 5000.";
    renderBotMessage(errMsg, "error");
    console.error("SchoolBot API error:", error);
  }

  isBotTyping = false;
  sendBtn.disabled = false;
  userInput.focus();
}

/** Sleep helper */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/** Clear the input field */
function clearInput() {
  userInput.value = "";
  userInput.style.height = "auto";
  updateCharCount();
}

/* ═══════════════════════════════════════════════════════════════
   TEXT-TO-SPEECH (TTS)
═══════════════════════════════════════════════════════════════ */

/**
 * Speak the bot's response using Web Speech Synthesis API.
 * Strips emoji/special chars for cleaner speech.
 * @param {string} text
 */
function speakText(text) {
  if (!speechSynthesis) return;

  // Cancel any ongoing speech
  speechSynthesis.cancel();

  // Clean text for speech: remove emojis and bullet symbols
  const cleanText = text
    .replace(/[\u{1F300}-\u{1FFFF}]/gu, "")  // emoji ranges
    .replace(/[•·▪▸◦►]/g, "")
    .replace(/\n{2,}/g, ". ")
    .replace(/\n/g, ". ")
    .trim();

  if (!cleanText) return;

  const utterance      = new SpeechSynthesisUtterance(cleanText);
  utterance.rate       = 1.0;
  utterance.pitch      = 1.0;
  utterance.volume     = 0.9;
  utterance.lang       = "en-US";

  // Prefer a clear English voice
  const voices = speechSynthesis.getVoices();
  const preferred = voices.find(
    v => v.lang.startsWith("en") && (v.name.includes("Google") || v.name.includes("Microsoft"))
  ) || voices.find(v => v.lang.startsWith("en"));

  if (preferred) utterance.voice = preferred;

  speechSynthesis.speak(utterance);
}

/* ═══════════════════════════════════════════════════════════════
   SPEECH RECOGNITION (STT)
═══════════════════════════════════════════════════════════════ */

// Check browser support
const SpeechRecognitionAPI =
  window.SpeechRecognition || window.webkitSpeechRecognition || null;

if (!SpeechRecognitionAPI) {
  // Gracefully disable voice input
  voiceBtn.disabled = true;
  voiceBtn.title    = "Voice not supported in this browser";
  voiceBtn.style.opacity = ".35";
  noVoiceNotice.style.display = "block";
} else {
  // Set up recognition instance
  recognition = new SpeechRecognitionAPI();
  recognition.continuous      = false;
  recognition.interimResults  = true;
  recognition.lang            = "en-US";
  recognition.maxAlternatives = 1;

  /* -- Events -- */

  recognition.onstart = () => {
    isListening = true;
    voiceBtn.classList.add("listening");
    // Swap mic icon for stop icon
    voiceBtn.querySelector(".icon-mic").style.display  = "none";
    voiceBtn.querySelector(".icon-stop").style.display = "block";
    voiceBanner.classList.add("active");
    voiceBannerText.textContent = "Listening… speak your question";
    // Stop TTS while user speaks
    if (speechSynthesis) speechSynthesis.cancel();
  };

  recognition.onresult = (event) => {
    let interim = "";
    let final   = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        final += transcript;
      } else {
        interim += transcript;
      }
    }

    // Show live interim result in the input field
    if (interim) {
      userInput.value = interim;
      autoGrowInput();
      updateCharCount();
      voiceBannerText.textContent = `"${interim}"`;
    }

    if (final) {
      userInput.value = final;
      autoGrowInput();
      updateCharCount();
      voiceBannerText.textContent = `✅ Got it: "${final}"`;
    }
  };

  recognition.onend = () => {
    isListening = false;
    voiceBtn.classList.remove("listening");
    voiceBtn.querySelector(".icon-mic").style.display  = "block";
    voiceBtn.querySelector(".icon-stop").style.display = "none";

    // Auto-send if we captured something
    const captured = userInput.value.trim();
    if (captured) {
      setTimeout(() => {
        voiceBanner.classList.remove("active");
        sendMessage(captured);
      }, 600);
    } else {
      voiceBanner.classList.remove("active");
    }
  };

  recognition.onerror = (event) => {
    isListening = false;
    voiceBtn.classList.remove("listening");
    voiceBtn.querySelector(".icon-mic").style.display  = "block";
    voiceBtn.querySelector(".icon-stop").style.display = "none";
    voiceBanner.classList.remove("active");

    let msg = "⚠️ Voice error.";
    if (event.error === "no-speech")          msg = "No speech detected. Try again.";
    if (event.error === "audio-capture")      msg = "Microphone not accessible. Check your browser permissions.";
    if (event.error === "not-allowed")        msg = "Microphone permission denied. Please allow mic access in browser settings.";
    if (event.error === "network")            msg = "Network error during voice recognition.";

    renderBotMessage(msg, "");
    console.warn("SpeechRecognition error:", event.error);
  };
}

/* ── Voice button click ──────────────────────────────────────── */
voiceBtn.addEventListener("click", () => {
  if (!recognition) return;

  if (isListening) {
    recognition.stop();
  } else {
    userInput.value = "";
    updateCharCount();
    try {
      recognition.start();
    } catch (e) {
      // Already started in some browsers
      console.warn("Recognition start error:", e);
    }
  }
});

/* ── Cancel voice ────────────────────────────────────────────── */
voiceCancel.addEventListener("click", () => {
  if (recognition && isListening) {
    recognition.abort();  // abort without sending
  }
  isListening = false;
  voiceBtn.classList.remove("listening");
  voiceBtn.querySelector(".icon-mic").style.display  = "block";
  voiceBtn.querySelector(".icon-stop").style.display = "none";
  voiceBanner.classList.remove("active");
  userInput.value = "";
  updateCharCount();
});

/* ═══════════════════════════════════════════════════════════════
   INPUT BAR EVENTS
═══════════════════════════════════════════════════════════════ */

sendBtn.addEventListener("click", () => {
  sendMessage(userInput.value);
});

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage(userInput.value);
  }
});

userInput.addEventListener("input", () => {
  autoGrowInput();
  updateCharCount();
});

/* ═══════════════════════════════════════════════════════════════
   QUICK TOPIC BUTTONS (sidebar)
═══════════════════════════════════════════════════════════════ */

document.querySelectorAll(".topic-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const msg = btn.getAttribute("data-msg");
    if (msg) {
      // Close sidebar on mobile
      sidebar.classList.remove("open");
      sidebarOverlay.classList.remove("active");
      sendMessage(msg);
    }
  });
});

/* ═══════════════════════════════════════════════════════════════
   CLEAR CHAT
═══════════════════════════════════════════════════════════════ */

clearBtn.addEventListener("click", () => {
  // Keep only the welcome message
  const welcome = document.getElementById("welcomeMsg");
  chatWindow.innerHTML = "";
  if (welcome) chatWindow.appendChild(welcome);

  // Stop speech
  if (speechSynthesis) speechSynthesis.cancel();
});

/* ═══════════════════════════════════════════════════════════════
   MOBILE SIDEBAR TOGGLE
═══════════════════════════════════════════════════════════════ */

menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  sidebarOverlay.classList.toggle("active");
});

sidebarOverlay.addEventListener("click", () => {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.remove("active");
});

/* ═══════════════════════════════════════════════════════════════
   VOICES INIT — preload TTS voice list (Chrome loads async)
═══════════════════════════════════════════════════════════════ */

if (speechSynthesis) {
  speechSynthesis.getVoices(); // trigger initial load
  speechSynthesis.addEventListener("voiceschanged", () => {
    speechSynthesis.getVoices(); // cache after async load
  });
}

/* ═══════════════════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════════════════ */

// Focus the input on page load
window.addEventListener("DOMContentLoaded", () => {
  userInput.focus();
  updateCharCount();
});


