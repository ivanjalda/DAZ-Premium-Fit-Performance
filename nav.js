(function () {
  const STORE_DPF = "https://dazpremiumfit.com";
  const STORE_DAZMOND = "https://dazmond.com";
  const STORE_VALMONT = "https://valmontco.com";

  const sharedStyles = `
    :root {
      --bg-main: #060709;
      --bg-panel: #0b0d12;
      --bg-card: #101319;
      --bg-card-alt: #151922;
      --border: #222733;
      --border-gold: rgba(212, 175, 55, 0.38);
      --gold: #d4af37;
      --gold-light: #f3d266;
      --gold-soft: rgba(212, 175, 55, 0.12);
      --crimson: #991b1b;
      --crimson-bright: #ef4444;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --green: #10b981;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
      line-height: 1.6;
      width: 100%;
      overflow-x: hidden;
    }

    /* TOP ECOSYSTEM BAR */
    .daz-eco-bar {
      width: 100%;
      background: linear-gradient(90deg, #07080a 0%, #191409 50%, #07080a 100%);
      border-bottom: 1px solid var(--border-gold);
      padding: 7px 2.5%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.75rem;
      letter-spacing: 0.8px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .daz-eco-bar .eco-title {
      color: var(--gold);
      font-weight: 800;
      text-transform: uppercase;
    }

    .daz-eco-links {
      display: flex;
      gap: 22px;
      flex-wrap: wrap;
    }

    .daz-eco-links a {
      color: #e5e7eb;
      text-decoration: none;
      font-weight: 600;
      transition: color 0.2s;
    }

    .daz-eco-links a:hover { color: var(--gold-light); }

    /* MAIN HEADER */
    .daz-header {
      position: sticky;
      top: 0;
      z-index: 999;
      width: 100%;
      background: rgba(6, 7, 9, 0.95);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      padding: 14px 2.5%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }

    .daz-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #fff;
      font-weight: 900;
      font-size: 1.15rem;
      letter-spacing: 1.8px;
      text-transform: uppercase;
    }

    .daz-brand span.gold { color: var(--gold); }
    .daz-brand span.badge-perf {
      background: var(--crimson);
      color: #fff;
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 3px;
      letter-spacing: 2px;
    }

    .daz-health-pill {
      font-family: monospace;
      font-size: 0.7rem;
      padding: 3px 10px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.1);
      color: var(--green);
      border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .daz-nav {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }

    .daz-nav a.nav-link {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.86rem;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: 6px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }

    .daz-nav a.nav-link:hover,
    .daz-nav a.nav-link.active {
      color: var(--gold);
      background: var(--gold-soft);
      border-color: var(--border-gold);
    }

    .daz-nav a.nav-cta {
      background: linear-gradient(135deg, var(--gold-light), var(--gold), #a67c1e);
      color: #060709;
      font-weight: 900;
      font-size: 0.82rem;
      padding: 9px 18px;
      border-radius: 6px;
      text-decoration: none;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      box-shadow: 0 4px 18px rgba(212, 175, 55, 0.25);
    }

    /* COMMON LAYOUT UTILITIES */
    .daz-container {
      width: 100%;
      padding: 36px 2.5% 60px;
    }

    .daz-page-banner {
      width: 100%;
      padding: 42px 2.5%;
      background:
        radial-gradient(circle at 85% 20%, rgba(212, 175, 55, 0.14), transparent 45%),
        radial-gradient(circle at 15% 85%, rgba(153, 27, 27, 0.16), transparent 45%),
        linear-gradient(180deg, #0c0e14 0%, #060709 100%);
      border-bottom: 1px solid var(--border);
    }

    .daz-page-banner .kicker {
      display: inline-block;
      font-size: 0.73rem;
      font-weight: 800;
      letter-spacing: 1.8px;
      color: var(--gold);
      border: 1px solid var(--border-gold);
      padding: 4px 12px;
      border-radius: 4px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }

    .daz-page-banner h1 {
      font-size: clamp(1.9rem, 3.2vw, 2.9rem);
      font-weight: 900;
      text-transform: uppercase;
      line-height: 1.1;
      margin-bottom: 10px;
    }

    .daz-page-banner p {
      color: var(--text-muted);
      font-size: 1.02rem;
      max-width: 850px;
    }

    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 22px; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 22px; }
    .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }

    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px;
      transition: border-color 0.2s;
    }

    .card:hover { border-color: var(--border-gold); }
    .card h3 { font-size: 1.18rem; margin-bottom: 8px; color: #fff; }

    .tag {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 4px;
      background: var(--gold-soft);
      color: var(--gold);
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }

    .tag-red { background: rgba(185, 28, 28, 0.22); color: #fca5a5; }
    .tag-green { background: rgba(16, 185, 129, 0.18); color: #6ee7b7; }

    .btn-primary {
      background: linear-gradient(135deg, var(--gold-light), var(--gold));
      color: #060709;
      padding: 13px 24px;
      border-radius: 6px;
      font-weight: 900;
      text-decoration: none;
      border: none;
      cursor: pointer;
      font-size: 0.88rem;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      display: inline-block;
    }

    .btn-outline {
      display: inline-block;
      padding: 10px 16px;
      border-radius: 6px;
      border: 1px solid var(--border-gold);
      background: rgba(212, 175, 55, 0.08);
      color: var(--gold-light);
      text-decoration: none;
      font-weight: 800;
      font-size: 0.8rem;
      letter-spacing: 0.9px;
      text-transform: uppercase;
      transition: all 0.2s;
    }

    .btn-outline:hover { background: var(--gold); color: #060709; }

    ul.clean-list { list-style: none; margin-top: 10px; }
    ul.clean-list li {
      padding: 9px 0;
      border-bottom: 1px solid #1b1f27;
      font-size: 0.92rem;
      color: #d1d5db;
    }
    ul.clean-list li:last-child { border-bottom: none; }

    /* LUXURY ECOSYSTEM FOOTER SHOWCASE */
    .daz-luxury-showcase {
      width: 100%;
      padding: 46px 2.5%;
      background: linear-gradient(180deg, #060709 0%, #0e1017 50%, #060709 100%);
      border-top: 1px solid var(--border-gold);
      border-bottom: 1px solid var(--border);
    }

    .daz-luxury-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .daz-luxury-head span {
      color: var(--gold);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 1.6px;
    }

    .daz-luxury-head h2 {
      font-size: 1.5rem;
      font-weight: 900;
      text-transform: uppercase;
    }

    .daz-ad-card {
      position: relative;
      background: linear-gradient(145deg, #13161f, #090a0e);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      transition: transform 0.2s, border-color 0.2s;
    }

    .daz-ad-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--gold), var(--crimson-bright));
    }

    .daz-ad-card:hover {
      border-color: var(--gold);
      transform: translateY(-3px);
    }

    .daz-ad-card small {
      color: var(--gold);
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 8px;
      display: block;
    }

    .daz-ad-card h3 {
      font-size: 1.32rem;
      font-weight: 900;
      margin-bottom: 10px;
    }

    .daz-ad-card p {
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-bottom: 20px;
    }

    .daz-footer {
      width: 100%;
      padding: 30px 2.5%;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.84rem;
      background: #040507;
    }

    @media (max-width: 860px) {
      .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
    }
  `;

  const styleEl = document.createElement("style");
  styleEl.textContent = sharedStyles;
  document.head.appendChild(styleEl);

  const path = window.location.pathname.split("/").pop() || "index.html";

  const pages = [
    { href: "index.html", label: "Planificador Total" },
    { href: "entrenamiento.html", label: "Entrenamiento Élite" },
    { href: "nutricion.html", label: "Nutrición & Báscula" },
    { href: "suplementacion.html", label: "Suplementación Total" },
    { href: "ciencia.html", label: "Ciencia & Blog" }
  ];

  const topHTML = `
    <div class="daz-eco-bar">
      <span class="eco-title">ECOSISTEMA OFICIAL • COMMUNITY16 GROUP</span>
      <div class="daz-eco-links">
        <a href="${STORE_DPF}" target="_blank" rel="noopener">DAZ PREMIUM FIT (Ropa Deportiva & Suplementación) ↗</a>
        <a href="${STORE_DAZMOND}" target="_blank" rel="noopener">DAZMOND® (Moda & Calzado) ↗</a>
        <a href="${STORE_VALMONT}" target="_blank" rel="noopener">VALMONT & CO. (Academia Financiera) ↗</a>
      </div>
    </div>
    <header class="daz-header">
      <a href="index.html" class="daz-brand">
        <span>DAZ <span class="gold">PREMIUM FIT</span></span>
        <span class="badge-perf">PERFORMANCE</span>
        <span class="daz-health-pill" id="global-audit-badge">AUDIT SYSTEM ACTIVE</span>
      </a>
      <nav class="daz-nav">
        ${pages.map(p => `<a href="${p.href}" class="nav-link ${path === p.href ? 'active' : ''}">${p.label}</a>`).join("")}
        <a href="${STORE_DPF}" target="_blank" rel="noopener" class="nav-cta">Tienda Oficial ↗</a>
      </nav>
    </header>
  `;

  const bottomHTML = `
    <section class="daz-luxury-showcase">
      <div class="daz-luxury-head">
        <div>
          <span>PORTAFOLIO OFICIAL • MARCAS REGISTRADAS EN EE. UU.</span>
          <h2>Universo DAZ & Valmont</h2>
        </div>
        <p style="color:var(--text-muted); font-size:0.88rem;">Equipamiento deportivo de élite, moda contemporánea y educación financiera estratégica.</p>
      </div>
      <div class="grid-3">
        <div class="daz-ad-card">
          <div>
            <small>INDUMENTARIA DE CULTURISMO & SUPLEMENTACIÓN</small>
            <h3>DAZ PREMIUM FIT®</h3>
            <p>Ropa deportiva técnica diseñada para el físico atlético, cortes oversized de alto gramaje, prendas de compresión y nuestra línea esencial de nutrición deportiva.</p>
          </div>
          <a href="${STORE_DPF}" target="_blank" rel="noopener" class="btn-outline">Visitar Tienda DAZ Premium Fit ↗</a>
        </div>
        <div class="daz-ad-card">
          <div>
            <small>MODA, CALZADO & ACCESORIOS • US TRADEMARK</small>
            <h3>DAZMOND® & CO.</h3>
            <p>Estética urbana sofisticada, calzado exclusivo y accesorios diseñados con identidad propia para destacar fuera del gimnasio.</p>
          </div>
          <a href="${STORE_DAZMOND}" target="_blank" rel="noopener" class="btn-outline">Explorar Colección DAZMOND® ↗</a>
        </div>
        <div class="daz-ad-card">
          <div>
            <small>ACADEMIA DE INVERSIÓN & MERCADOS GLOBALES</small>
            <h3>VALMONT & CO.</h3>
            <p>Formación financiera avanzada, protocolos de inversión bursátil e inmobiliaria y análisis estratégico de capital liderados por Ivan J. Valmont.</p>
          </div>
          <a href="${STORE_VALMONT}" target="_blank" rel="noopener" class="btn-outline">Acceder a Valmont & Co. ↗</a>
        </div>
      </div>
    </section>
    <footer class="daz-footer">
      <p><strong>DAZ PREMIUM FIT PERFORMANCE</strong> • División Científica de <a href="${STORE_DPF}" target="_blank" style="color:var(--gold); text-decoration:none;">DAZ Premium Fit®</a></p>
      <p id="global-audit-footer" style="margin-top:6px; font-size:0.78rem;">Verificando huellas digitales del sistema...</p>
    </footer>
  `;

  document.body.insertAdjacentHTML("afterbegin", topHTML);
  document.body.insertAdjacentHTML("beforeend", bottomHTML);

  fetch("data/revision.json")
    .then(r => r.json())
    .then(rev => {
      const badge = document.getElementById("global-audit-badge");
      const footer = document.getElementById("global-audit-footer");
      if (badge) badge.textContent = `REVISIÓN: ${rev.estado} • ${rev.archivos_verificados} JSON`;
      if (footer) footer.textContent = `Última auditoría con huellas SHA-256: ${rev.fecha_utc} • Integridad: ${rev.estado}`;
    })
    .catch(() => {});
})();
