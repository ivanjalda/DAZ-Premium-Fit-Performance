/* DAZ Performance: enlaces a la tienda de suplementos de DAZ Premium Fit.
   Mientras la tienda no publique los suplementos, se muestran como "Próximamente".
   El revisor automático (guardian.py) cambia data/store_status.json cuando ya están publicados. */
(() => {
  const isEn = () => (localStorage.getItem("daz_lang") || "es") === "en";
  function apply(live) {
    if (live) return;
    document.querySelectorAll('a[href*="dazpremiumfit.com/collections/supplements"]').forEach((a) => {
      if (a.dataset.dzSoon) return;
      a.dataset.dzSoon = "1";
      a.removeAttribute("href");
      a.removeAttribute("target");
      a.style.opacity = "0.6";
      a.style.cursor = "default";
      a.textContent = isEn() ? "🔜 Coming soon to DAZ Premium Fit" : "🔜 Próximamente en DAZ Premium Fit";
    });
  }
  function run() {
    fetch("/data/store_status.json", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : {}))
      .catch(() => ({}))
      .then((s) => {
        const live = !!(s && s.supplements_live);
        apply(live);
        if (!live) new MutationObserver(() => apply(false)).observe(document.body, { childList: true, subtree: true });
      });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
