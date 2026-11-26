/* DAZ Performance Premium: zona gratis / zona de pago y botón "Hazte Premium" en todas las páginas. */
(() => {
  const PAY_URL = "https://buy.stripe.com/fZueVefzC9yI0I66iq1gY2W";
  const PRICE = "4,99 €";
  const KEY = "daz_premium";
  const lang = () => (localStorage.getItem("daz_lang") || "es") === "en" ? "en" : "es";

  const T = {
    es: {
      cta: `⭐ Hazte Premium · ${PRICE}/mes`,
      lockTitle: "Contenido Premium",
      lockText: "Desbloquea esta sección con DAZ Performance Premium.",
      lockBtn: `Desbloquear por ${PRICE}/mes`,
      modalTitle: "DAZ Performance Premium",
      perks: [
        "Entrenamiento personal cada mañana en tu Telegram",
        "Todas las rutinas por objetivo, no solo la básica",
        "Tu plan de comidas diario en gramos según tu objetivo",
        "Tu combinación de suplementos con dosis y horario",
        "Planificador total con calorías, macros y rutina",
        "Cancela cuando quieras",
      ],
      go: `Suscribirme por ${PRICE}/mes`,
      close: "Ahora no",
      welcome: "✅ ¡Bienvenido a Premium! Ya tienes todo desbloqueado en este dispositivo. Rellena tus datos y pulsa el botón de Telegram para recibir tu entrenamiento personal cada mañana.",
      badge: "⭐ PREMIUM ACTIVO",
    },
    en: {
      cta: `⭐ Go Premium · ${PRICE}/mo`,
      lockTitle: "Premium content",
      lockText: "Unlock this section with DAZ Performance Premium.",
      lockBtn: `Unlock for ${PRICE}/mo`,
      modalTitle: "DAZ Performance Premium",
      perks: [
        "Personal workout every morning on Telegram",
        "Every routine for your goal, not just the basic one",
        "Your daily meal plan in grams for your goal",
        "Your supplement stack with doses and timing",
        "Full planner with calories, macros and routine",
        "Cancel anytime",
      ],
      go: `Subscribe for ${PRICE}/mo`,
      close: "Not now",
      welcome: "✅ Welcome to Premium! Everything is unlocked on this device. Fill in your details and tap the Telegram button to get your personal workout every morning.",
      badge: "⭐ PREMIUM ACTIVE",
    },
  };

  // 1. Activar Premium al volver del pago
  try {
    const params = new URLSearchParams(location.search);
    const session = params.get("premium_session");
    if (session && /^cs_/.test(session)) {
      localStorage.setItem(KEY, JSON.stringify({ session, since: new Date().toISOString() }));
      sessionStorage.setItem("daz_premium_welcome", "1");
      history.replaceState(null, "", location.pathname);
    }
  } catch (_) {}

  const isPremium = () => {
    try { return !!JSON.parse(localStorage.getItem(KEY) || "null"); } catch (_) { return false; }
  };
  window.dazIsPremium = isPremium;

  const css = `
  .dzp-cta{position:fixed;right:18px;bottom:18px;z-index:9998;background:linear-gradient(135deg,#ef4444,#991b1b);color:#fff;
    font-weight:800;border:1px solid #d4af37;border-radius:999px;padding:13px 20px;font-size:.95rem;cursor:pointer;
    box-shadow:0 8px 28px rgba(239,68,68,.45);text-decoration:none;letter-spacing:.3px}
  .dzp-cta:hover{transform:translateY(-2px)}
  .dzp-badge{position:fixed;right:18px;bottom:18px;z-index:9998;background:#0b0d12;color:#d4af37;border:1px solid #d4af37;
    border-radius:999px;padding:9px 16px;font-weight:800;font-size:.8rem}
  .dzp-locked{position:relative;min-height:220px;overflow:hidden}
  .dzp-locked>*:not(.dzp-veil){filter:blur(6px);pointer-events:none;user-select:none}
  .dzp-veil{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;
    gap:10px;text-align:center;padding:20px;background:rgba(6,7,9,.72);border:1px solid rgba(212,175,55,.38);border-radius:12px}
  .dzp-veil h4{color:#d4af37;font-size:1.1rem;margin:0}
  .dzp-veil p{color:#e5e7eb;margin:0;max-width:420px}
  .dzp-btn{background:linear-gradient(135deg,#ef4444,#991b1b);color:#fff;border:1px solid #d4af37;border-radius:10px;
    padding:12px 18px;font-weight:800;cursor:pointer;text-decoration:none;display:inline-block}
  .dzp-modal{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.75);display:flex;align-items:center;justify-content:center;padding:16px}
  .dzp-box{background:#0b0d12;border:1px solid #d4af37;border-radius:16px;max-width:440px;width:100%;padding:26px;color:#f3f4f6}
  .dzp-box h3{color:#d4af37;margin:0 0 6px}
  .dzp-box .dzp-price{font-size:2rem;font-weight:900;margin:6px 0 12px}
  .dzp-box ul{padding-left:0;list-style:none;margin:0 0 18px}
  .dzp-box li{margin:8px 0}
  .dzp-box li:before{content:"✔ ";color:#10b981;font-weight:900}
  .dzp-close{background:none;border:none;color:#9ca3af;margin-top:10px;cursor:pointer;width:100%}
  .dzp-welcome{background:rgba(16,185,129,.12);border:1px solid #10b981;color:#e5e7eb;border-radius:12px;padding:14px 16px;margin:16px auto;max-width:1100px}
  `;

  function openModal() {
    const t = T[lang()];
    const m = document.createElement("div");
    m.className = "dzp-modal";
    m.innerHTML = `<div class="dzp-box">
      <h3>${t.modalTitle}</h3>
      <div class="dzp-price">${PRICE}<small style="font-size:.9rem;color:#9ca3af"> / ${lang() === "en" ? "month" : "mes"}</small></div>
      <ul>${t.perks.map((p) => `<li>${p}</li>`).join("")}</ul>
      <a class="dzp-btn" style="width:100%;text-align:center;box-sizing:border-box" href="${PAY_URL}" rel="noopener">${t.go}</a>
      <button class="dzp-close" type="button">${t.close}</button></div>`;
    m.addEventListener("click", (e) => { if (e.target === m || e.target.classList.contains("dzp-close")) m.remove(); });
    document.body.appendChild(m);
  }
  window.dazOpenPremium = openModal;

  function lock(el) {
    if (!el || el.classList.contains("dzp-locked") || isPremium()) return;
    const t = T[lang()];
    el.classList.add("dzp-locked");
    const v = document.createElement("div");
    v.className = "dzp-veil";
    v.innerHTML = `<h4>🔒 ${t.lockTitle}</h4><p>${t.lockText}</p><button type="button" class="dzp-btn">${t.lockBtn}</button>`;
    v.querySelector("button").addEventListener("click", openModal);
    el.appendChild(v);
  }

  function lockByHeading(texts) {
    document.querySelectorAll("h2,h3").forEach((h) => {
      const txt = (h.textContent || "").toLowerCase();
      if (texts.some((x) => txt.includes(x))) lock(h.closest(".card") || h.parentElement);
    });
  }

  // Funciones de pago dentro de las herramientas
  function guardFunction(name, isAllowed) {
    const original = window[name];
    if (typeof original !== "function" || original.__dzp) return;
    const wrapped = function (...args) {
      if (!isPremium() && !isAllowed(...args)) { openModal(); return; }
      return original.apply(this, args);
    };
    wrapped.__dzp = true;
    window[name] = wrapped;
  }

  function applyGates() {
    if (isPremium()) return;
    const page = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    if (page === "nutricion.html") lockByHeading(["configura tu plan", "tu plan diario", "set up your plan", "your daily plan"]);
    if (page === "suplementacion.html") lockByHeading(["calcula tu stack", "calculate your stack"]);
    if (page === "entrenamiento.html") guardFunction("chooseRoutine", (idx) => Number(idx) === 0);
    if (page === "index.html" || page === "") guardFunction("runPlanner", () => false);
    if (page === "perfil.html") lockByHeading(["ejemplo de sesión", "sample session"]);
  }

  function init() {
    const style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
    const t = T[lang()];
    if (isPremium()) {
      const b = document.createElement("div");
      b.className = "dzp-badge";
      b.textContent = t.badge;
      document.body.appendChild(b);
      if (sessionStorage.getItem("daz_premium_welcome")) {
        sessionStorage.removeItem("daz_premium_welcome");
        const w = document.createElement("div");
        w.className = "dzp-welcome";
        w.textContent = t.welcome;
        (document.querySelector("main") || document.body).prepend(w);
      }
    } else {
      const a = document.createElement("button");
      a.type = "button";
      a.className = "dzp-cta";
      a.textContent = t.cta;
      a.addEventListener("click", openModal);
      document.body.appendChild(a);
    }
    applyGates();
    new MutationObserver(() => applyGates()).observe(document.body, { childList: true, subtree: true });
    setTimeout(applyGates, 1500);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
