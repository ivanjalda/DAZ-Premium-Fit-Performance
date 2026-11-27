/* DAZ Performance: packs de pago (Entrenamiento, Nutrición, Suplementos, Completo) y zona gratis. */
(() => {
  const PACKS = {
    entreno: { url: "https://buy.stripe.com/cNi3cw87acKU8ay22a1gZ0X", price: "2,99 €", icon: "🏋️",
      es: { name: "Pack Entrenamiento", desc: "Todas las rutinas y tu sesión diaria en Telegram" },
      en: { name: "Training Pack", desc: "Every routine and your daily session on Telegram" } },
    nutricion: { url: "https://buy.stripe.com/4gM8wQ7365is9eC5em1gZ0Y", price: "2,99 €", icon: "🍽️",
      es: { name: "Pack Nutrición", desc: "Tu menú diario en gramos y tus macros" },
      en: { name: "Nutrition Pack", desc: "Your daily meal plan in grams and your macros" } },
    suplementos: { url: "https://buy.stripe.com/9B614oafibGQbmKgX41gZ0Z", price: "1,99 €", icon: "💊",
      es: { name: "Pack Suplementos", desc: "Tus suplementos con dosis y horario" },
      en: { name: "Supplements Pack", desc: "Your supplements with doses and timing" } },
    full: { url: "https://buy.stripe.com/fZueVefzC9yI0I66iq1gY2W", price: "4,99 €", icon: "⭐",
      es: { name: "Pack Completo (Premium)", desc: "Los 3 packs juntos + planificador total. Ahorras 2,98 €" },
      en: { name: "Complete Pack (Premium)", desc: "All 3 packs + full planner. Save 2.98 €" } },
  };
  const KEY = "daz_packs";
  const OLD_KEY = "daz_premium";
  const lang = () => (localStorage.getItem("daz_lang") || "es") === "en" ? "en" : "es";

  const T = {
    es: {
      cta: "⭐ Packs desde 1,99 €/mes",
      lockTitle: "Contenido de pago",
      lockText: "Desbloquea esta sección con su pack o con el Pack Completo.",
      lockBtn: "Ver packs",
      modalTitle: "Elige tu pack DAZ Performance",
      month: "mes",
      best: "MÁS ELEGIDO",
      close: "Ahora no",
      trial: "🎁 ¿Lo quieres probar antes? 7 días gratis de tu plan en Telegram",
      welcome: "✅ ¡Pack activado! Ya tienes desbloqueado tu contenido en este dispositivo. Rellena tus datos en Mi Cuenta y pulsa el botón de Telegram para recibirlo cada mañana.",
      badge: "ACTIVO",
    },
    en: {
      cta: "⭐ Packs from 1.99 €/mo",
      lockTitle: "Paid content",
      lockText: "Unlock this section with its pack or with the Complete Pack.",
      lockBtn: "See packs",
      modalTitle: "Choose your DAZ Performance pack",
      month: "mo",
      best: "MOST POPULAR",
      close: "Not now",
      trial: "🎁 Want to try first? 7 free days of your plan on Telegram",
      welcome: "✅ Pack activated! Your content is unlocked on this device. Fill in your details in My Account and tap the Telegram button to get it every morning.",
      badge: "ACTIVE",
    },
  };

  // Packs comprados en este navegador
  function getPacks() {
    let packs = [];
    try { packs = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (_) { packs = []; }
    try { if (localStorage.getItem(OLD_KEY)) packs.push("full"); } catch (_) {}
    return [...new Set(packs.filter((p) => PACKS[p]))];
  }
  function addPack(p) {
    const packs = getPacks();
    if (!packs.includes(p)) packs.push(p);
    try { localStorage.setItem(KEY, JSON.stringify(packs)); } catch (_) {}
  }
  const hasPack = (p) => { const ps = getPacks(); return ps.includes("full") || ps.includes(p); };
  const isPremium = () => getPacks().includes("full");
  window.dazHasPack = hasPack;
  window.dazIsPremium = isPremium;

  // 1. Activar el pack al volver del pago
  try {
    const params = new URLSearchParams(location.search);
    const session = params.get("premium_session");
    if (session && /^cs_/.test(session)) {
      const pack = params.get("pack");
      addPack(PACKS[pack] ? pack : "full");
      sessionStorage.setItem("daz_premium_welcome", "1");
      history.replaceState(null, "", location.pathname);
    }
  } catch (_) {}

  const css = `
  .dzp-cta{position:fixed;right:18px;bottom:18px;z-index:9998;background:linear-gradient(135deg,#ef4444,#991b1b);color:#fff;
    font-weight:800;border:1px solid #d4af37;border-radius:999px;padding:13px 20px;font-size:.95rem;cursor:pointer;
    box-shadow:0 8px 28px rgba(239,68,68,.45);text-decoration:none;letter-spacing:.3px}
  .dzp-cta:hover{transform:translateY(-2px)}
  .dzp-badge{position:fixed;right:18px;bottom:18px;z-index:9998;background:#0b0d12;color:#d4af37;border:1px solid #d4af37;
    border-radius:999px;padding:9px 16px;font-weight:800;font-size:.8rem;cursor:pointer}
  .dzp-locked{position:relative;min-height:220px;overflow:hidden}
  .dzp-locked>*:not(.dzp-veil){filter:blur(6px);pointer-events:none;user-select:none}
  .dzp-veil{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;
    gap:10px;text-align:center;padding:20px;background:rgba(6,7,9,.72);border:1px solid rgba(212,175,55,.38);border-radius:12px}
  .dzp-veil h4{color:#d4af37;font-size:1.1rem;margin:0}
  .dzp-veil p{color:#e5e7eb;margin:0;max-width:420px}
  .dzp-btn{background:linear-gradient(135deg,#ef4444,#991b1b);color:#fff;border:1px solid #d4af37;border-radius:10px;
    padding:12px 18px;font-weight:800;cursor:pointer;text-decoration:none;display:inline-block}
  .dzp-modal{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.78);display:flex;align-items:center;justify-content:center;padding:16px;overflow:auto}
  .dzp-box{background:#0b0d12;border:1px solid #d4af37;border-radius:16px;max-width:520px;width:100%;padding:22px;color:#f3f4f6;max-height:92vh;overflow:auto}
  .dzp-box h3{color:#d4af37;margin:0 0 12px;text-align:center}
  .dzp-pack{display:flex;align-items:center;gap:12px;border:1px solid #2a2f3a;border-radius:12px;padding:12px 14px;margin:8px 0;
    text-decoration:none;color:#f3f4f6;background:#11141b;position:relative}
  .dzp-pack:hover{border-color:#d4af37}
  .dzp-pack.full{border:2px solid #d4af37;background:linear-gradient(135deg,rgba(239,68,68,.16),rgba(212,175,55,.12))}
  .dzp-pack.hl{border-color:#ef4444;box-shadow:0 0 0 2px rgba(239,68,68,.35)}
  .dzp-pack .ic{font-size:1.6rem}
  .dzp-pack .tx{flex:1}
  .dzp-pack .tx b{display:block}
  .dzp-pack .tx small{color:#9ca3af}
  .dzp-pack .pr{font-weight:900;white-space:nowrap}
  .dzp-pack .tag{position:absolute;top:-9px;right:12px;background:#d4af37;color:#000;font-size:.65rem;font-weight:900;border-radius:6px;padding:2px 7px}
  .dzp-pack .ok{color:#10b981;font-weight:900}
  .dzp-trial{display:block;text-align:center;color:#d4af37;margin-top:12px;font-weight:700;text-decoration:none}
  .dzp-close{background:none;border:none;color:#9ca3af;margin-top:10px;cursor:pointer;width:100%}
  .dzp-welcome{background:rgba(16,185,129,.12);border:1px solid #10b981;color:#e5e7eb;border-radius:12px;padding:14px 16px;margin:16px auto;max-width:1100px}
  `;

  function packRow(id, highlight) {
    const L = lang();
    const p = PACKS[id];
    const owned = hasPack(id) && (id === "full" ? isPremium() : true);
    const right = owned ? `<span class="ok">✔ ${T[L].badge}</span>` : `<span class="pr">${p.price}/${T[L].month}</span>`;
    const tag = id === "full" ? `<span class="tag">${T[L].best}</span>` : "";
    const cls = `dzp-pack${id === "full" ? " full" : ""}${highlight === id ? " hl" : ""}`;
    const href = owned ? "#" : p.url;
    return `<a class="${cls}" href="${href}" rel="noopener">${tag}<span class="ic">${p.icon}</span>
      <span class="tx"><b>${p[L].name}</b><small>${p[L].desc}</small></span>${right}</a>`;
  }

  function openModal(highlight) {
    const t = T[lang()];
    const m = document.createElement("div");
    m.className = "dzp-modal";
    m.innerHTML = `<div class="dzp-box"><h3>${t.modalTitle}</h3>
      ${["full", "entreno", "nutricion", "suplementos"].map((id) => packRow(id, highlight)).join("")}
      <a class="dzp-trial" href="perfil.html">${t.trial}</a>
      <button class="dzp-close" type="button">${t.close}</button></div>`;
    m.addEventListener("click", (e) => {
      if (e.target === m || e.target.classList.contains("dzp-close")) m.remove();
      const a = e.target.closest && e.target.closest("a.dzp-pack");
      if (a && a.getAttribute("href") === "#") e.preventDefault();
    });
    document.body.appendChild(m);
  }
  window.dazOpenPremium = openModal;

  function lock(el, pack) {
    if (!el || el.classList.contains("dzp-locked") || hasPack(pack)) return;
    const t = T[lang()];
    const name = PACKS[pack][lang()].name;
    el.classList.add("dzp-locked");
    const v = document.createElement("div");
    v.className = "dzp-veil";
    v.innerHTML = `<h4>🔒 ${t.lockTitle}</h4><p>${t.lockText}</p>
      <a class="dzp-btn" href="${PACKS[pack].url}" rel="noopener">${PACKS[pack].icon} ${name} · ${PACKS[pack].price}/${t.month}</a>
      <button type="button" class="dzp-btn" style="background:#11141b">${t.lockBtn}</button>`;
    v.querySelector("button").addEventListener("click", () => openModal(pack));
    el.appendChild(v);
  }

  function lockByHeading(texts, pack) {
    document.querySelectorAll("h2,h3").forEach((h) => {
      const txt = (h.textContent || "").toLowerCase();
      if (texts.some((x) => txt.includes(x))) lock(h.closest(".card") || h.parentElement, pack);
    });
  }

  function guardFunction(name, pack, isAllowed) {
    const original = window[name];
    if (typeof original !== "function" || original.__dzp) return;
    const wrapped = function (...args) {
      if (!hasPack(pack) && !isAllowed(...args)) { openModal(pack); return; }
      return original.apply(this, args);
    };
    wrapped.__dzp = true;
    window[name] = wrapped;
  }

  function applyGates() {
    if (isPremium()) return;
    const page = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    if (page === "nutricion.html") lockByHeading(["configura tu plan", "tu plan diario", "set up your plan", "your daily plan"], "nutricion");
    if (page === "suplementacion.html") lockByHeading(["calcula tu stack", "calculate your stack"], "suplementos");
    if (page === "entrenamiento.html") guardFunction("chooseRoutine", "entreno", (idx) => Number(idx) === 0);
    // Planificador total (cruza los 3 packs): 1 uso gratis al día, después Pack Completo
    if (page === "index.html" || page === "") guardFunction("runPlanner", "full", () => {
      const today = new Date().toISOString().slice(0, 10);
      let used = null;
      try { used = localStorage.getItem("daz_free_planner"); } catch (e) {}
      if (used === today) return false;
      try { localStorage.setItem("daz_free_planner", today); } catch (e) {}
      return true;
    });
  }

  function init() {
    const style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
    const t = T[lang()];
    const packs = getPacks();
    if (packs.length) {
      const b = document.createElement("div");
      b.className = "dzp-badge";
      b.textContent = isPremium() ? `⭐ PREMIUM ${t.badge}` : packs.map((p) => PACKS[p].icon).join(" ") + ` ${t.badge} · +`;
      b.addEventListener("click", () => openModal());
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
      a.addEventListener("click", () => openModal());
      document.body.appendChild(a);
    }
    applyGates();
    new MutationObserver(() => applyGates()).observe(document.body, { childList: true, subtree: true });
    setTimeout(applyGates, 1500);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
