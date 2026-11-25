import os
import json
import datetime
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
WORKER_URL = os.environ.get("CF_WORKER_URL", "").strip()
ADMIN_SECRET = os.environ.get("CF_ADMIN_SECRET", "").strip()
CHANNEL_ES = os.environ.get("TELEGRAM_CHANNEL_ES", "@DAZPerformance_ES").strip()
CHANNEL_EN = os.environ.get("TELEGRAM_CHANNEL_EN", "@DAZPerformance_EN").strip()

# Calendario semanal de sesiones por rutina (0=Lunes ... 6=Domingo)
WORKOUT_SCHEDULES = {
    "ppl6": {
        0: {
            "es": ("PUSH A: PECHO, HOMBRO Y TRÍCEPS", "58 min", [
                ("Press Inclinado con Mancuernas (30°)", "4 x 8-10", "120s"),
                ("Press Banca Plano con Barra", "4 x 6-8", "150s"),
                ("Elevaciones Laterales en Polea", "4 x 12-15", "60s"),
                ("Cruces en Polea Alta a Baja", "3 x 12-15", "75s"),
                ("Extensión de Tríceps en Polea Alta", "4 x 10-12", "75s")
            ]),
            "en": ("PUSH A: CHEST, SHOULDERS & TRICEPS", "58 min", [
                ("Incline Dumbbell Press (30°)", "4 x 8-10", "120s"),
                ("Flat Barbell Bench Press", "4 x 6-8", "150s"),
                ("Cable Lateral Raises", "4 x 12-15", "60s"),
                ("High-to-Low Cable Flyes", "3 x 12-15", "75s"),
                ("Overhead Cable Triceps Extension", "4 x 10-12", "75s")
            ])
        },
        1: {
            "es": ("PULL A: ESPALDA, DELTOIDES POSTERIOR Y BÍCEPS", "55 min", [
                ("Dominadas Lastradas o Jalón al Pecho", "4 x 6-8", "120s"),
                ("Remo con Barra Inclinado", "4 x 8-10", "150s"),
                ("Remo Unilateral en Polea Baja", "3 x 10-12", "90s"),
                ("Face Pull en Polea Alta", "4 x 15", "60s"),
                ("Curl Bíceps en Banco Inclinado 45°", "4 x 8-10", "75s")
            ]),
            "en": ("PULL A: BACK, REAR DELTS & BICEPS", "55 min", [
                ("Weighted Pull-Ups or Lat Pulldown", "4 x 6-8", "120s"),
                ("Bent-Over Barbell Row", "4 x 8-10", "150s"),
                ("Single-Arm Seated Cable Row", "3 x 10-12", "90s"),
                ("High Cable Face Pulls", "4 x 15", "60s"),
                ("45° Incline Dumbbell Bicep Curl", "4 x 8-10", "75s")
            ])
        },
        2: {
            "es": ("LEGS A: CUÁDRICEPS, ISQUIOS, GLÚTEO Y GEMELO", "65 min", [
                ("Sentadilla Libre o Hack Squat", "4 x 6-8", "180s"),
                ("Peso Muerto Rumano con Barra", "4 x 8-10", "150s"),
                ("Prensa Inclinada 45°", "3 x 10-12", "120s"),
                ("Curl Femoral Tumbado", "3 x 12", "75s"),
                ("Elevación de Talones de Pie", "4 x 12-15", "60s")
            ]),
            "en": ("LEGS A: QUADS, HAMSTRINGS, GLUTES & CALVES", "65 min", [
                ("Barbell Back Squat or Hack Squat", "4 x 6-8", "180s"),
                ("Romanian Deadlift (RDL)", "4 x 8-10", "150s"),
                ("45° Leg Press", "3 x 10-12", "120s"),
                ("Lying Leg Curl", "3 x 12", "75s"),
                ("Standing Calf Raises", "4 x 12-15", "60s")
            ])
        },
        3: {
            "es": ("PUSH B: HIPERTROFIA DE HOMBRO 3D, PECHO Y TRÍCEPS", "55 min", [
                ("Press Militar Sentado con Mancuernas", "4 x 8-10", "120s"),
                ("Press Inclinado en Multipower", "3 x 10-12", "90s"),
                ("Elevaciones Laterales Mancuernas", "4 x 15", "60s"),
                ("Press Francés con Barra Z", "4 x 10-12", "90s"),
                ("Fondos en Paralelas", "3 x al fallo controlado", "90s")
            ]),
            "en": ("PUSH B: 3D DELTS, CHEST & TRICEPS HYPERTROPHY", "55 min", [
                ("Seated Dumbbell Overhead Press", "4 x 8-10", "120s"),
                ("Smith Machine Incline Press", "3 x 10-12", "90s"),
                ("Dumbbell Lateral Raises", "4 x 15", "60s"),
                ("EZ-Bar Skullcrushers", "4 x 10-12", "90s"),
                ("Parallel Bar Dips", "3 x controlled failure", "90s")
            ])
        },
        4: {
            "es": ("PULL B: AMPLITUD DORSAL Y GROSOR DE BRAZO", "55 min", [
                ("Jalón Agarre Estrecho Neutro", "4 x 10-12", "90s"),
                ("Remo en Punta (T-Bar)", "4 x 8-10", "120s"),
                ("Pull-Over en Polea Alta con Cuerda", "3 x 12-15", "60s"),
                ("Curl Martillo con Cuerda en Polea", "4 x 10-12", "75s"),
                ("Pájaros en Máquina Inversa", "4 x 15", "60s")
            ]),
            "en": ("PULL B: LAT WIDTH & ARM THICKNESS", "55 min", [
                ("Close-Grip Neutral Lat Pulldown", "4 x 10-12", "90s"),
                ("Chest-Supported T-Bar Row", "4 x 8-10", "120s"),
                ("Rope Cable Pullover", "3 x 12-15", "60s"),
                ("Cable Rope Hammer Curl", "4 x 10-12", "75s"),
                ("Reverse Pec Deck Rear Delt Fly", "4 x 15", "60s")
            ])
        },
        5: {
            "es": ("LEGS B: GLÚTEO, FEMORAL Y CUÁDRICEPS METABÓLICO", "60 min", [
                ("Hip Thrust con Barra Olímpica", "4 x 8-10", "150s"),
                ("Sentadilla Búlgara con Mancuernas", "3 x 10 / lado", "90s"),
                ("Extensión de Cuádriceps (Pausa 1s arriba)", "4 x 12-15", "75s"),
                ("Curl Femoral Sentado", "4 x 12", "75s"),
                ("Gemelo Sentado", "4 x 15", "60s")
            ]),
            "en": ("LEGS B: GLUTES, HAMSTRINGS & METABOLIC QUADS", "60 min", [
                ("Barbell Hip Thrust", "4 x 8-10", "150s"),
                ("Dumbbell Bulgarian Split Squat", "3 x 10 / leg", "90s"),
                ("Leg Extensions (1s peak pause)", "4 x 12-15", "75s"),
                ("Seated Leg Curl", "4 x 12", "75s"),
                ("Seated Calf Raises", "4 x 15", "60s")
            ])
        },
        6: {
            "es": ("DÍA DE DESCANSO Y RECUPERACIÓN ACTIVA", "0 min", []),
            "en": ("FULL REST & ACTIVE RECOVERY DAY", "0 min", [])
        }
    }
}


def send_tg(chat_id, text):
    if not TOKEN or not chat_id:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status


def fetch_subscribers():
    if not WORKER_URL or not ADMIN_SECRET:
        return []
    req = urllib.request.Request(
        f"{WORKER_URL.rstrip('/')}/subscribers",
        headers={"Authorization": f"Bearer {ADMIN_SECRET}"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def format_workout_message(user, weekday):
    lang = user.get("lang", "es")
    split = user.get("split", "ppl6")
    weight = float(user.get("weight", 85))
    name = user.get("name", "Atleta")

    schedule = WORKOUT_SCHEDULES.get(split, WORKOUT_SCHEDULES["ppl6"])
    day_plan = schedule.get(weekday, schedule[0])[lang]
    title, duration, exercises = day_plan

    creatine_g = round(weight * 0.1, 1)

    if lang == "en":
        if not exercises:
            return (
                f"🔋 <b>DAZ PREMIUM FIT PERFORMANCE — SUNDAY RECOVERY</b>\n\n"
                f"Good morning, <b>{name}</b>. Today is total nervous system and muscular recovery.\n"
                f"• Take your daily <b>{creatine_g}g Creatine Monohydrate</b> + Omega-3.\n"
                f"• Hit your protein target ({round(weight*2.1)}g) and sleep 8 hours.\n\n"
                f"👉 Official Store: https://dazpremiumfit.com"
            )
        lines = [
            f"🔥 <b>DAZ PREMIUM FIT PERFORMANCE • MORNING WORKOUT</b>",
            f"Athlete: <b>{name}</b> | Duration: <b>{duration}</b>",
            f"🎯 <b>{title}</b>\n"
        ]
        for idx, (ex_name, sets, rest) in enumerate(exercises, 1):
            lines.append(f"{idx}️⃣ <b>{ex_name}</b>\n   • Sets: {sets} | Rest: <b>{rest}</b> between sets")
        lines.append(f"\n💊 Today's Creatine: <b>{creatine_g}g</b> | Protein Goal: <b>{round(weight*2.1)}g</b>")
        lines.append("🛒 Gear & Supplements: https://dazpremiumfit.com")
        return "\n".join(lines)
    else:
        if not exercises:
            return (
                f"🔋 <b>DAZ PREMIUM FIT PERFORMANCE — DESCANSO Y CRECIMIENTO</b>\n\n"
                f"Buenos días, <b>{name}</b>. Hoy toca recuperación completa del sistema nervioso y tejido muscular.\n"
                f"• Toma tus <b>{creatine_g}g de Creatina Monohidrato</b> + Omega-3.\n"
                f"• Cumple tu objetivo de proteína ({round(weight*2.1)}g) y prioriza el sueño profundo.\n\n"
                f"👉 Tienda Oficial: https://dazpremiumfit.com"
            )
        lines = [
            f"🔥 <b>DAZ PREMIUM FIT PERFORMANCE • ENTRENAMIENTO DE HOY</b>",
            f"Atleta: <b>{name}</b> | Duración estimada: <b>{duration}</b>",
            f"🎯 <b>{title}</b>\n"
        ]
        for idx, (ex_name, sets, rest) in enumerate(exercises, 1):
            lines.append(f"{idx}️⃣ <b>{ex_name}</b>\n   • Series: {sets} | Descanso: <b>{rest}</b> entre series")
        lines.append(f"\n💊 Dosis Creatina hoy: <b>{creatine_g}g</b> | Objetivo Proteína: <b>{round(weight*2.1)}g</b>")
        lines.append("🛒 Ropa Deportiva y Suplementos: https://dazpremiumfit.com")
        return "\n".join(lines)


def main():
    weekday = datetime.datetime.utcnow().weekday()  # 0 = Lunes ... 6 = Domingo
    subscribers = fetch_subscribers()
    print(f"[COACH] Suscriptores activos encontrados: {len(subscribers)}")

    for user in subscribers:
        try:
            msg = format_workout_message(user, weekday)
            send_tg(user["chat_id"], msg)
            print(f"[COACH OK] Enviado a {user.get('name')} ({user.get('lang')})")
        except Exception as e:
            print(f"[COACH ERR] Error enviando a {user.get('chat_id')}: {e}")

    # Publicación diaria automática en ambos canales oficiales (ES y EN)
    try:
        msg_es = format_workout_message({"name": "Comunidad DAZ", "lang": "es", "split": "ppl6", "weight": 85}, weekday)
        msg_en = format_workout_message({"name": "DAZ Athletes", "lang": "en", "split": "ppl6", "weight": 85}, weekday)
        if CHANNEL_ES:
            send_tg(CHANNEL_ES, msg_es)
        if CHANNEL_EN:
            send_tg(CHANNEL_EN, msg_en)
    except Exception as e:
        print("[CHANNELS ERR]", e)


if __name__ == "__main__":
    main()
