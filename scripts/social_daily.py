"""DAZ Performance · Publicación diaria automática para redes.

Cada día crea:
- social/img/AAAA-MM-DD.jpg       (cuadrada 1080x1080: Instagram, Facebook, Threads)
- social/img/AAAA-MM-DD-pin.jpg   (vertical 1000x1500: Pinterest, historias)
- social/posts.json               (texto listo para copiar y pegar en cada red)
- social/feed.xml                 (feed RSS: Pinterest y otras webs lo publican solas)
Todas las imágenes llevan el logo y venden la suscripción Premium.
Solo usa Pillow (gratis).
"""
import datetime
import json
import os
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = "https://dazperformance.com"
PREMIUM = f"{SITE}/premium.html"
OUT = "social"
KEEP_DAYS = 30
F_IT = "assets/fonts/Montserrat-Italic.ttf"
F_RG = "assets/fonts/Montserrat.ttf"
RED, GOLD, WHITE, GREY = (230, 30, 30), (214, 175, 60), (245, 245, 247), (175, 175, 182)

# Biblioteca de publicaciones (rota cada día). kicker · título · texto o lista · pie de foto.
POSTS = [
    ("NUEVO · PACKS DAZ PERFORMANCE", "ELIGE TU PACK", None,
     ["Entrenamiento · 2,99 €/mes", "Nutrición · 2,99 €/mes", "Suplementos · 1,99 €/mes", "Completo (los 3) · 4,99 €/mes"],
     "Paga solo por lo que necesitas o llévate los 3 con el Pack Completo y ahorra 2,98 € al mes 👉"),
    ("PACK ENTRENAMIENTO · 2,99 €/MES", "TODAS LAS RUTINAS + TU SESIÓN DIARIA", None,
     ["Volumen, fuerza y definición", "Tu sesión exacta cada mañana", "Plan de recuperación en descanso", "7 días gratis para probar"],
     "Tu entrenador en Telegram por 2,99 €/mes. Pruébalo 7 días gratis 👉"),
    ("PACK NUTRICIÓN · 2,99 €/MES", "TU MENÚ EN GRAMOS CADA DÍA", None,
     ["Calorías calculadas con tu peso", "Proteína, hidratos y grasas", "Volumen, definición o recomposición", "Cada mañana en Telegram"],
     "Deja de adivinar qué comer: tu menú y tus macros en gramos por 2,99 €/mes 👉"),
    ("PACK SUPLEMENTOS · 1,99 €/MES", "SOLO LO QUE FUNCIONA, BIEN DOSIFICADO", None,
     ["Creatina, proteína, cafeína y vitamina D", "Dosis según tu peso", "Horario exacto cada día", "Con base científica"],
     "Ni humo ni gasto inútil: tu stack de suplementos con dosis y horario por 1,99 €/mes 👉"),
    ("PACK COMPLETO · 4,99 €/MES", "LOS 3 PACKS POR MENOS", None,
     ["Entrenamiento + Nutrición + Suplementos", "Planificador total sin límites", "Todo tu plan cada mañana", "Ahorras 2,98 € al mes"],
     "El pack más elegido: entrenamiento, nutrición y suplementos por 4,99 €/mes 👉"),
    ("NUEVO · DAZ PERFORMANCE", "TU ENTRENADOR PERSONAL EN TELEGRAM",
     "Dinos tu peso, tu objetivo y tus días de entreno. Cada mañana recibes tu sesión exacta.", None,
     "Tu entrenador personal, en tu móvil, cada mañana. Configura tu perfil en 1 minuto 👉"),
    ("CADA MAÑANA A LAS 7:00", "TU SESIÓN EXACTA, SIN PENSAR", None,
     ["Ejercicios, series y descansos", "Hecha para 3, 4, 5 o 6 días", "Plan de recuperación en descanso", "Calorías y macros del día"],
     "Abre Telegram y entrena. Nosotros pensamos por ti 💪"),
    ("NUTRICIÓN CON CIENCIA", "TU MENÚ EN GRAMOS PARA TU OBJETIVO",
     "Volumen, definición o recomposición: calorías y macros calculados para ti.", None,
     "Deja de adivinar qué comer. Menú en gramos para tu objetivo 🍽️"),
    ("MITO VS. CIENCIA", "CREATINA: 3–5 g AL DÍA",
     "Todos los días, también en descanso. Es el suplemento con más evidencia científica.", None,
     "La creatina no necesita fase de carga ni dosis gigantes. 3–5 g al día y constancia."),
    ("¿QUÉ INCLUYE?", "GRATIS VS PREMIUM", None,
     ["Gratis: canal diario y calculadoras", "Premium: todas las rutinas", "Premium: menú en gramos", "Premium: suplementos a tu medida", "Cancela cuando quieras"],
     "Empieza gratis. Pásate a Premium cuando quieras ir en serio ⭐"),
    ("PREMIUM · 4,99 €/MES", "MENOS QUE UN BATIDO AL MES",
     "Entrenamiento, nutrición y suplementación con base científica en tu móvil.", None,
     "Por menos de lo que cuesta un batido, tienes un plan completo cada día."),
    ("PROTEÍNA", "1,6–2,2 g POR KILO AL DÍA",
     "Repártela en 3–5 tomas de 25–40 g. Así maximizas la ganancia muscular.", None,
     "¿Cuánta proteína necesitas? Te lo calculamos con tu peso exacto."),
    ("HIPERTROFIA", "10–20 SERIES POR MÚSCULO A LA SEMANA",
     "Ese es el rango donde más crece el músculo según los estudios.", None,
     "Más no siempre es mejor. Nuestras rutinas están dentro del rango óptimo."),
    ("DESCANSO", "EL MÚSCULO CRECE CUANDO DESCANSAS",
     "Duerme 7–9 horas. Camina 8.000 pasos. Los días de descanso también tienen plan.", None,
     "Tu plan de recuperación también llega cada mañana a Telegram 😴"),
    ("DEFINICIÓN", "PIERDE GRASA SIN PERDER MÚSCULO", None,
     ["Déficit moderado: 300–500 kcal", "Proteína alta: 2 g por kilo", "Mantén el peso en la barra", "Pasos diarios: 8.000–10.000"],
     "Definir bien es mantener la fuerza. Te damos las cifras exactas."),
    ("VOLUMEN LIMPIO", "GANA MÚSCULO, NO GRASA", None,
     ["Superávit pequeño: 200–300 kcal", "Progresión de cargas cada semana", "Proteína en cada comida", "Mide tu peso 3 veces por semana"],
     "Un volumen limpio se planifica. Hazlo con números reales."),
    ("PROGRAMAS", "ELIGE TU PROGRAMA", None,
     ["Push / Pull / Legs · 6 días", "Torso / Pierna · 4 días", "Full Body · 3 días", "Brazos y Hombros · 5 días", "Pierna y Glúteo · 5 días"],
     "Elige los días que puedes entrenar y recibe la rutina de cada día."),
    ("SUPLEMENTOS", "LO QUE SÍ FUNCIONA", None,
     ["Creatina monohidrato", "Proteína whey", "Cafeína antes de entrenar", "Vitamina D si te falta sol"],
     "Ni humo ni promesas: solo suplementos con evidencia científica."),
    ("TU PROGRESO", "SOBRECARGA PROGRESIVA",
     "Si cada semana subes un poco el peso o las repeticiones, creces. Así de simple.", None,
     "Apunta, progresa, repite. Tu sesión diaria te dice qué hacer."),
]
HASHTAGS = "#DAZPerformance #fitness #gym #entrenamiento #nutricion #hipertrofia #culturismo #suplementos #gymmotivation #vidasana"


def font(size, weight=900, italic=True):
    f = ImageFont.truetype(F_IT if italic else F_RG, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def background(W, H):
    im = Image.new("RGB", (W, H), (8, 8, 9))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((W * 0.1, -H * 0.15, W * 0.9, H * 0.45), fill=(90, 10, 10))
    d.ellipse((W * 0.35, H * 0.7, W * 1.2, H * 1.3), fill=(60, 45, 8))
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(W // 6)), 0.55)
    d = ImageDraw.Draw(im)
    for i in range(-H, W, 46):
        d.line((i, H, i + H * 0.35, 0), fill=(16, 16, 18), width=2)
    return im


def wrap(d, text, f, maxw):
    lines, line = [], ""
    for w in text.split(" "):
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            line = t
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def center(d, y, text, f, fill, W):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)
    b = f.getbbox("Ag")
    return y + (b[3] - b[1]) + int(f.size * 0.28)


def render(path, kicker, title, body, bullets, W, H):
    im = background(W, H)
    d = ImageDraw.Draw(im)
    logo = Image.open("assets/logo-transparent.png").convert("RGBA")
    ls = int(W * 0.24) if H == W else int(W * 0.32)
    logo = logo.resize((ls, ls), Image.LANCZOS)
    top = int(H * 0.04) if H == W else int(H * 0.06)
    im.paste(logo, ((W - ls) // 2, top), logo)
    y = top + ls + int(H * 0.015)
    y = center(d, y, kicker, font(30, 800), GOLD, W) + 6
    tf = font(84 if H == W else 92, 900)
    for line in wrap(d, title, tf, W * 0.88):
        y = center(d, y, line, tf, WHITE, W)
    d.rectangle(((W - 160) / 2, y + 16, (W + 160) / 2, y + 22), fill=RED)
    y += 46
    if bullets:
        bf = font(36, 700, False)
        for b in bullets:
            for i, line in enumerate(wrap(d, b, bf, W * 0.76)):
                x = W * 0.13
                if i == 0:
                    d.ellipse((x - 6, y + 14, x + 10, y + 30), fill=GOLD)
                d.text((x + 30, y), line, font=bf, fill=WHITE)
                y += 50
            y += 6
    else:
        bf = font(36, 600, False)
        for line in wrap(d, body, bf, W * 0.82):
            y = center(d, y, line, bf, GREY, W)
    bh = int(H * 0.105) if H == W else int(H * 0.075)
    by = H - bh - int(H * 0.045)
    d.rounded_rectangle((W * 0.08, by, W * 0.92, by + bh), radius=bh // 2, fill=RED)
    cf = font(40, 900)
    t = "PACKS DESDE 1,99 €/MES  ·  dazperformance.com"
    if d.textlength(t, font=cf) > W * 0.8:
        cf = font(32, 900)
    bb = cf.getbbox(t)
    d.text(((W - d.textlength(t, font=cf)) / 2, by + (bh - (bb[3] - bb[1])) / 2 - bb[1]), t, font=cf, fill=WHITE)
    im.save(path, quality=90, optimize=True)


def build_feed(posts):
    items = []
    for p in posts[:KEEP_DAYS]:
        pub = datetime.datetime.fromisoformat(p["date"] + "T07:00:00+00:00").strftime("%a, %d %b %Y %H:%M:%S +0000")
        items.append(
            "<item>"
            f"<title>{escape(p['title'])}</title>"
            f"<link>{escape(p['link'])}</link>"
            f"<guid isPermaLink=\"false\">daz-{p['date']}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{escape(p['caption'])}</description>"
            f"<enclosure url=\"{escape(p['image_pin'])}\" type=\"image/jpeg\" length=\"0\"/>"
            f"<media:content url=\"{escape(p['image_pin'])}\" medium=\"image\" type=\"image/jpeg\"/>"
            "</item>"
        )
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        "<title>DAZ Performance · Entrenamiento, nutrición y suplementos</title>"
        f"<link>{SITE}</link>"
        f'<atom:link href="{SITE}/social/feed.xml" rel="self" type="application/rss+xml"/>'
        "<description>Consejos diarios de entrenamiento y nutrición con base científica. Premium 4,99 €/mes.</description>"
        f"<language>es</language><lastBuildDate>{now}</lastBuildDate>"
        f"<image><url>{SITE}/assets/logo-512.png</url><title>DAZ Performance</title><link>{SITE}</link></image>"
        + "".join(items)
        + "</channel></rss>\n"
    )


def run():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    day = today.isoformat()
    os.makedirs(f"{OUT}/img", exist_ok=True)
    kicker, title, body, bullets, lead = POSTS[today.toordinal() % len(POSTS)]
    sq, pin = f"{OUT}/img/{day}.jpg", f"{OUT}/img/{day}-pin.jpg"
    render(sq, kicker, title, body, bullets, 1080, 1080)
    render(pin, kicker, title, body, bullets, 1000, 1500)
    link = f"{PREMIUM}?utm_source=social&utm_medium=post&utm_campaign={day}"
    caption = f"{title.capitalize()}\n\n{lead}\n\n⭐ Packs desde 1,99 €/mes · 7 días gratis · {PREMIUM}\n\n{HASHTAGS}"

    path = f"{OUT}/posts.json"
    posts = []
    if os.path.exists(path):
        try:
            posts = json.load(open(path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            posts = []
    posts = [p for p in posts if p.get("date") != day]
    posts.insert(0, {
        "date": day, "title": title, "caption": caption, "link": link,
        "image": f"{SITE}/{sq}", "image_pin": f"{SITE}/{pin}",
    })
    posts = posts[:KEEP_DAYS]
    json.dump(posts, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(f"{OUT}/feed.xml", "w", encoding="utf-8").write(build_feed(posts))

    keep = {p["date"] for p in posts}
    for f in os.listdir(f"{OUT}/img"):
        if f[:10] not in keep:
            os.remove(f"{OUT}/img/{f}")
    print(f"[SOCIAL] {day}: {title}")


if __name__ == "__main__":
    run()
