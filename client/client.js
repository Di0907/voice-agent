// client.js
const API = "http://127.0.0.1:8000";

const hold   = document.getElementById("hold");
const logBox = document.getElementById("log");
const player = document.getElementById("player");

let recorder = null;
let chunks   = [];
let sessionId = null;

function append(msg) {
  if (!logBox) return;
  logBox.value += msg + "\n";
  logBox.scrollTop = logBox.scrollHeight;
}

// ---- 1) Check microphone permission when page loads ----
(async () => {
  try {
    const test = await navigator.mediaDevices.getUserMedia({ audio: true });
    test.getTracks().forEach(t => t.stop());
    append("[Mic] Permission granted");
  } catch (e) {
    append("[Mic] " + e.name + " - " + e.message + " (please allow microphone access)");
  }
})();

// Choose a supported audio MIME type
function pickMimeType() {
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/ogg;codecs=opus",
    "audio/ogg"
  ];
  for (const t of candidates) {
    try {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported?.(t)) return t;
    } catch {}
  }
  return "";
}

hold.onmousedown = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mime = pickMimeType();
    const options = mime ? { mimeType: mime } : {};
    if (!mime) append("[Warn] Using default MIME type");

    recorder = new MediaRecorder(stream, options);
    chunks = [];

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunks.push(e.data);
    };

    recorder.onstop = async () => {
      try {
        const blob = new Blob(chunks, { type: mime || "audio/webm" });
        chunks = [];

        // --- Send to ASR ---
        const fd = new FormData();
        fd.append("file", blob, `sample.${(mime.includes("ogg") ? "ogg" : "webm")}`);
        append("[Info] Uploading audio (" + blob.type + ", " + blob.size + " bytes)");

        const asrResp = await fetch(`${API}/asr`, { method: "POST", body: fd });
        if (!asrResp.ok) throw new Error("ASR HTTP " + asrResp.status);
        const asr = await asrResp.json();
        append("User: " + (asr.text || "<empty>"));

        // --- Call Chat API ---
        const chatResp = await fetch(`${API}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, text: asr.text || "" })
        });
        if (!chatResp.ok) throw new Error("Chat HTTP " + chatResp.status);
        const chat = await chatResp.json();
        sessionId = chat.session_id;
        append("Assistant: " + (chat.text || chat.reply || "<empty>"));

        // --- Call TTS API ---
        const ttsResp = await fetch(`${API}/tts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: chat.text || chat.reply || "" })
        });
        if (!ttsResp.ok) {
          const errText = await ttsResp.text().catch(() => "");
          append("[Error] TTS failed: HTTP " + ttsResp.status + " " + errText);
          return;
        }

        const audioBlob = await ttsResp.blob();
        if (!audioBlob || audioBlob.size === 0) {
          append("[Warn] Empty audio from TTS");
          return;
        }

        const url = URL.createObjectURL(audioBlob);
        player.src = url;

        try {
          await player.play();
        } catch (e) {
          append("[Hint] Autoplay blocked, click ▶ to play");
        }
      } catch (err) {
        append("[Error] " + err.message);
        console.error(err);
      } finally {
        recorder?.stream?.getTracks?.().forEach(t => t.stop());
      }
    };

    recorder.start();
    append("[Recording started]");
  } catch (e) {
    append("[MicError] " + e.name + " - " + e.message + " (check browser/system settings)");
  }
};

hold.onmouseup = () => {
  if (recorder && recorder.state !== "inactive") {
    recorder.stop();
    append("[Recording stopped]");
  }
};
