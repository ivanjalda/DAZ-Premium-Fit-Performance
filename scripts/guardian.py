"""Guardián DAZ Performance: revisa y repara la web y Telegram varias veces al día.

- Corrige errores comunes en las páginas (dominios mal escritos, descripción para Google,
  script de autorreparación).
- Comprueba que los datos de la web (JSON) se pueden leer y que la web responde.
- Comprueba que el bot de Telegram funciona.
- Si el envío diario a los canales todavía no ha salido hoy, lo lanza él mismo.
- Avisa en privado por Telegram solo cuando ha reparado algo o hay un problema.
"""
import datetime
import glob
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request

SITE = "https://dazperformance.com"
TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
OWNER_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
UA = {"User-Agent": "Mozilla/5.0 (DAZ Guardian Bot)"}

fixes, problems = [], []


def http_ok(url: str) -> bool:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def repair_pages() -> None:
    for path in sorted(glob.glob("*.html")):
        if path.startswith("google"):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            original = f.read()
        content = original
        if "dazshopping.com" in content:
            content = content.replace("dazshopping.com", "dazpremiumfit.com")
            fixes.append(f"{path}: enlace de tienda corregido")
        # Creatina con base científica: 3-5 g al día (no 0,1 g por kilo)
        new_c = re.sub(r"\(\s*weight\s*\*\s*0\.1\s*\)\.toFixed\(1\)", "(weight >= 60 ? 5 : 3)", content)
        if new_c != content:
            content = new_c
            fixes.append(f"{path}: dosis de creatina ajustada a 3-5 g/día")
        if "<head" in content.lower() and 'name="description"' not in content.lower():
            tag = ('  <meta name="description" content="DAZ Performance: entrenamientos por objetivos, '
                   'nutrición, macros y suplementación con base científica." />\n')
            content = re.sub(r"(</head>)", tag + r"\1", content, count=1, flags=re.I)
            fixes.append(f"{path}: añadida descripción para Google")
        if "</body>" in content.lower() and "self-heal.js" not in content:
            content = re.sub(r"(</body>)", '  <script src="self-heal.js"></script>\n\\1', content, count=1, flags=re.I)
            fixes.append(f"{path}: añadida autorreparación")
        if content.count("<script") != content.count("</script>"):
            problems.append(f"{path}: hay un bloque de código sin cerrar")
        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
    for req in ["index.html", "entrenamiento.html", "nutricion.html", "suplementacion.html", "perfil.html", "nav.js"]:
        if not os.path.exists(req):
            problems.append(f"Falta la página {req}")


def check_data() -> None:
    for path in sorted(glob.glob("data/*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                json.load(f)
        except Exception as e:
            problems.append(f"{path}: datos dañados ({e.__class__.__name__})")


def check_online() -> None:
    for page in ["/", "/entrenamiento.html", "/nutricion.html", "/suplementacion.html", "/perfil.html"]:
        if not http_ok(SITE + page):
            problems.append(f"La página {page} no responde")


def check_bot() -> None:
    if not TOKEN:
        problems.append("Falta la clave del bot (TELEGRAM_TOKEN)")
        return
    if not http_ok(f"https://api.telegram.org/bot{TOKEN}/getMe"):
        problems.append("El bot de Telegram no responde")


def ensure_daily_post() -> None:
    """Si hoy (hora de España) no ha salido el entrenamiento a los canales, lo envía."""
    now_utc = datetime.datetime.utcnow()
    today = now_utc.date().isoformat()
    if now_utc.hour < 6:
        return
    status = {}
    try:
        with open("data/coach_status.json", encoding="utf-8") as f:
            status = json.load(f)
    except Exception:
        pass
    if status.get("date") == today:
        return
    result = subprocess.run(["python", "scripts/telegram_coach.py"], capture_output=True, text=True)
    if result.returncode == 0:
        fixes.append("Envío diario a los canales recuperado (no había salido a su hora)")
    else:
        problems.append("No se pudo enviar el entrenamiento diario a los canales")


SUPP_URL = "https://dazpremiumfit.com/collections/supplements"
STATUS_FILE = "data/store_status.json"


def check_supplements_store() -> None:
    """Activa los enlaces de suplementos cuando DAZ Premium Fit ya los ha publicado."""
    try:
        status = json.load(open(STATUS_FILE, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        status = {"supplements_live": False}
    live = False
    try:
        with urllib.request.urlopen(urllib.request.Request(SUPP_URL, headers=UA), timeout=20) as r:
            html = r.read().decode("utf-8", "ignore")
            live = 200 <= r.status < 300 and "/products/" in html
    except Exception:
        live = False
    if live and not status.get("supplements_live"):
        fixes.append("¡DAZ Premium Fit ya tiene los suplementos publicados! Enlaces de suplementos activados en la web")
    if bool(status.get("supplements_live")) != live:
        status["supplements_live"] = live
        status["checked"] = datetime.date.today().isoformat()
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False)


def notify() -> None:
    if not (fixes or problems) or not TOKEN or not OWNER_CHAT:
        return
    lines = ["🛡 Guardián DAZ Performance"]
    if fixes:
        lines.append("\nReparado:")
        lines += [f"✅ {x}" for x in fixes]
    if problems:
        lines.append("\nRevisar:")
        lines += [f"⚠️ {x}" for x in problems]
    data = urllib.parse.urlencode({"chat_id": OWNER_CHAT, "text": "\n".join(lines)[:3900]}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data, headers=UA), timeout=20)
    except Exception as e:
        print("[GUARDIAN] Aviso no enviado:", e)


if __name__ == "__main__":
    repair_pages()
    check_data()
    check_online()
    check_bot()
    ensure_daily_post()
    check_supplements_store()
    notify()
    print("[GUARDIAN] Reparado:", fixes or "nada")
    print("[GUARDIAN] Revisar:", problems or "nada")
