(() => {
  const CHECK_INTERVAL_MS = 3 * 60 * 60 * 1000; // Cada 3 horas
  const LOG_KEY = "daz_self_heal_log";

  function recordHeal(action, detail) {
    try {
      const prev = JSON.parse(localStorage.getItem(LOG_KEY) || "[]");
      prev.unshift({
        ts: new Date().toISOString(),
        page: window.location.pathname,
        action,
        detail
      });
      localStorage.setItem(LOG_KEY, JSON.stringify(prev.slice(0, 40)));
    } catch (_) {}
  }

  function repairStorageAndState() {
    // Repara perfil corrupto o sin estructura válida
    try {
      const rawProfile = localStorage.getItem("daz_athlete_profile");
      if (rawProfile) {
        const parsed = JSON.parse(rawProfile);
        if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
          localStorage.setItem("daz_athlete_profile", "{}");
          recordHeal("storage_reset", "Perfil corrupto restaurado a objeto limpio");
        }
      }
    } catch (_) {
      localStorage.setItem("daz_athlete_profile", "{}");
      recordHeal("storage_parse_fix", "JSON inválido en daz_athlete_profile corregido");
    }

    // Repara lista de alimentos si se corrompe
    try {
      const rawFoods = localStorage.getItem("daz_food_entries");
      if (rawFoods) {
        const parsedFoods = JSON.parse(rawFoods);
        if (!Array.isArray(parsedFoods)) {
          localStorage.removeItem("daz_food_entries");
          recordHeal("food_log_fix", "Registro de alimentos no válido limpiado");
        }
      }
    } catch (_) {
      localStorage.removeItem("daz_food_entries");
      recordHeal("food_log_parse_fix", "JSON inválido en daz_food_entries limpiado");
    }
  }

  function repairDomAndLinks() {
    // Corrige enlaces rotos o inexistentes hacia dazpremiumfit.com o rutas locales
    document.querySelectorAll("a[href]").forEach((a) => {
      const href = a.getAttribute("href") || "";
      if (href.includes("dazshopping.com")) {
        a.setAttribute("href", "https://dazpremiumfit.com");
        recordHeal("link_fix", "Enlace dazshopping.com redirigido a dazpremiumfit.com");
      }
      if (href.trim() === "" || href.trim() === "#") {
        a.setAttribute("href", "index.html");
        recordHeal("empty_href_fix", "Enlace vacío redirigido a index.html");
      }
    });

    // Asegura que el contenedor principal no quede oculto por error tras un fallo de pestaña
    const main = document.querySelector("main.daz-container");
    if (main && getComputedStyle(main).display === "none") {
      main.style.display = "block";
      recordHeal("main_visibility_fix", "Contenedor principal restaurado a visible");
    }

    // Si en entrenamiento.html no hay rutina pintada y existe contenedor, fuerza renderizado si expuso función
    if (document.getElementById("routine-detail") && !document.getElementById("routine-detail").innerHTML.trim()) {
      if (typeof window.renderRoutines === "function") {
        window.renderRoutines();
        recordHeal("routine_render_fix", "Renderizado de rutinas recuperado automáticamente");
      }
    }

    // Si en nutricion.html falta calcular dieta o totales, fuerza recálculo si existen las funciones
    if (document.getElementById("tot-kcal") && typeof window.renderAll === "function") {
      window.renderAll();
    }
    if (document.getElementById("d-output") && !document.getElementById("d-output").innerHTML.trim() && typeof window.calculateDiet === "function") {
      window.calculateDiet();
      recordHeal("diet_render_fix", "Cálculo de dieta por objetivos recuperado");
    }
  }

  function runSelfCheck() {
    repairStorageAndState();
    repairDomAndLinks();
  }

  // Captura errores globales sin romper la experiencia del usuario
  window.addEventListener("error", (ev) => {
    recordHeal("runtime_error", `${ev.message || "Error"} (${ev.filename || "script"}:${ev.lineno || 0})`);
    setTimeout(runSelfCheck, 150);
  });

  window.addEventListener("unhandledrejection", (ev) => {
    const reason = ev && ev.reason ? (ev.reason.message || String(ev.reason)) : "Promesa rechazada";
    recordHeal("promise_rejection", reason);
    setTimeout(runSelfCheck, 150);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", runSelfCheck);
  } else {
    runSelfCheck();
  }

  // Revisión periódica cada varias horas mientras esté abierta la página
  setInterval(runSelfCheck, CHECK_INTERVAL_MS);

  // Expone diagnóstico rápido por consola si quieres revisarlo
  window.DAZSelfHeal = {
    runNow: runSelfCheck,
    getLogs: () => JSON.parse(localStorage.getItem(LOG_KEY) || "[]")
  };
})();
