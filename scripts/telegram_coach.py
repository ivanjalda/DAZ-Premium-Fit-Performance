import datetime
import json
import os
import urllib.error
import urllib.request


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHANNEL_ES = os.environ.get("TELEGRAM_CHANNEL_ES", "").strip()
TELEGRAM_CHANNEL_EN = os.environ.get("TELEGRAM_CHANNEL_EN", "").strip()
CF_WORKER_URL = os.environ.get("CF_WORKER_URL", "").strip().rstrip("/")
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "").strip()

BRAND_WEB_DPF = "https://dazpremiumfit.com"
PAY_URL = "https://buy.stripe.com/fZueVefzC9yI0I66iq1gY2W"
PACK_LINKS = {
    "full": PAY_URL,
    "entreno": "https://buy.stripe.com/cNi3cw87acKU8ay22a1gZ0X",
    "nutricion": "https://buy.stripe.com/4gM8wQ7365is9eC5em1gZ0Y",
    "suplementos": "https://buy.stripe.com/9B614oafibGQbmKgX41gZ0Z",
}
TRIAL_DAYS = 7
OWNER_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
BRAND_WEB_DAZMOND = "https://dazmond.com"
BRAND_WEB_VALMONT = "https://valmontco.com"


ROUTINES = {
    "chest_power_a": {
        "es": {
            "program": "ESPECIALIZACIÓN PECHO & EMPUJE — BLOQUE A (TENSIÓN MECÁNICA)",
            "focus": "PECTORAL SUPERIOR, PECHO MEDIO Y TRÍCEPS",
            "duration": "62 min",
            "cue": "Escápulas retraídas y deprimidas en el banco; pausa de 1s en el punto más bajo sin rebotar.",
            "exercises": [
                ("Press Inclinado con Barra (30°)", "4 x 6-8 reps", "150s", "Énfasis en haz clavicular con control excéntrico de 3s."),
                ("Press Banca Plano con Mancuernas", "4 x 8-10 reps", "120s", "Aducción completa de mancuernas al subir sin bloquear codos."),
                ("Press en Máquina Convergente Inclinada", "3 x 10-12 reps", "90s", "Mantén tensión constante y bloquea 1s en contracción máxima."),
                ("Cruces en Polea Alta a Baja", "3 x 12-15 reps", "75s", "Cruza ligeramente las manos frente al esternón para apurar fibras."),
                ("Press Francés / Extensión Tríceps Polea", "4 x 10-12 reps", "75s", "Codos fijos a los costados; extiende por completo sin balanceo."),
            ],
        },
        "en": {
            "program": "CHEST & PUSH SPECIALIZATION — BLOCK A (MECHANICAL TENSION)",
            "focus": "UPPER CHEST, MID PECTORALS & TRICEPS",
            "duration": "62 min",
            "cue": "Retract and depress shoulder blades on the bench; 1s pause at bottom stretch without bouncing.",
            "exercises": [
                ("Incline Barbell Bench Press (30°)", "4 x 6-8 reps", "150s", "Targets upper pecs with a controlled 3s eccentric lowering phase."),
                ("Flat Dumbbell Bench Press", "4 x 8-10 reps", "120s", "Full adduction at top without locking elbows aggressively."),
                ("Incline Converging Chest Press Machine", "3 x 10-12 reps", "90s", "Keep constant tension and squeeze peak contraction for 1s."),
                ("High-to-Low Cable Flyes", "3 x 12-15 reps", "75s", "Cross wrists slightly across sternum to maximize inner-chest squeeze."),
                ("Overhead Cable Triceps Extension", "4 x 10-12 reps", "75s", "Lock upper arms in place and extend fully without torso swing."),
            ],
        },
    },
    "chest_hypertrophy_b": {
        "es": {
            "program": "ESPECIALIZACIÓN PECHO & EMPUJE — BLOQUE B (ESTIRAMIENTO & METABÓLICO)",
            "focus": "PECHO COMPLETO, DELTOIDE LATERAL Y TRÍCEPS",
            "duration": "60 min",
            "cue": "Prioriza el rango de estiramiento profundo y la calidad de contracción por encima del peso bruto.",
            "exercises": [
                ("Press Inclinado con Mancuernas (30°)", "4 x 8-10 reps", "120s", "Baja hasta sentir estiramiento seguro en pectoral superior."),
                ("Aperturas en Contractora (Pec Deck)", "4 x 12-15 reps", "75s", "Pausa de 1s en el centro apretando el pecho con firmeza."),
                ("Fondos en Paralelas Inclinados (Pecho)", "3 x 8-12 reps", "120s", "Inclina el torso hacia adelante; añade lastre si superas 12 reps."),
                ("Elevaciones Laterales en Polea Baja", "4 x 12-15 reps", "60s", "Separa la muñeca hacia afuera en arco amplio sin encoger trapecio."),
                ("Extensión de Tríceps con Cuerda en Polea", "3 x 12-15 reps", "75s", "Abre las puntas de la cuerda al final de cada repetición."),
            ],
        },
        "en": {
            "program": "CHEST & PUSH SPECIALIZATION — BLOCK B (DEEP STRETCH & METABOLIC)",
            "focus": "FULL PECTORALS, LATERAL DELTS & TRICEPS",
            "duration": "60 min",
            "cue": "Prioritize deep loaded stretch and peak contraction quality over ego loads.",
            "exercises": [
                ("Incline Dumbbell Press (30°)", "4 x 8-10 reps", "120s", "Lower under control into a deep, safe upper-chest stretch."),
                ("Pec Deck Fly Machine", "4 x 12-15 reps", "75s", "Hold a hard 1s peak squeeze at midline on every rep."),
                ("Forward-Leaning Chest Dips", "3 x 8-12 reps", "120s", "Lean torso forward to bias pecs; add weight once past 12 reps."),
                ("Single-Arm Cable Lateral Raises", "4 x 12-15 reps", "60s", "Sweep hand outward in a wide arc while keeping traps relaxed."),
                ("Cable Rope Triceps Pressdown", "3 x 12-15 reps", "75s", "Flare rope ends outward at full lockout without shoulder roll."),
            ],
        },
    },
    "pull_back": {
        "es": {
            "program": "TIRÓN & ESPALDA — DENSIDAD Y AMPLITUD",
            "focus": "DORSALES, ESPALDA ALTA Y BÍCEPS",
            "duration": "64 min",
            "cue": "Inicia cada repetición llevando los codos atrás y abajo, evitando tirar con el antebrazo.",
            "exercises": [
                ("Remo con Barra o en Máquina T-Bar", "4 x 6-8 reps", "150s", "Torso estable y tira hacia la cadera baja para grosor."),
                ("Jalón al Pecho en Polea (Agarre Neutro/Ancho)", "4 x 8-12 reps", "105s", "Lleva el pecho hacia el agarre sin balancearte hacia atrás."),
                ("Remo en Polea Baja / Máquina con Apoyo", "3 x 10-12 reps", "90s", "Aprieta escápulas 1s al final y controla el retorno."),
                ("Pullover en Polea Alta con Cuerda", "3 x 12-15 reps", "75s", "Brazos casi extendidos para aislar el dorsal ancho."),
                ("Curl de Bíceps con Barra / Mancuernas", "3 x 10-12 reps", "75s", "Evita adelantar los hombros al subir; excéntrica limpia."),
            ],
        },
        "en": {
            "program": "PULL & BACK — THICKNESS & WIDTH",
            "focus": "LATS, UPPER BACK & BICEPS",
            "duration": "64 min",
            "cue": "Initiate every rep by driving elbows down and back rather than pulling with hands.",
            "exercises": [
                ("Barbell or Chest-Supported T-Bar Row", "4 x 6-8 reps", "150s", "Keep torso braced and pull toward lower hips for back density."),
                ("Lat Pulldown (Wide or Neutral Grip)", "4 x 8-12 reps", "105s", "Pull bar to upper chest without excessive momentum."),
                ("Seated Cable or Machine Row", "3 x 10-12 reps", "90s", "Squeeze shoulder blades for 1s and control the stretch."),
                ("Straight-Arm Cable Pullover", "3 x 12-15 reps", "75s", "Keep arms nearly straight to isolate latissimus dorsi."),
                ("Barbell or Dumbbell Biceps Curl", "3 x 10-12 reps", "75s", "Keep elbows pinned and avoid rolling shoulders forward."),
            ],
        },
    },
    "legs_lower": {
        "es": {
            "program": "PIERNA COMPLETA — FUERZA & CADENA POSTERIOR",
            "focus": "CUÁDRICEPS, ISQUIOTIBIALES, GLÚTEO Y GEMELO",
            "duration": "68 min",
            "cue": "Mantén la planta del pie firme y la columna neutra; profundidad constante en cada serie.",
            "exercises": [
                ("Sentadilla Libre o Hack Squat", "4 x 6-8 reps", "180s", "Profundidad controlada y empuje uniforme con todo el pie."),
                ("Peso Muerto Rumano con Barra o Mancuernas", "4 x 8-10 reps", "150s", "Cadera atrás hasta sentir tensión en isquios sin redondear zona lumbar."),
                ("Prensa Inclinada 45°", "3 x 10-12 reps", "120s", "No despegues la zona lumbar del respaldo en el fondo."),
                ("Curl Femoral Tumbado o Sentado", "3 x 12 reps", "75s", "Contracción máxima y bajada lenta en 3 segundos."),
                ("Elevación de Talones de Pie", "4 x 12-15 reps", "60s", "Pausa de 1s abajo en estiramiento y 1s arriba."),
            ],
        },
        "en": {
            "program": "LOWER BODY — STRENGTH & POSTERIOR CHAIN",
            "focus": "QUADS, HAMSTRINGS, GLUTES & CALVES",
            "duration": "68 min",
            "cue": "Keep tripod foot pressure and neutral spine; consistent depth on every working set.",
            "exercises": [
                ("Barbell Back Squat or Hack Squat", "4 x 6-8 reps", "180s", "Controlled descent and steady drive through full foot."),
                ("Romanian Deadlift (RDL)", "4 x 8-10 reps", "150s", "Hinge hips back to hamstring stretch while keeping spine neutral."),
                ("45° Leg Press", "3 x 10-12 reps", "120s", "Keep lower back glued to pad at bottom of travel."),
                ("Lying or Seated Leg Curl", "3 x 12 reps", "75s", "Hard peak squeeze and 3s eccentric lowering."),
                ("Standing Calf Raises", "4 x 12-15 reps", "60s", "1s pause in bottom stretch and 1s at top contraction."),
            ],
        },
    },
    "upper_conditioning": {
        "es": {
            "program": "TORSO & BOMBA METABÓLICA — CIERRE DE SEMANA",
            "focus": "PECHO SUPERIOR, HOMBROS, BRAZOS Y CORE",
            "duration": "55 min",
            "cue": "Ritmo ágil con descansos medidos para acumular volumen efectivo sin perder técnica.",
            "exercises": [
                ("Press Inclinado en Smith o Multipower", "3 x 8-10 reps", "120s", "Alinea el banco justo bajo el punto de máximo estímulo pectoral."),
                ("Press Militar / Hombro en Máquina", "3 x 8-12 reps", "105s", "Sube sin hiperextender la zona lumbar."),
                ("Cruces en Polea Media / Aperturas", "3 x 12-15 reps", "75s", "Enfoque en cierre pectoral con tensión continua."),
                ("Superserie Bíceps Polea + Tríceps Polea", "3 x 12-15 reps", "75s", "Ejecución limpia alternando ambos grupos."),
                ("Elevación de Piernas o Crunch en Polea", "3 x 15 reps", "60s", "Flexión vertebral controlada, sin tirones de cadera."),
            ],
        },
        "en": {
            "program": "UPPER & METABOLIC PUMP — WEEKLY FINISHER",
            "focus": "UPPER CHEST, SHOULDERS, ARMS & CORE",
            "duration": "55 min",
            "cue": "Crisp pacing with disciplined rest periods to build quality volume cleanly.",
            "exercises": [
                ("Smith Machine Incline Press", "3 x 8-10 reps", "120s", "Position bench cleanly under upper-chest line of drive."),
                ("Shoulder Press (Machine or Dumbbell)", "3 x 8-12 reps", "105s", "Press overhead without arching lower back."),
                ("Mid-Cable Flyes or Chest Press Finisher", "3 x 12-15 reps", "75s", "Focus on smooth arc and constant pec tension."),
                ("Superset: Cable Curl + Cable Triceps", "3 x 12-15 reps", "75s", "Controlled tempo alternating biceps and triceps."),
                ("Hanging Leg Raise or Cable Crunch", "3 x 15 reps", "60s", "Curl pelvis/ribcage smoothly without hip-flexor yank."),
            ],
        },
    },
}


# Calendario semanal por programa (lunes=0 ... domingo=6). None = día de descanso.
SPLIT_SCHEDULES = {
    "ppl6": ["chest_power_a", "pull_back", "legs_lower", "chest_hypertrophy_b", "pull_back", "legs_lower", None],
    "ul4": ["upper_conditioning", "legs_lower", None, "chest_hypertrophy_b", "legs_lower", None, None],
    "fb3": ["upper_conditioning", None, "legs_lower", None, "chest_power_a", None, None],
    "spec_arms": ["upper_conditioning", "legs_lower", "chest_hypertrophy_b", "pull_back", "upper_conditioning", None, None],
    "spec_legs": ["legs_lower", "upper_conditioning", "legs_lower", "pull_back", "legs_lower", None, None],
}

GOAL_KCAL_PER_KG = {"volumen": 35, "definicion": 26, "recomposicion": 30}


def daily_macros(weight_kg: float, goal: str) -> tuple[int, int, int, int]:
    """Devuelve kcal, proteína, carbohidratos y grasas (g) orientativos."""
    w = max(40.0, min(220.0, float(weight_kg or 80)))
    kcal = int(round(w * GOAL_KCAL_PER_KG.get(str(goal).lower(), 32) / 50.0) * 50)
    protein = int(round(w * 2.0))
    fat = int(round(w * 0.9))
    carbs = max(50, int(round((kcal - protein * 4 - fat * 9) / 4)))
    return kcal, protein, carbs, fat


def supplements_live() -> bool:
    """True cuando DAZ Premium Fit ya ha publicado sus suplementos (lo marca guardian.py)."""
    try:
        with open("data/store_status.json", encoding="utf-8") as f:
            return bool(json.load(f).get("supplements_live"))
    except (OSError, ValueError):
        return False


def supplement_lines(lang: str, weight_kg: float, goal: str, training_day: bool) -> list[str]:
    """Stack con evidencia científica (ISSN): creatina, proteína, cafeína y vitamina D."""
    w = max(40.0, min(220.0, float(weight_kg or 80)))
    creat = 5 if w >= 60 else 3
    caf = min(400, int(round(w * 3 / 10.0) * 10))
    _, prot, _, _ = daily_macros(w, goal)
    whey = 30 if prot - 120 < 40 else 40
    en = str(lang).lower().startswith("en")
    out = [f"💊 Creatine monohydrate {creat} g (any time, every day)" if en
           else f"💊 Creatina monohidrato {creat} g (a cualquier hora, todos los días)"]
    out.append(f"💊 Whey {whey} g if you don't reach {prot} g of protein with food" if en
               else f"💊 Proteína whey {whey} g si no llegas a {prot} g de proteína con la comida")
    if training_day:
        out.append(f"💊 Caffeine {caf} mg 30-60 min before training (not after 16:00)" if en
                   else f"💊 Cafeína {caf} mg 30-60 min antes de entrenar (no después de las 16:00)")
    out.append("💊 Vitamin D 1000-2000 IU with a meal if you get little sun" if en
               else "💊 Vitamina D 1000-2000 UI con una comida si te da poco el sol")
    return out


def build_rest_message(lang: str, name: str, weight_kg: float, goal: str) -> str:
    lang = "en" if str(lang).lower().startswith("en") else "es"
    idx = datetime.datetime.now(datetime.timezone.utc).weekday()
    day_label, default_name = get_day_labels(lang, idx)
    who = (name or "").strip() or default_name
    kcal, p, c, f = daily_macros(weight_kg, goal)
    if lang == "en":
        return "\n".join([
            f"🧘 DAZ PERFORMANCE — {day_label} · RECOVERY DAY",
            f"👤 {who}: muscles grow while you rest. Today:",
            "1️⃣ 8,000–10,000 steps or 30 min easy walk",
            "2️⃣ 10 min mobility: hips, thoracic spine, shoulders",
            "3️⃣ 7–9 h of sleep tonight",
            "",
            f"🍽️ Today's target: ~{kcal} kcal · P {p} g · C {c} g · F {f} g",
            f"💊 Creatine {5 if float(weight_kg or 80) >= 60 else 3} g (also on rest days)",
        ])
    return "\n".join([
        f"🧘 DAZ PERFORMANCE — {day_label} · DÍA DE RECUPERACIÓN",
        f"👤 {who}: el músculo crece mientras descansas. Hoy:",
        "1️⃣ 8.000–10.000 pasos o 30 min de paseo suave",
        "2️⃣ 10 min de movilidad: cadera, espalda alta y hombros",
        "3️⃣ Dormir 7–9 horas esta noche",
        "",
        f"🍽️ Objetivo de hoy: ~{kcal} kcal · P {p} g · H {c} g · G {f} g",
        f"💊 Creatina {5 if float(weight_kg or 80) >= 60 else 3} g (también en descanso)",
    ])


WEEKLY_ROTATION = [
    "chest_power_a",
    "pull_back",
    "legs_lower",
    "chest_hypertrophy_b",
    "upper_conditioning",
    "chest_power_a",
    "legs_lower",
]


def get_day_labels(lang: str, weekday_idx: int) -> tuple[str, str]:
    days_es = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
    days_en = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    if lang == "en":
        return days_en[weekday_idx], "DAZ Athlete"
    return days_es[weekday_idx], "Atleta DAZ"


def build_workout_message(
    lang: str = "es",
    name: str = "",
    weight_kg: float = 88.0,
    goal: str = "volumen",
    routine_key: str | None = None,
) -> str:
    lang = "en" if str(lang).lower().startswith("en") else "es"
    now = datetime.datetime.now(datetime.timezone.utc)
    weekday_idx = now.weekday()
    selected_key = routine_key or WEEKLY_ROTATION[weekday_idx]
    routine = ROUTINES.get(selected_key, ROUTINES["chest_power_a"])[lang]

    day_label, default_name = get_day_labels(lang, weekday_idx)
    athlete_name = (name or "").strip() or default_name
    safe_weight = max(40.0, min(220.0, float(weight_kg or 88.0)))
    creatine_g = 5 if safe_weight >= 60 else 3  # dosis estándar 3-5 g/día (ISSN)
    protein_g = int(round(safe_weight * 2.0))

    lines = []
    if lang == "en":
        goal_map = {
            "volumen": "Lean Bulk / Hypertrophy",
            "definicion": "Fat Loss / Conditioning",
            "recomposicion": "Body Recomposition",
        }
        goal_label = goal_map.get(str(goal).lower(), "Performance & Hypertrophy")
        lines.append(f"🔥 DAZ PERFORMANCE — {day_label} PROTOCOL")
        lines.append(f"👤 Athlete: {athlete_name} | 🎯 Goal: {goal_label} | ⏱️ {routine['duration']}")
        lines.append(f"📋 {routine['program']}")
        lines.append(f"🎯 Target: {routine['focus']}")
        lines.append(f"💡 Execution Cue: {routine['cue']}")
        lines.append("")
        for idx, (ex_name, sets_reps, rest, note) in enumerate(routine["exercises"], start=1):
            lines.append(f"{idx}️⃣ {ex_name}")
            lines.append(f"   • {sets_reps} | Rest: {rest}")
            lines.append(f"   • Note: {note}")
        lines.append("")
        kcal, _p, carbs_g, fat_g = daily_macros(safe_weight, goal)
        lines.append(f"🍽️ Today: ~{kcal} kcal · P {protein_g} g · C {carbs_g} g · F {fat_g} g")
        lines.append(f"💊 Creatine ~{creatine_g}g")
        lines.append(f"🛒 Sportswear & supplements (coming soon): {BRAND_WEB_DPF}" if not supplements_live()
                     else f"🛒 Gear & Supplements: {BRAND_WEB_DPF}")
        lines.append(f"🖤 DAZMOND®: {BRAND_WEB_DAZMOND} | 📈 Valmont & Co.: {BRAND_WEB_VALMONT}")
    else:
        goal_map = {
            "volumen": "Volumen Limpio / Hipertrofia",
            "definicion": "Definición / Pérdida de Grasa",
            "recomposicion": "Recomposición Corporal",
        }
        goal_label = goal_map.get(str(goal).lower(), "Rendimiento e Hipertrofia")
        lines.append(f"🔥 DAZ PERFORMANCE — PROTOCOLO DEL {day_label}")
        lines.append(f"👤 Atleta: {athlete_name} | 🎯 Objetivo: {goal_label} | ⏱️ {routine['duration']}")
        lines.append(f"📋 {routine['program']}")
        lines.append(f"🎯 Enfoque: {routine['focus']}")
        lines.append(f"💡 Clave técnica: {routine['cue']}")
        lines.append("")
        for idx, (ex_name, sets_reps, rest, note) in enumerate(routine["exercises"], start=1):
            lines.append(f"{idx}️⃣ {ex_name}")
            lines.append(f"   • {sets_reps} | Descanso: {rest}")
            lines.append(f"   • Técnica: {note}")
        lines.append("")
        kcal, _p, carbs_g, fat_g = daily_macros(safe_weight, goal)
        lines.append(f"🍽️ Hoy: ~{kcal} kcal · P {protein_g} g · H {carbs_g} g · G {fat_g} g")
        lines.append(f"💊 Creatina ~{creatine_g}g")
        lines.append(f"🛒 Ropa deportiva y suplementos (próximamente): {BRAND_WEB_DPF}" if not supplements_live()
                     else f"🛒 Ropa y Suplementos: {BRAND_WEB_DPF}")
        lines.append(f"🖤 DAZMOND®: {BRAND_WEB_DAZMOND} | 📈 Valmont & Co.: {BRAND_WEB_VALMONT}")

    return "\n".join(lines)


def send_telegram_message(chat_id: str, text: str) -> bool:
    if not TELEGRAM_TOKEN or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": str(chat_id),
            "text": text,
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (DAZ Engine Bot)"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("ok"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Telegram sendMessage failed for {chat_id}: {exc}")
        return False


def fetch_registered_users() -> list[dict]:
    if not CF_WORKER_URL or not ADMIN_SECRET:
        return []
    url = f"{CF_WORKER_URL}/subscribers"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {ADMIN_SECRET}",
            "X-Admin-Secret": ADMIN_SECRET,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (DAZ Engine Bot)",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            if isinstance(raw, list):
                return raw
            if isinstance(raw, dict) and isinstance(raw.get("users"), list):
                return raw["users"]
            return []
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[INFO] Could not fetch users from worker ({url}): {exc}")
        return []


def run() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("Missing TELEGRAM_TOKEN environment variable.")

    # 1. Envío a canales oficiales ES y EN
    if TELEGRAM_CHANNEL_ES:
        msg_es_channel = build_workout_message(
            lang="es",
            name="Comunidad DAZ",
            weight_kg=88.0,
            goal="volumen",
        )
        msg_es_channel += "\n\n⭐ DAZ Performance Premium · 4,99 €/mes\nTu entrenamiento personal cada mañana, todas las rutinas, menú en gramos y suplementos a tu medida 👉 https://dazperformance.com/premium.html"
        ok_es = send_telegram_message(TELEGRAM_CHANNEL_ES, msg_es_channel)
        print(f"[CHANNEL_ES] sent={ok_es}")

    if TELEGRAM_CHANNEL_EN:
        msg_en_channel = build_workout_message(
            lang="en",
            name="DAZ Athlete",
            weight_kg=88.0,
            goal="volumen",
        )
        msg_en_channel += "\n\n⭐ DAZ Performance Premium · 4.99 €/month\nYour personal workout every morning, every routine, meal plan in grams and custom supplements 👉 https://dazperformance.com/premium.html"
        ok_en = send_telegram_message(TELEGRAM_CHANNEL_EN, msg_en_channel)
        print(f"[CHANNEL_EN] sent={ok_en}")

    # Marca para el Guardián: el envío de hoy ya ha salido
    if locals().get("ok_es") or locals().get("ok_en"):
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/coach_status.json", "w", encoding="utf-8") as f:
                json.dump({"date": datetime.datetime.utcnow().date().isoformat(),
                           "time_utc": datetime.datetime.utcnow().strftime("%H:%M")}, f)
        except OSError as exc:
            print(f"[WARN] No se pudo guardar el estado del envío: {exc}")

    # 2. Envío personalizado a usuarios registrados en Cloudflare KV vía Worker
    users = fetch_registered_users()
    print(f"[USERS] loaded={len(users)}")
    for user in users:
        chat_id = user.get("chat_id") or user.get("telegram_id") or user.get("id")
        if not chat_id:
            continue
        u_lang = user.get("lang", "es")
        u_name = user.get("name", "")
        u_weight = user.get("weight", 88.0)
        u_goal = user.get("goal", "volumen")
        u_split = str(user.get("split") or user.get("routine") or user.get("split_routine") or "ppl6")
        schedule = SPLIT_SCHEDULES.get(u_split)
        today_idx = datetime.datetime.now(datetime.timezone.utc).weekday()
        if schedule is not None:
            u_routine = schedule[today_idx]
        else:
            u_routine = u_split if u_split in ROUTINES else None

        # Acceso por packs: dueño, prueba gratis de TRIAL_DAYS días o packs comprados
        is_en = str(u_lang).lower().startswith("en")
        days_used = 0
        try:
            created = datetime.datetime.fromisoformat(str(user.get("created", "")).replace("Z", "+00:00"))
            days_used = (datetime.datetime.now(datetime.timezone.utc) - created).days
        except ValueError:
            days_used = 0
        is_owner = bool(OWNER_CHAT_ID) and str(chat_id) == OWNER_CHAT_ID
        in_trial = days_used < TRIAL_DAYS
        packs = set(user.get("packs") or [])
        if user.get("premium"):
            packs.add("full")
        all_access = is_owner or in_trial or "full" in packs

        def has(p: str) -> bool:
            return all_access or p in packs

        def link(p: str) -> str:
            return f"{PACK_LINKS[p]}?client_reference_id={chat_id}"

        focus = ""
        if u_routine and u_routine in ROUTINES:
            focus = ROUTINES[u_routine]["en" if is_en else "es"]["focus"]

        if not all_access and not packs:
            if today_idx not in (0, 3):  # lunes y jueves: recordatorio corto
                print(f"[USER {chat_id}] trial ended, no message today")
                continue
            if is_en:
                teaser = (f"🔒 DAZ PERFORMANCE · Your free trial has ended.\n\n"
                          + (f"Today's session was ready for you: {focus}.\n\n" if focus else "")
                          + "Choose your pack and keep your plan every morning:\n"
                          + f"🏋️ Training 2.99 €/mo → {link('entreno')}\n"
                          + f"🍽️ Nutrition 2.99 €/mo → {link('nutricion')}\n"
                          + f"💊 Supplements 1.99 €/mo → {link('suplementos')}\n"
                          + f"⭐ Complete 4.99 €/mo (all 3) → {link('full')}")
            else:
                teaser = (f"🔒 DAZ PERFORMANCE · Tu prueba gratis ha terminado.\n\n"
                          + (f"Hoy tenías lista tu sesión: {focus}.\n\n" if focus else "")
                          + "Elige tu pack y sigue recibiendo tu plan cada mañana:\n"
                          + f"🏋️ Entrenamiento 2,99 €/mes → {link('entreno')}\n"
                          + f"🍽️ Nutrición 2,99 €/mes → {link('nutricion')}\n"
                          + f"💊 Suplementos 1,99 €/mes → {link('suplementos')}\n"
                          + f"⭐ Completo 4,99 €/mes (los 3) → {link('full')}")
            ok_user = send_telegram_message(str(chat_id), teaser)
            print(f"[USER {chat_id}] teaser sent={ok_user}")
            continue

        if schedule is not None and u_routine is None:
            personal_msg = build_rest_message(u_lang, u_name, u_weight, u_goal)
        else:
            personal_msg = build_workout_message(
                lang=u_lang,
                name=u_name,
                weight_kg=u_weight,
                goal=u_goal,
                routine_key=u_routine,
            )

        # Suplementación completa en lugar de la línea simple de creatina
        stack = supplement_lines(u_lang, u_weight, u_goal, training_day=not (schedule is not None and u_routine is None))
        base_lines = personal_msg.split("\n")
        idx = next((i for i, l in enumerate(base_lines) if l.startswith("💊")), None)
        if idx is not None:
            base_lines = base_lines[:idx] + stack + [l for l in base_lines[idx + 1:] if not l.startswith("💊")]
            personal_msg = "\n".join(base_lines)

        if not all_access:
            lines = personal_msg.split("\n")
            if not has("nutricion"):
                lines = [l for l in lines if not l.startswith("🍽️")]
            if not has("suplementos"):
                lines = [l for l in lines if not l.startswith("💊")]
            if not has("entreno"):
                head = lines[0] if lines else "DAZ PERFORMANCE"
                keep = [l for l in lines if l.startswith("🍽️") or l.startswith("💊")]
                locked = (f"🔒 Today's session ({focus or 'training'}) is in the Training Pack · 2.99 €/mo → {link('entreno')}"
                          if is_en else
                          f"🔒 Tu sesión de hoy ({focus or 'entrenamiento'}) está en el Pack Entrenamiento · 2,99 €/mes → {link('entreno')}")
                lines = [head, ""] + keep + ["", locked]
            personal_msg = "\n".join(lines)
            missing = [p for p in ("entreno", "nutricion", "suplementos") if p not in packs]
            if missing:
                personal_msg += ("\n\n⭐ Get everything with the Complete Pack · 4.99 €/mo → " if is_en
                                 else "\n\n⭐ Tenlo todo con el Pack Completo · 4,99 €/mes → ") + link("full")
        elif in_trial and not is_owner and "full" not in packs:
            left = TRIAL_DAYS - days_used
            if is_en:
                personal_msg += (f"\n\n🎁 Free trial: {left} day(s) left." if left > 1 else "\n\n⏳ Your free trial ends tomorrow.")
                personal_msg += f"\n⭐ Keep it with a pack from 1.99 €/mo (send /premium) or the Complete Pack 4.99 € → {link('full')}"
            else:
                personal_msg += (f"\n\n🎁 Prueba gratis: te quedan {left} día(s)." if left > 1 else "\n\n⏳ Tu prueba gratis termina mañana.")
                personal_msg += f"\n⭐ Sigue con un pack desde 1,99 €/mes (escribe /premium) o el Pack Completo 4,99 € → {link('full')}"
        ok_user = send_telegram_message(str(chat_id), personal_msg)
        print(f"[USER {chat_id}] lang={u_lang} sent={ok_user}")


if __name__ == "__main__":
    run()
