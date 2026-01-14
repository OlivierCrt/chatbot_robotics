import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { VRMLoaderPlugin, VRMUtils } from "@pixiv/three-vrm";


console.log("=== APP START (VRM + life) ===");

// --------------------
// Page setup
// --------------------
document.body.style.margin = "0";
document.body.style.background = "#b3aeaeff";

// Debug badge
const badge = document.createElement("div");
badge.style.position = "fixed";
badge.style.left = "12px";
badge.style.top = "12px";
badge.style.zIndex = "9999";
badge.style.padding = "8px 10px";
badge.style.borderRadius = "10px";
badge.style.fontFamily = "system-ui, sans-serif";
badge.style.fontSize = "14px";
badge.style.background = "rgba(0,0,0,0.65)";
badge.style.color = "white";
badge.textContent = "Init…";
document.body.appendChild(badge);






const bubble = document.createElement("div");
bubble.style.position = "fixed";
bubble.style.right = "24px";
bubble.style.bottom = "120px";
bubble.style.maxWidth = "320px";
bubble.style.padding = "14px 16px";
bubble.style.borderRadius = "18px";
bubble.style.background = "rgba(0,0,0,0.7)";
bubble.style.color = "white";
bubble.style.fontFamily = "system-ui, sans-serif";
bubble.style.fontSize = "15px";
bubble.style.lineHeight = "1.4";
bubble.style.boxShadow = "0 10px 25px rgba(0,0,0,0.25)";
bubble.style.opacity = "0";
bubble.style.transform = "translateY(10px)";
bubble.style.transition = "all 0.3s ease";
bubble.style.pointerEvents = "none";
bubble.textContent = "";
document.body.appendChild(bubble);

function showBubble(text) {
  bubble.textContent = text;
  bubble.style.opacity = "1";
  bubble.style.transform = "translateY(0)";
}

function hideBubble() {
  bubble.style.opacity = "0";
  bubble.style.transform = "translateY(10px)";
}









// Caméra au lancement (réglages)
const START_CAM_POS = new THREE.Vector3(0.0, 0.7, 1.0);  // x,y,z
const START_TARGET  = new THREE.Vector3(0.0, 0.60, 0.00);  // où regarde la caméra





// --------------------
// UI: input + mic + stored variable
// --------------------
let userText = ""; // ✅ ta variable "source de vérité"

const ui = document.createElement("div");
ui.style.position = "fixed";
ui.style.left = "12px";
ui.style.bottom = "12px";
ui.style.zIndex = "9999";
ui.style.display = "flex";
ui.style.gap = "8px";
ui.style.alignItems = "center";
ui.style.padding = "10px";
ui.style.borderRadius = "14px";
ui.style.background = "rgba(0,0,0,0.65)";
ui.style.backdropFilter = "blur(6px)";
ui.style.color = "white";
ui.style.fontFamily = "system-ui, sans-serif";
ui.style.maxWidth = "min(900px, calc(100vw - 24px))";
document.body.appendChild(ui);




// --------------------
// Chat UI (bulles) au-dessus de la barre
// --------------------
const chat = document.createElement("div");
chat.style.position = "fixed";
chat.style.left = "12px";
chat.style.bottom = "72px"; // juste au-dessus de ta barre
chat.style.zIndex = "9999";
chat.style.width = "min(520px, calc(100vw - 24px))";
chat.style.maxHeight = "45vh";
chat.style.overflowY = "auto";
chat.style.display = "flex";
chat.style.flexDirection = "column";
chat.style.gap = "10px";
chat.style.padding = "12px";
chat.style.borderRadius = "14px";
chat.style.background = "rgba(0,0,0,0.35)";
chat.style.backdropFilter = "blur(6px)";
chat.style.border = "1px solid rgba(255,255,255,0.12)";
chat.style.fontFamily = "system-ui, sans-serif";
document.body.appendChild(chat);

function addBubble(text, who = "bot") {
  const row = document.createElement("div");
  row.style.display = "flex";
  row.style.justifyContent = (who === "user") ? "flex-end" : "flex-start";

  const b = document.createElement("div");
  b.textContent = text;
  b.style.maxWidth = "85%";
  b.style.whiteSpace = "pre-wrap";
  b.style.padding = "10px 12px";
  b.style.borderRadius = "16px";
  b.style.fontSize = "14px";
  b.style.lineHeight = "1.35";
  b.style.boxShadow = "0 8px 18px rgba(0,0,0,0.18)";
  b.style.border = "1px solid rgba(255,255,255,0.12)";

  if (who === "user") {
    b.style.background = "rgba(70,130,255,0.35)";
    b.style.color = "white";
    b.style.borderTopRightRadius = "6px";
  } else {
    b.style.background = "rgba(0,0,0,0.65)";
    b.style.color = "white";
    b.style.borderTopLeftRadius = "6px";
  }

  row.appendChild(b);
  chat.appendChild(row);

  // auto-scroll
  chat.scrollTop = chat.scrollHeight;
}








const input = document.createElement("input");
input.type = "text";
input.placeholder = "Tape ton message…";
input.style.flex = "1";
input.style.minWidth = "240px";
input.style.padding = "10px 12px";
input.style.borderRadius = "12px";
input.style.border = "1px solid rgba(255,255,255,0.15)";
input.style.outline = "none";
input.style.background = "rgba(255,255,255,0.08)";
input.style.color = "white";
ui.appendChild(input);

const btnSend = document.createElement("button");
btnSend.textContent = "Envoyer";
btnSend.style.padding = "10px 12px";
btnSend.style.borderRadius = "12px";
btnSend.style.border = "0";
btnSend.style.cursor = "pointer";
ui.appendChild(btnSend);

const btnMic = document.createElement("button");
btnMic.textContent = "🎤";
btnMic.title = "Dicter";
btnMic.style.padding = "10px 12px";
btnMic.style.borderRadius = "12px";
btnMic.style.border = "0";
btnMic.style.cursor = "pointer";
ui.appendChild(btnMic);

const status = document.createElement("span");
status.textContent = "";
status.style.fontSize = "12px";
status.style.opacity = "0.85";
ui.appendChild(status);

// helper: update variable + keep input in sync
function setUserText(v) {
  userText = (v ?? "").toString();
  input.value = userText;
  console.log("userText =", userText);
}

// send handlers
async function submit() {
  const userMsg = input.value.trim();
  if (!userMsg) return;

  addBubble(userMsg, "user"); // ✅ bulle user

  setUserText(userMsg);
  input.value = "";

  try {
    badge.textContent = "🤖 Rasa…";
    const rasaReply = await sendToRasa(userMsg);

    if (!rasaReply) {
      badge.textContent = "⚠️ Rasa a répondu vide";
      return;
    }

    addBubble(rasaReply, "bot"); // ✅ bulle bot
    console.log("Rasa reply:", rasaReply);

    await speakXTTS(rasaReply);
  } catch (e) {
    console.error(e);
    badge.textContent = "❌ Erreur (voir console)";
    addBubble("❌ Erreur: " + (e?.message ?? "inconnue"), "bot");
  }
}




btnSend.onclick = submit;
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") submit();
});

// --------------------
// Speech-to-text (Web Speech API)
// --------------------
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let isListening = false;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = "fr-FR";
  recognition.interimResults = true;
  recognition.continuous = false; // une phrase puis stop

  recognition.onstart = () => {
    isListening = true;
    status.textContent = "Écoute…";
    btnMic.textContent = "⏹️";
  };

  recognition.onend = () => {
    isListening = false;
    status.textContent = "";
    btnMic.textContent = "🎤";
  };

  recognition.onerror = (e) => {
    console.warn("SpeechRecognition error:", e);
    status.textContent = "Erreur micro";
  };

  recognition.onresult = (event) => {
    // concatène les résultats
    let finalText = "";
    let interimText = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const res = event.results[i];
      const txt = res[0].transcript;
      if (res.isFinal) finalText += txt;
      else interimText += txt;
    }

    // on affiche ce qui arrive en direct dans l’input
    if (interimText) {
      input.value = (userText ? userText + " " : "") + interimText;
      status.textContent = "…";
    }
    if (finalText) {
      // commit en variable
      const merged = (userText ? userText + " " : "") + finalText;
      setUserText(merged.trim());
      status.textContent = "OK";
      // option : auto-submit après dictée
      // submit();
    }
  };

  btnMic.onclick = () => {
    try {
      if (!recognition) return;
      if (isListening) recognition.stop();
      else recognition.start();
    } catch (err) {
      console.warn(err);
    }
  };
} else {
  // Pas supporté sur ce navigateur
  btnMic.disabled = true;
  btnMic.style.opacity = "0.5";
  btnMic.title = "Speech-to-text non supporté ici";
  status.textContent = "STT indisponible";
}













// Simple UI buttons
const btnSpeak = document.createElement("button");
btnSpeak.textContent = "Parler (test)";
btnSpeak.style.position = "fixed";
btnSpeak.style.left = "12px";
btnSpeak.style.top = "54px";
btnSpeak.style.zIndex = "9999";
btnSpeak.style.padding = "10px 12px";
btnSpeak.style.borderRadius = "10px";
btnSpeak.style.border = "0";
btnSpeak.style.cursor = "pointer";
document.body.appendChild(btnSpeak);

// --------------------
// Renderer / Scene / Camera
// --------------------
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xe6e6e6);

const camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 0.001, 10000);
camera.position.set(0, 1.4, 1.2);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 1.4, 0);
controls.update();

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.9));
const dir = new THREE.DirectionalLight(0xffffff, 1.2);
dir.position.set(2, 3, 2);
scene.add(dir);

// Helper
const axes = new THREE.AxesHelper(0.5);
axes.position.set(0, 1.0, 0);
scene.add(axes);

// --------------------
// VRM state
// --------------------
let vrm = null;

// --------------------
// Helpers: expressions (blink/mouth)
// --------------------
function setExpr(key, v) {
  const exp = vrm?.expressionManager;
  if (!exp) return false;
  try {
    exp.setValue(key, v);
    return true;
  } catch {
    return false;
  }
}

function setMouthOpen(v) {
  // VRM 0.x: souvent aa/ih/ou/ee/oh
  const ok =
    setExpr("aa", v) ||
    setExpr("a", v);

  // Ajoute un petit mix (si dispo)
  setExpr("ih", 0.15 * v);
  setExpr("ou", 0.20 * v);
  setExpr("ee", 0.10 * v);
  setExpr("oh", 0.20 * v);

  // fallback clés simples parfois présentes
  setExpr("i", 0.15 * v);
  setExpr("u", 0.20 * v);
  setExpr("e", 0.10 * v);
  setExpr("o", 0.20 * v);

  return ok;
}

function resetMouth() {
  setMouthOpen(0);
}




// --------------------
// Rasa -> texte, puis XTTS -> audio
// --------------------
async function sendToRasa(userMessage) {
  const res = await fetch("http://localhost:5005/webhooks/rest/webhook", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender: "samuel", message: userMessage }),
  });

  if (!res.ok) throw new Error(`Rasa HTTP ${res.status}`);
  const msgs = await res.json(); // [{text:"..."}, ...]
  const replyText = msgs.map((m) => m.text).filter(Boolean).join("\n").trim();
  return replyText;
}

let currentAudio = null;
let mouthTimer = null;

function startMouthWhilePlaying() {
  if (mouthTimer) clearInterval(mouthTimer);
  let t = 0;
  mouthTimer = setInterval(() => {
    t++;
    const open = 0.10 + 0.70 * (Math.sin(t * 0.55) * 0.5 + 0.5);
    setMouthOpen(open);
  }, 50);
}

function stopMouth() {
  if (mouthTimer) clearInterval(mouthTimer);
  mouthTimer = null;
  resetMouth();
}

async function speakXTTS(text) {
  if (!text || !text.trim()) return;
  if (!vrm) return;

  // stop audio en cours
  if (currentAudio) {
    try { currentAudio.pause(); } catch {}
    currentAudio = null;
  }
  stopMouth();

  badge.textContent = "🎤 XTTS…";

  // ⚠️ adapte l'URL si ton serveur XTTS est ailleurs
  const url = `http://127.0.0.1:8000/tts?text=${encodeURIComponent(text)}&lang=fr`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`XTTS HTTP ${res.status}`);

  const blob = await res.blob();
  const audioUrl = URL.createObjectURL(blob);

  const audio = new Audio(audioUrl);
  currentAudio = audio;

  audio.onplay = () => {
    badge.textContent = "🔊 Parle…";
    startMouthWhilePlaying();
  };
  audio.onended = () => {
    badge.textContent = "✅ OK";
    stopMouth();
    URL.revokeObjectURL(audioUrl);
    currentAudio = null;
  };
  audio.onerror = () => {
    badge.textContent = "❌ Audio error";
    stopMouth();
    URL.revokeObjectURL(audioUrl);
    currentAudio = null;
  };

  await audio.play();
}






let blinkTimeout = null;
function startBlinkLoop() {
  if (!vrm?.expressionManager) return;

  const exp = vrm.expressionManager;

  function blinkOnce() {
    let t = 0;
    const duration = 140; // ms
    const step = 16;

    const id = setInterval(() => {
      t += step;
      const x = t / duration; // 0..1
      const v = x < 0.5 ? x * 2 : (1 - x) * 2;

      // Selon modèle, une ou plusieurs de ces clés existent
      exp.setValue("blink", v);
      exp.setValue("blinkLeft", v);
      exp.setValue("blinkRight", v);

      if (t >= duration) {
        clearInterval(id);
        exp.setValue("blink", 0);
        exp.setValue("blinkLeft", 0);
        exp.setValue("blinkRight", 0);
      }
    }, step);

    blinkTimeout = setTimeout(blinkOnce, 2500 + Math.random() * 3500);
  }

  blinkOnce();
}

// --------------------
// Helper: anti T-pose (petite pose bras)
// --------------------
function applyArmsDownPose() {
  const hum = vrm?.humanoid;
  if (!hum) return;

  // Essaie plusieurs APIs selon version three-vrm
  const getBone =
    hum.getNormalizedBoneNode?.bind(hum) ||
    hum.getRawBoneNode?.bind(hum) ||
    hum.getBoneNode?.bind(hum);

  if (!getBone) {
    console.warn("No humanoid bone getter found on vrm.humanoid");
    return;
  }

  const L_UA = getBone("leftUpperArm");
  const R_UA = getBone("rightUpperArm");
  const L_LA = getBone("leftLowerArm");
  const R_LA = getBone("rightLowerArm");

  if (!L_UA || !R_UA) {
    console.warn("UpperArm bones not found, cannot apply pose.");
    return;
  }

  // reset (évite d’accumuler si reload)
  [L_UA, R_UA, L_LA, R_LA].forEach((b) => b && b.rotation.set(0, 0, 0));

  // Bras le long du corps (valeurs à ajuster un peu selon avatar)
  L_UA.rotation.z = 1.10;
  R_UA.rotation.z = -1.10;

  if (L_LA) L_LA.rotation.z = 0.15;
  if (R_LA) R_LA.rotation.z = -0.15;

  L_UA.rotation.x = 0.10;
  R_UA.rotation.x = 0.10;

  console.log("Arms-down pose applied ✅");
}


// --------------------
// Free TTS + mouth animation
// --------------------
function speak(text) {
  if (!vrm) return;

  window.speechSynthesis.cancel();

  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1.0;
  utter.pitch = 1.0;

  let t = 0;
  const mouthId = setInterval(() => {
    t++;
    // lipsync fake mais crédible
    const open = 0.15 + 0.65 * (Math.sin(t * 0.55) * 0.5 + 0.5);
    setMouthOpen(open);
  }, 50);

  utter.onend = () => {
    clearInterval(mouthId);
    resetMouth();
  };
  utter.onerror = () => {
    clearInterval(mouthId);
    resetMouth();
  };

  window.speechSynthesis.speak(utter);
}

btnSpeak.onclick = () => speakXTTS("Bonjour, Je suis ton assistant, Comment puis je t'aider?");

// --------------------
// Load VRM
// --------------------
badge.textContent = "Loading /avatar.vrm …";

const loader = new GLTFLoader();
loader.register((parser) => new VRMLoaderPlugin(parser));

loader.load(
  "/avatar.vrm",
  (gltf) => {
    vrm = gltf.userData.vrm;

    if (!vrm) {
      console.error("❌ VRM not found in gltf.userData.vrm");
      badge.textContent = "❌ VRM not found (see console)";
      return;
    }

    // VRM0 orientation fix (if available)
    try {
      if (VRMUtils?.rotateVRM0) VRMUtils.rotateVRM0(vrm);
    } catch {}

    scene.add(vrm.scene);

    // Avoid culling issues
    vrm.scene.traverse((o) => (o.frustumCulled = false));

    
    const box = new THREE.Box3().setFromObject(vrm.scene);
    const center = box.getCenter(new THREE.Vector3());
    vrm.scene.position.sub(center);

    // ✅ Pose caméra fixe au lancement
    camera.position.copy(START_CAM_POS);
    controls.target.copy(START_TARGET);
    controls.update();

    const box2 = new THREE.Box3().setFromObject(vrm.scene);
    const size2 = box2.getSize(new THREE.Vector3());

    const maxDim = Math.max(size2.x, size2.y, size2.z);
    const fov = (camera.fov * Math.PI) / 180;
    let dist = maxDim / (2 * Math.tan(fov / 2));
    dist *= 1.4;

    
    camera.near = Math.max(0.001, dist / 100);
    camera.far = dist * 100;
    camera.updateProjectionMatrix();

    
    controls.update();

    // Make it feel alive
    applyArmsDownPose();
    startBlinkLoop();

    badge.textContent = "✅ VRM ready";
    console.log("VRM ready ✅", vrm);
  },
  (prog) => {
    if (prog.total) {
      const pct = Math.round((prog.loaded / prog.total) * 100);
      badge.textContent = `Loading /avatar.vrm … ${pct}%`;
    }
  },
  (err) => {
    console.error("❌ Failed to load /avatar.vrm:", err);
    badge.textContent = "❌ Failed to load VRM (see console)";
  }
);

// --------------------
// Render loop
// --------------------
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  controls.update();

  const dt = clock.getDelta();
  if (vrm) vrm.update(dt);

  renderer.render(scene, camera);
}
animate();

// --------------------
// Resize
// --------------------
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
