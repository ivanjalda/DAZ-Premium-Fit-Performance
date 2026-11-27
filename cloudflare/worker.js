// DAZ Performance · Bot de Telegram (Cloudflare Worker)
// - GET  /subscribers  -> lista de clientes activos (solo con ADMIN_SECRET)
// - POST /stripe       -> aviso de Stripe cuando alguien paga o cancela Premium
// - POST /             -> webhook de Telegram (/start, /plan, /stop, /premium, /ayuda)
const WEB = "https://dazperformance.com";
const PREMIUM = "https://dazperformance.com/premium.html";
const PERFIL = "https://dazperformance.com/perfil.html";
const PAY_URL = "https://buy.stripe.com/fZueVefzC9yI0I66iq1gY2W";
const TRIAL_DAYS = 7;
const payLink = (chatId) => `${PAY_URL}?client_reference_id=${chatId}`;
// Packs: enlace de pago de Stripe -> pack
const PACK_URLS = {
  full: PAY_URL,
  entreno: "https://buy.stripe.com/cNi3cw87acKU8ay22a1gZ0X",
  nutricion: "https://buy.stripe.com/4gM8wQ7365is9eC5em1gZ0Y",
  suplementos: "https://buy.stripe.com/9B614oafibGQbmKgX41gZ0Z",
};
const PACK_BY_PLINK = {
  plink_1UgRmjLJVU4oTPuXB9gN3N71: "entreno",
  plink_1UgRoJLJVU4oTPuXNy5YWwMI: "nutricion",
  plink_1UgRpiLJVU4oTPuXBHIyytKy: "suplementos",
};
const PACK_NAMES = {
  full: { es: "⭐ Pack Completo", en: "⭐ Complete Pack" },
  entreno: { es: "🏋️ Pack Entrenamiento", en: "🏋️ Training Pack" },
  nutricion: { es: "🍽️ Pack Nutrición", en: "🍽️ Nutrition Pack" },
  suplementos: { es: "💊 Pack Suplementos", en: "💊 Supplements Pack" },
};
const packLink = (p, chatId) => `${PACK_URLS[p]}?client_reference_id=${chatId}`;
const userPacks = (u) => { const s = new Set(u.packs || []); if (u.premium) s.add("full"); return [...s]; };
function packsMenu(L, chatId) {
  return L === "en"
    ? `⭐ DAZ Performance packs (cancel anytime):\n\n🏋️ Training · 2.99 €/mo\nEvery routine + your daily session\n👉 ${packLink("entreno", chatId)}\n\n🍽️ Nutrition · 2.99 €/mo\nDaily meal plan in grams + macros\n👉 ${packLink("nutricion", chatId)}\n\n💊 Supplements · 1.99 €/mo\nYour stack with doses and timing\n👉 ${packLink("suplementos", chatId)}\n\n⭐ COMPLETE · 4.99 €/mo (all 3, save 2.98 €)\n👉 ${packLink("full", chatId)}`
    : `⭐ Packs DAZ Performance (cancela cuando quieras):\n\n🏋️ Entrenamiento · 2,99 €/mes\nTodas las rutinas + tu sesión diaria\n👉 ${packLink("entreno", chatId)}\n\n🍽️ Nutrición · 2,99 €/mes\nTu menú diario en gramos + macros\n👉 ${packLink("nutricion", chatId)}\n\n💊 Suplementos · 1,99 €/mes\nTu stack con dosis y horario\n👉 ${packLink("suplementos", chatId)}\n\n⭐ COMPLETO · 4,99 €/mes (los 3, ahorras 2,98 €)\n👉 ${packLink("full", chatId)}`;
}

const SPLITS = {
  ppl6: { es: "Push / Pull / Legs · 6 días", en: "Push / Pull / Legs · 6 days" },
  ul4: { es: "Torso / Pierna · 4 días", en: "Upper / Lower · 4 days" },
  fb3: { es: "Full Body · 3 días", en: "Full Body · 3 days" },
  spec_arms: { es: "Brazos y Hombros · 5 días", en: "Arms & Shoulders · 5 days" },
  spec_legs: { es: "Pierna y Glúteo · 5 días", en: "Legs & Glutes · 5 days" },
};
const GOALS = {
  volumen: { es: "Volumen / Hipertrofia", en: "Lean Bulk / Hypertrophy" },
  definicion: { es: "Definición / Perder grasa", en: "Fat Loss / Cut" },
  recomposicion: { es: "Recomposición", en: "Recomposition" },
};

function parseStart(payload) {
  // formato: idioma_programa_peso_objetivo  (el programa puede llevar "_", p. ej. spec_arms)
  const p = String(payload || "").trim().split("_").filter(Boolean);
  if (p.length < 4) return null;
  const lang = p[0] === "en" ? "en" : "es";
  const goal = GOALS[p[p.length - 1]] ? p[p.length - 1] : "volumen";
  let weight = parseFloat(p[p.length - 2]);
  if (!isFinite(weight)) weight = 80;
  weight = Math.max(40, Math.min(220, weight));
  const split = p.slice(1, -2).join("_");
  return { lang, split: SPLITS[split] ? split : "ppl6", weight: String(weight), goal };
}

async function tg(env, method, body) {
  return fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

function send(env, chatId, text) {
  return tg(env, "sendMessage", { chat_id: chatId, text, disable_web_page_preview: true });
}

function status(u) {
  const L = u.lang === "en" ? "en" : "es";
  const ps = userPacks(u);
  if (ps.length) return ps.map((p) => PACK_NAMES[p][L]).join(" + ") + (L === "en" ? " active" : " activo");
  const left = Math.ceil(TRIAL_DAYS - (Date.now() - Date.parse(u.created || Date.now())) / 86400000);
  if (left > 0) return L === "en" ? `🎁 Free trial: ${left} day(s) left` : `🎁 Prueba gratis: te quedan ${left} día(s)`;
  return L === "en" ? "🔒 Trial ended — /premium to choose your pack" : "🔒 Prueba terminada — /premium para elegir tu pack";
}

function summary(u) {
  const L = u.lang === "en" ? "en" : "es";
  const kcalF = { volumen: 35, definicion: 26, recomposicion: 30 }[u.goal] || 32;
  const w = parseFloat(u.weight) || 80;
  const kcal = Math.round((w * kcalF) / 50) * 50;
  const prot = Math.round(w * 2);
  if (L === "en") {
    return `🔥 DAZ PERFORMANCE — ACCOUNT LINKED\n\nWelcome, ${u.name}.\n• Program: ${SPLITS[u.split].en}\n• Goal: ${GOALS[u.goal].en}\n• Weight: ${w} kg\n• Daily target: ~${kcal} kcal · ${prot} g protein\n• ${status(u)}\n\nEvery morning you'll get your exact session here (or a recovery plan on rest days).\n\nCommands: /plan your data · /stop pause · /premium go Premium\nChange your data: ${PERFIL}\n\n⭐ Packs from 1.99 €/month — send /premium · Complete Pack 4.99 € → ${payLink(u.chat_id)}`;
  }
  return `🔥 DAZ PERFORMANCE — CUENTA VINCULADA\n\nBienvenido, ${u.name}.\n• Programa: ${SPLITS[u.split].es}\n• Objetivo: ${GOALS[u.goal].es}\n• Peso: ${w} kg\n• Objetivo diario: ~${kcal} kcal · ${prot} g de proteína\n• ${status(u)}\n\nCada mañana recibirás aquí tu sesión exacta del día (o tu plan de recuperación en días de descanso).\n\nComandos: /plan tus datos · /stop pausar · /premium hazte Premium\nCambiar tus datos: ${PERFIL}\n\n⭐ Packs desde 1,99 €/mes — escribe /premium · Pack Completo 4,99 € → ${payLink(u.chat_id)}`;
}

async function verifyStripe(env, raw, header) {
  if (!env.STRIPE_WEBHOOK_SECRET || !header) return false;
  const parts = Object.fromEntries(header.split(",").map((kv) => kv.split("=")));
  if (!parts.t || !parts.v1) return false;
  if (Math.abs(Date.now() / 1000 - Number(parts.t)) > 600) return false;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.STRIPE_WEBHOOK_SECRET),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${parts.t}.${raw}`));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  const sigs = header.split(",").filter((x) => x.startsWith("v1=")).map((x) => x.slice(3));
  return sigs.includes(hex);
}

async function handleStripe(request, env) {
  const raw = await request.text();
  if (!(await verifyStripe(env, raw, request.headers.get("Stripe-Signature")))) {
    return new Response("Bad signature", { status: 400 });
  }
  const event = JSON.parse(raw);
  const obj = event.data && event.data.object ? event.data.object : {};
  if (event.type === "checkout.session.completed") {
    const chatId = obj.client_reference_id;
    const pack = PACK_BY_PLINK[obj.payment_link] || "full";
    if (chatId && /^-?\d+$/.test(chatId)) {
      const key = `user_${chatId}`;
      const user = (await env.DAZ_USERS.get(key, "json")) || { chat_id: Number(chatId), name: "Atleta", lang: "es", split: "ppl6", weight: "80", goal: "volumen", created: new Date().toISOString() };
      const ps = new Set(user.packs || []);
      ps.add(pack);
      user.packs = [...ps];
      if (pack === "full") user.premium = true;
      user.active = true;
      user.premium_since = user.premium_since || new Date().toISOString();
      await env.DAZ_USERS.put(key, JSON.stringify(user));
      if (obj.subscription) await env.DAZ_USERS.put(`sub_${obj.subscription}`, JSON.stringify({ chatId: String(chatId), pack }));
      const L = user.lang === "en" ? "en" : "es";
      await send(env, chatId, L === "en"
        ? `✅ ${PACK_NAMES[pack].en} activated! You'll get it every morning here. Thank you 💪`
        : `✅ ¡${PACK_NAMES[pack].es} activado! Lo recibirás aquí cada mañana. Gracias 💪`);
    }
  } else if (event.type === "customer.subscription.deleted") {
    const raw = await env.DAZ_USERS.get(`sub_${obj.id}`);
    if (raw) {
      let info;
      try { info = JSON.parse(raw); } catch (e) { info = { chatId: raw, pack: "full" }; }
      if (typeof info !== "object" || info === null) info = { chatId: String(raw), pack: "full" };
      const key = `user_${info.chatId}`;
      const user = await env.DAZ_USERS.get(key, "json");
      if (user) {
        user.packs = (user.packs || []).filter((p) => p !== info.pack);
        if (info.pack === "full") user.premium = false;
        await env.DAZ_USERS.put(key, JSON.stringify(user));
        const L = user.lang === "en" ? "en" : "es";
        await send(env, info.chatId, L === "en"
          ? `Your ${PACK_NAMES[info.pack].en} has ended. Come back anytime: /premium`
          : `Tu ${PACK_NAMES[info.pack].es} ha terminado. Puedes volver cuando quieras: /premium`);
      }
    }
  }
  return new Response("OK");
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/stripe" && request.method === "POST") return handleStripe(request, env);

    // 1. GitHub Actions lee los clientes cada mañana (solo claves user_)
    if (url.pathname === "/subscribers" && request.method === "GET") {
      const auth = request.headers.get("Authorization");
      if (auth !== `Bearer ${env.ADMIN_SECRET}`) return new Response("Unauthorized", { status: 401 });
      const users = [];
      let cursor;
      do {
        const list = await env.DAZ_USERS.list({ prefix: "user_", cursor });
        for (const key of list.keys) {
          const val = await env.DAZ_USERS.get(key.name, "json");
          if (val && val.active) users.push(val);
        }
        cursor = list.list_complete ? null : list.cursor;
      } while (cursor);
      return new Response(JSON.stringify(users), { headers: { "Content-Type": "application/json" } });
    }

    // 2. Webhook de Telegram
    if (request.method === "POST") {
      let update;
      try { update = await request.json(); } catch (e) { return new Response("OK"); }
      const msg = update.message;
      if (!msg || !msg.text) return new Response("OK");
      const chatId = msg.chat.id;
      const name = (msg.from && msg.from.first_name) || "Atleta";
      const text = msg.text.trim();
      const key = `user_${chatId}`;
      const saved = await env.DAZ_USERS.get(key, "json");
      const lang = saved ? saved.lang : ((msg.from && msg.from.language_code) || "es").startsWith("en") ? "en" : "es";

      if (text.startsWith("/start")) {
        const data = parseStart(text.split(" ")[1]);
        if (data) {
          const user = { ...(saved || {}), chat_id: chatId, name, ...data, active: true,
            created: saved && saved.created ? saved.created : new Date().toISOString(),
            updated: new Date().toISOString() };
          await env.DAZ_USERS.put(key, JSON.stringify(user));
          await send(env, chatId, summary(user));
        } else if (saved) {
          saved.active = true; saved.updated = new Date().toISOString();
          await env.DAZ_USERS.put(key, JSON.stringify(saved));
          await send(env, chatId, summary(saved));
        } else {
          await send(env, chatId, lang === "en"
            ? `👋 Welcome to DAZ Performance.\n\nTo get YOUR daily workout, set your weight, goal and training days here (1 minute):\n👉 ${PERFIL}\n\nThen tap "Activate on Telegram" and you're in.`
            : `👋 Bienvenido a DAZ Performance.\n\nPara recibir TU entrenamiento diario, pon tu peso, objetivo y días de entreno aquí (1 minuto):\n👉 ${PERFIL}\n\nLuego pulsa "Activar en Telegram" y listo.`);
        }
      } else if (text.startsWith("/stop")) {
        if (saved) { saved.active = false; await env.DAZ_USERS.put(key, JSON.stringify(saved)); }
        await send(env, chatId, lang === "en"
          ? "⏸️ Daily messages paused. Send /start whenever you want to come back."
          : "⏸️ Envíos diarios pausados. Escribe /start cuando quieras volver.");
      } else if (text.startsWith("/plan")) {
        await send(env, chatId, saved ? summary(saved)
          : (lang === "en" ? `Set up your profile first: ${PERFIL}` : `Primero configura tu perfil: ${PERFIL}`));
      } else if (text.startsWith("/premium")) {
        await send(env, chatId, packsMenu(lang, chatId));
      } else {
        await send(env, chatId, lang === "en"
          ? `🤖 Commands:\n/plan your data\n/premium go Premium\n/stop pause messages\n\n🌐 ${WEB}`
          : `🤖 Comandos:\n/plan tus datos\n/premium hazte Premium\n/stop pausar envíos\n\n🌐 ${WEB}`);
      }
      return new Response("OK");
    }

    return new Response("DAZ Performance Bot Worker Active");
  },
};
