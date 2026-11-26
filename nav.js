(function () {
  const STORE_DPF = "https://dazpremiumfit.com";
  const STORE_DAZMOND = "https://dazmond.com";
  const STORE_VALMONT = "https://valmontco.com";

  const I18N = {
    es: {
      nav_planner: "Planificador Total",
      nav_training: "Entrenamiento Élite",
      nav_nutrition: "Nutrición & Báscula",
      nav_supps: "Suplementación",
      nav_blog: "Ciencia & Blog",
      nav_profile: "Mi Cuenta & Telegram",
      nav_shop: "Tienda Oficial ↗",
      eco_title: "ECOSISTEMA OFICIAL • COMMUNITY16 GROUP",
      eco_dpf: "DAZ PREMIUM FIT (Ropa Deportiva & Suplementación) ↗",
      eco_daz: "DAZMOND® (Moda & Calzado) ↗",
      eco_val: "VALMONT & CO. (Academia Financiera) ↗",
      univ_kicker: "PORTAFOLIO OFICIAL • MARCAS REGISTRADAS EN EE. UU.",
      univ_title: "Universo DAZ & Valmont"
    },
    en: {
      nav_planner: "Total Planner",
      nav_training: "Elite Training",
      nav_nutrition: "Nutrition & Scale",
      nav_supps: "Supplements",
      nav_blog: "Science & Blog",
      nav_profile: "My Account & Telegram",
      nav_shop: "Official Store ↗",
      eco_title: "OFFICIAL ECOSYSTEM • COMMUNITY16 GROUP",
      eco_dpf: "DAZ PREMIUM FIT (Bodybuilding Apparel & Supplements) ↗",
      eco_daz: "DAZMOND® (Fashion & Footwear) ↗",
      eco_val: "VALMONT & CO. (Financial Academy) ↗",
      univ_kicker: "OFFICIAL PORTFOLIO • U.S. REGISTERED TRADEMARKS",
      univ_title: "DAZ & Valmont Universe"
    }
  };

  let currentLang = localStorage.getItem("daz_lang") || "es";

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
    .daz-eco-bar .eco-title { color: var(--gold); font-weight: 800; text-transform: uppercase; }
    .daz-eco-links { display: flex; gap: 20px; flex-wrap: wrap; }
    .daz-eco-links a { color: #e5e7eb; text-decoration: none; font-weight: 600; transition: color 0.2s; }
    .daz-eco-links a:hover { color: var(--gold-light); }

    .daz-header {
      position: sticky;
      top: 0;
      z-index: 999;
      width: 100%;
      background: rgba(6, 7, 9, 0.96);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      padding: 13px 2.5%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .daz-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: #fff;
      font-weight: 900;
      font-size: 1.12rem;
      letter-spacing: 1.6px;
      text-transform: uppercase;
    }
    .daz-brand { display: inline-flex; align-items: center; gap: 10px; }
    .daz-brand-logo { width: 38px; height: 38px; border-radius: 8px; object-fit: cover; }
    .daz-brand span.gold { color: var(--gold); }
    .daz-brand span.badge-perf {
      background: var(--crimson);
      color: #fff;
      font-size: 0.68rem;
      padding: 2px 8px;
      border-radius: 3px;
      letter-spacing: 1.8px;
    }
    .daz-nav { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .daz-nav a.nav-link {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 700;
      padding: 7px 12px;
      border-radius: 6px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }
    .daz-nav a.nav-link:hover, .daz-nav a.nav-link.active {
      color: var(--gold);
      background: var(--gold-soft);
      border-color: var(--border-gold);
    }
    .lang-switch {
      background: #11141c;
      border: 1px solid var(--border-gold);
      color: var(--gold-light);
      padding: 6px 10px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 0.78rem;
      cursor: pointer;
    }
    .daz-nav a.nav-cta {
      background: linear-gradient(135deg, var(--gold-light), var(--gold), #a67c1e);
      color: #060709;
      font-weight: 900;
      font-size: 0.8rem;
      padding: 8px 15px;
      border-radius: 6px;
      text-decoration: none;
      letter-spacing: 0.7px;
      text-transform: uppercase;
    }
    .daz-container { width: 100%; padding: 36px 2.5% 60px; }
    .daz-page-banner {
      width: 100%;
      padding: 40px 2.5%;
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
      font-size: clamp(1.85rem, 3.2vw, 2.85rem);
      font-weight: 900;
      text-transform: uppercase;
      line-height: 1.1;
      margin-bottom: 10px;
    }
    .daz-page-banner p { color: var(--text-muted); font-size: 1.02rem; max-width: 850px; }

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

    /* PUBLICIDAD EDITORIAL CON FOTOGRAFÍA DE LUJO */
    .daz-luxury-showcase {
      width: 100%;
      padding: 50px 2.5%;
      background: linear-gradient(180deg, #060709 0%, #0e1017 50%, #060709 100%);
      border-top: 1px solid var(--border-gold);
      border-bottom: 1px solid var(--border);
    }
    .daz-luxury-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 26px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .daz-luxury-head span { color: var(--gold); font-size: 0.78rem; font-weight: 800; letter-spacing: 1.6px; }
    .daz-luxury-head h2 { font-size: 1.55rem; font-weight: 900; text-transform: uppercase; }
    .daz-ad-card {
      position: relative;
      background: linear-gradient(145deg, #13161f, #090a0e);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s, border-color 0.25s;
    }
    .daz-ad-card:hover { border-color: var(--gold); transform: translateY(-4px); }
    .daz-ad-img-wrap {
      position: relative;
      width: 100%;
      height: 220px;
      overflow: hidden;
      border-bottom: 1px solid var(--border-gold);
    }
    .daz-ad-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: contrast(1.08) brightness(0.85);
      transition: transform 0.4s ease;
    }
    .daz-ad-card:hover .daz-ad-img-wrap img { transform: scale(1.05); }
    .daz-ad-img-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, transparent 35%, rgba(9, 10, 14, 0.95) 100%);
    }
    .daz-ad-body {
      padding: 22px 24px 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex: 1;
    }
    .daz-ad-body small { color: var(--gold); font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px; display: block; }
    .daz-ad-body h3 { font-size: 1.32rem; font-weight: 900; margin-bottom: 10px; }
    .daz-ad-body p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px; }

    .daz-footer {
      width: 100%;
      padding: 28px 2.5%;
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
  const t = I18N[currentLang];

  const pages = [
    { href: "index.html", label: t.nav_planner },
    { href: "entrenamiento.html", label: t.nav_training },
    { href: "nutricion.html", label: t.nav_nutrition },
    { href: "suplementacion.html", label: t.nav_supps },
    { href: "ciencia.html", label: t.nav_blog },
    { href: "perfil.html", label: t.nav_profile },
    { href: "premium.html", label: "⭐ Premium" }
  ];

  const topHTML = `
    <div class="daz-eco-bar">
      <span class="eco-title">${t.eco_title}</span>
      <div class="daz-eco-links">
        <a href="${STORE_DPF}" target="_blank" rel="noopener">${t.eco_dpf}</a>
        <a href="${STORE_DAZMOND}" target="_blank" rel="noopener">${t.eco_daz}</a>
        <a href="${STORE_VALMONT}" target="_blank" rel="noopener">${t.eco_val}</a>
      </div>
    </div>
    <header class="daz-header">
      <a href="index.html" class="daz-brand"><img class="daz-brand-logo" src="assets/logo-192.png" alt="DAZ Premium Fit" width="38" height="38" />
        <span>DAZ <span class="gold">PERFORMANCE</span></span>
      </a>
      <nav class="daz-nav">
        ${pages.map(p => `<a href="${p.href}" class="nav-link ${path === p.href ? 'active' : ''}">${p.label}</a>`).join("")}
        <button class="lang-switch" onclick="toggleDazLang()">${currentLang === "es" ? "🇺🇸 EN (USA)" : "🇪🇸 ES"}</button>
        <a href="${STORE_DPF}" target="_blank" rel="noopener" class="nav-cta">${t.nav_shop}</a>
      </nav>
    </header>
  `;

  const bottomHTML = `
    <section class="daz-luxury-showcase">
      <div class="daz-luxury-head">
        <div>
          <span>${t.univ_kicker}</span>
          <h2>${t.univ_title}</h2>
        </div>
      </div>
      <div class="grid-3">
        <div class="daz-ad-card">
          <div class="daz-ad-img-wrap">
            <img src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=900&q=80" alt="DAZ Premium Fit Bodybuilding Apparel" loading="lazy" />
            <div class="daz-ad-img-overlay"></div>
          </div>
          <div class="daz-ad-body">
            <div>
              <small>BODYBUILDING APPAREL & SUPPLEMENTS</small>
              <h3>DAZ PREMIUM FIT®</h3>
              <p>${currentLang === "en" ? "Engineered bodybuilding apparel, heavyweight pump tees, compression gear, and clinical-grade essentials." : "Ropa deportiva técnica diseñada para el físico atlético, cortes oversized de alto gramaje, prendas de compresión y suplementación esencial."}</p>
            </div>
            <a href="${STORE_DPF}" target="_blank" rel="noopener" class="btn-outline">${currentLang === "en" ? "Shop DAZ Premium Fit ↗" : "Visitar Tienda DAZ Premium Fit ↗"}</a>
          </div>
        </div>
        <div class="daz-ad-card">
          <div class="daz-ad-img-wrap">
            <img src="https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80" alt="DAZMOND Luxury Fashion" loading="lazy" />
            <div class="daz-ad-img-overlay"></div>
          </div>
          <div class="daz-ad-body">
            <div>
              <small>FASHION, FOOTWEAR & ACCESSORIES • US TRADEMARK</small>
              <h3>DAZMOND® & CO.</h3>
              <p>${currentLang === "en" ? "Contemporary luxury streetwear, exclusive footwear, and signature accessories." : "Estética urbana sofisticada, calzado exclusivo y accesorios diseñados con identidad propia para destacar fuera del gimnasio."}</p>
            </div>
            <a href="${STORE_DAZMOND}" target="_blank" rel="noopener" class="btn-outline">${currentLang === "en" ? "Explore DAZMOND® ↗" : "Explorar Colección DAZMOND® ↗"}</a>
          </div>
        </div>
        <div class="daz-ad-card">
          <div class="daz-ad-img-wrap">
            <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=900&q=80" alt="Valmont & Co Financial Academy" loading="lazy" />
            <div class="daz-ad-img-overlay"></div>
          </div>
          <div class="daz-ad-body">
            <div>
              <small>GLOBAL MARKETS & INVESTMENT ACADEMY</small>
              <h3>VALMONT & CO.</h3>
              <p>${currentLang === "en" ? "Advanced financial education, equity & real estate protocols led by Ivan J. Valmont." : "Formación financiera avanzada, protocolos de inversión bursátil e inmobiliaria liderados por Ivan J. Valmont."}</p>
            </div>
            <a href="${STORE_VALMONT}" target="_blank" rel="noopener" class="btn-outline">${currentLang === "en" ? "Access Valmont & Co. ↗" : "Acceder a Valmont & Co. ↗"}</a>
          </div>
        </div>
      </div>
    </section>
    <footer class="daz-footer">
      <p><strong>DAZ PREMIUM FIT PERFORMANCE</strong> • División Científica de <a href="${STORE_DPF}" target="_blank" style="color:var(--gold); text-decoration:none;">DAZ Premium Fit®</a> • Community16 LLC</p>
    </footer>
  `;

  document.body.insertAdjacentHTML("afterbegin", topHTML);
  document.body.insertAdjacentHTML("beforeend", bottomHTML);

  window.toggleDazLang = function () {
    const next = currentLang === "es" ? "en" : "es";
    localStorage.setItem("daz_lang", next);
    location.reload();
  };
})();
