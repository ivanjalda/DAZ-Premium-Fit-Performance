// DAZ Performance · Bot de Telegram (Cloudflare Worker)
// - GET  /subscribers  -> lista de clientes activos (solo con ADMIN_SECRET)
// - POST /             -> webhook de Telegram (/start, /plan, /stop, /premium, /ayuda)
const WEB = "https://dazperformance.com";
const PREMIUM = "https://dazperformance.com/premium.html";
const PERFIL = "https://dazperformance.com/perfil.html";

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

function summary(u) {
  const L = u.lang === "en" ? "en" : "es";
  const kcalF = { volumen: 35, definicion: 26, recomposicion: 30 }[u.goal] || 32;
  const w = parseFloat(u.weight) || 80;
  const kcal = Math.round((w * kcalF) / 50) * 50;
  const prot = Math.round(w * 2);
  if (L === "en") {
    return `🔥 DAZ PERFORMANCE — ACCOUNT LINKED\n\nWelcome, ${u.name}.\n• Program: ${SPLITS[u.split].en}\n• Goal: ${GOALS[u.goal].en}\n• Weight: ${w} kg\n• Daily target: ~${kcal} kcal · ${prot} g protein\n\nEvery morning you'll get your exact session here (or a recovery plan on rest days).\n\nCommands: /plan your data · /stop pause · /premium go Premium\nChange your data: ${PERFIL}\n\n⭐ Premium 4.99 €/month: every routine, meal plan in grams and custom supplements → ${PREMIUM}`;
  }
  return `🔥 DAZ PERFORMANCE — CUENTA VINCULADA\n\nBienvenido, ${u.name}.\n• Programa: ${SPLITS[u.split].es}\n• Objetivo: ${GOALS[u.goal].es}\n• Peso: ${w} kg\n• Objetivo diario: ~${kcal} kcal · ${prot} g de proteína\n\nCada mañana recibirás aquí tu sesión exacta del día (o tu plan de recuperación en días de descanso).\n\nComandos: /plan tus datos · /stop pausar · /premium hazte Premium\nCambiar tus datos: ${PERFIL}\n\n⭐ Premium 4,99 €/mes: todas las rutinas, menú en gramos y suplementos a tu medida → ${PREMIUM}`;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. GitHub Actions lee los clientes cada mañana
    if (url.pathname === "/subscribers" && request.method === "GET") {
      const auth = request.headers.get("Authorization");
      if (auth !== `Bearer ${env.ADMIN_SECRET}`) return new Response("Unauthorized", { status: 401 });
      const users = [];
      let cursor;
      do {
        const list = await env.DAZ_USERS.list({ cursor });
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
          const user = { chat_id: chatId, name, ...data, active: true,
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
        await send(env, chatId, lang === "en"
          ? `⭐ DAZ Performance Premium · 4.99 €/month\n• Every routine unlocked\n• Meal plan in grams for your goal\n• Supplement stack calculator\n• Personal workout every morning\n\n👉 ${PREMIUM}`
          : `⭐ DAZ Performance Premium · 4,99 €/mes\n• Todas las rutinas desbloqueadas\n• Menú en gramos para tu objetivo\n• Calculadora de suplementos\n• Tu entrenamiento personal cada mañana\n\n👉 ${PREMIUM}`);
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
