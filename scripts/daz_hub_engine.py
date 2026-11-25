import os
import json
import datetime
import hashlib

DATA_DIR = "data"
STORE_URL = "https://dazpremiumfit.com"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_rotation_index(total_items, step_days=2):
    epoch = datetime.date(2026, 1, 1)
    today = datetime.date.today()
    days_passed = (today - epoch).days
    return (days_passed // step_days) % total_items


def build_nutrition_matrix():
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "equation": "Mifflin-St Jeor (1990) + Factor de Actividad Físico",
        "protocols": [
            {
                "id": "volumen",
                "name": "Superávit Limpio (Hipertrofia Máxima)",
                "caloric_delta": "+350 kcal sobre TDEE",
                "protein_g_kg": 2.1,
                "fat_g_kg": 0.9,
                "carbs_rule": "Resto de calorías para glucógeno y rendimiento",
                "meal_timing": "4-5 ingestas diarias; 40% de carbohidratos concentrados peri-entreno.",
                "sample_menu": [
                    "Comida 1: 120g Avena + 40g Whey Isolate + 15g Crema de Almendras + Arándanos",
                    "Comida 2 (Pre-Entreno): 200g Pechuga de Pollo + 250g Arroz Basmati cocido + 10ml AOVE",
                    "Comida 3 (Post-Entreno): 220g Ternera Magra + 300g Patata asada + Verduras verdes",
                    "Comida 4: 250g Salmón o Huevos enteros (4 uds) + 150g Arroz o Pan de masa madre"
                ]
            },
            {
                "id": "definicion",
                "name": "Déficit Estratégico (Preservación Muscular)",
                "caloric_delta": "-450 kcal sobre TDEE",
                "protein_g_kg": 2.4,
                "fat_g_kg": 0.75,
                "carbs_rule": "Ciclado alrededor del entrenamiento",
                "meal_timing": "Alta saciedad, prioridad proteica para bloquear catabolismo.",
                "sample_menu": [
                    "Comida 1: 6 Claras + 2 Huevos enteros + 60g Avena + Café solo",
                    "Comida 2 (Pre-Entreno): 220g Pechuga de Pavo + 150g Arroz cocido + Espárragos",
                    "Comida 3 (Post-Entreno): 45g Whey Isolate + 1 Plátano + 5g Creatina Monohidrato",
                    "Comida 4: 250g Merluza o Lubina + 250g Brócoli/Calabacín + 10ml AOVE"
                ]
            },
            {
                "id": "recomposicion",
                "name": "Recomposición Corporal (Calorías de Mantenimiento)",
                "caloric_delta": "0 kcal (TDEE Exacto)",
                "protein_g_kg": 2.3,
                "fat_g_kg": 0.85,
                "carbs_rule": "Moderados y constantes",
                "meal_timing": "Distribución equitativa de leucina cada 4 horas (3-4g por toma).",
                "sample_menu": [
                    "Comida 1: 40g Whey Isolate + 80g Copos de Avena + 10g Nueces",
                    "Comida 2: 200g Solomillo de Pollo + 200g Boniato asado + Ensalada",
                    "Comida 3: 200g Ternera Magra + 180g Arroz Integral + Pimientos",
                    "Comida 4: 250g Queso Fresco Batido 0% o Caseína + 20g Almendras"
                ]
            }
        ]
    }


def build_training_system():
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "by_days": [
            {
                "days": "3 Días (Full Body Pesado)",
                "level": "Intermedio / Agenda Exigente",
                "schedule": "Lunes - Miércoles - Viernes",
                "focus": "Tensión mecánica global y progresión de cargas en básicos multiarticulares.",
                "sessions": [
                    "Día 1: Sentadilla Barra (4x6), Press Banca Plano (4x6), Remo con Barra (4x8), Curl Barra Z (3x10)",
                    "Día 2: Peso Muerto Rumano (4x8), Press Militar Barra (4x6), Jalón al Pecho (4x10), Fondos Lastrados (3x8)",
                    "Día 3: Prensa 45° (4x10), Press Inclinado Mancuernas (4x8), Remo Polea Baja (4x10), Elevaciones Laterales (4x15)"
                ]
            },
            {
                "days": "4 Días (Torso / Pierna Potencia-Hipertrofia)",
                "level": "Intermedio - Avanzado",
                "schedule": "Lunes, Martes, Jueves, Viernes",
                "focus": "Frecuencia 2 real por grupo muscular con recuperación neural óptima.",
                "sessions": [
                    "Día 1 (Torso Fuerza): Press Banca (4x5), Remo Pendlay (4x6), Press Militar (3x8), Dominadas (3x8)",
                    "Día 2 (Pierna Fuerza): Sentadilla Libre (4x6), Peso Muerto Rumano (4x8), Prensa (3x10), Gemelo Pie (4x12)",
                    "Día 3 (Torso Hipertrofia): Press Inclinado (4x10), Jalón Neutro (4x10), Elevaciones Laterales (4x15), Superserie Brazo (3x12)",
                    "Día 4 (Pierna Hipertrofia): Sentadilla Hack (4x10), Hip Thrust (4x10), Curl Femoral Tumbado (4x12), Extensión Cuádriceps (3x15)"
                ]
            },
            {
                "days": "5 Días (PHAT / Híbrido Élite)",
                "level": "Avanzado",
                "schedule": "Lunes a Viernes (Sábado y Domingo Descanso)",
                "focus": "Combina dos días de fuerza pesada con tres días de volumen metabólico y detalle muscular.",
                "sessions": [
                    "Día 1: Torso Pesado (Press Banca, Remo Barra, Press Hombro)",
                    "Día 2: Pierna Pesada (Sentadilla, Peso Muerto Rumano, Gemelo)",
                    "Día 3: Espalda y Hombros Hipertrofia (12-15 reps controladas)",
                    "Día 4: Pierna y Glúteo Hipertrofia (Hack, Hip Thrust, Aislamientos)",
                    "Día 5: Pecho y Brazos Bombo Máximo (Inclinado, Cruces, Bíceps/Tríceps)"
                ]
            },
            {
                "days": "6 Días (Push Pull Legs x2)",
                "level": "Atleta Avanzado",
                "schedule": "6 Días Activos / 1 Descanso Total",
                "focus": "Máximo estímulo semanal repartido sin fatiga excesiva por sesión.",
                "sessions": [
                    "Lunes / Jueves (Push): Pecho, Deltoides Anterior/Lateral, Tríceps",
                    "Martes / Viernes (Pull): Dorsal, Trapecio, Deltoides Posterior, Bíceps",
                    "Miércoles / Sábado (Legs): Cuádriceps, Isquiosurales, Glúteo, Gemelo"
                ]
            }
        ],
        "by_muscle_group": [
            {
                "id": "pecho",
                "muscle": "Pectoral (Estética y Densidad)",
                "svg_type": "bench_press",
                "biomechanics": "Aducción horizontal del húmero. Priorizar ángulo clavicular (30°) para estética superior.",
                "exercises": [
                    {"name": "Press Inclinado con Mancuernas (30°)", "sets": "4 x 8-10", "rest": "120s", "cue": "Retracción escapular firme, baja hasta estirar el pectoral sin perder tensión."},
                    {"name": "Press Banca Plano con Barra", "sets": "4 x 6-8", "rest": "150s", "cue": "Codos a 45° respecto al torso, empuje explosivo."},
                    {"name": "Cruces en Polea Alta a Baja", "sets": "3 x 12-15", "rest": "75s", "cue": "Contracción pico de 1 segundo juntando muñecas."},
                    {"name": "Fondos en Paralelas Lastrados", "sets": "3 x 8-10", "rest": "90s", "cue": "Inclina el torso 20° hacia delante para enfatizar pectoral inferior."}
                ]
            },
            {
                "id": "espalda",
                "muscle": "Espalda (Amplitud en V y Grosor)",
                "svg_type": "lat_pulldown",
                "biomechanics": "Extensión y aducción del hombro en plano frontal para amplitud; retracción escapular en plano sagital para grosor.",
                "exercises": [
                    {"name": "Jalón al Pecho Agarre Neutro/Mag", "sets": "4 x 8-10", "rest": "120s", "cue": "Inicia el movimiento deprimiendo los hombros, lleva los codos a la cadera."},
                    {"name": "Remo con Barra Inclinado", "sets": "4 x 6-8", "rest": "150s", "cue": "Torso a 45°, tira hacia el ombligo manteniendo lumbar neutra."},
                    {"name": "Remo Unilateral en Polea Baja", "sets": "3 x 10-12", "rest": "90s", "cue": "Estira completamente el dorsal en la fase excéntrica de 3 segundos."},
                    {"name": "Pull-Over en Polea Alta con Cuerda", "sets": "3 x 12-15", "rest": "75s", "cue": "Brazos semirrígidos, aísla el dorsal sin intervención del bíceps."}
                ]
            },
            {
                "id": "pierna",
                "muscle": "Pierna Completa (Cuádriceps e Isquios)",
                "svg_type": "squat",
                "biomechanics": "Máxima flexión de rodilla bajo carga para vastos del cuádriceps; bisagra de cadera para isquiosurales.",
                "exercises": [
                    {"name": "Sentadilla Libre o Hack Squat", "sets": "4 x 6-8", "rest": "180s", "cue": "Rodillas siguen la línea de la punta del pie, profundidad paralela o superior."},
                    {"name": "Peso Muerto Rumano con Barra", "sets": "4 x 8-10", "rest": "150s", "cue": "Empuja la cadera atrás hasta notar tensión máxima en el isquio; barra pegada a tibias."},
                    {"name": "Prensa Inclinada 45° (Pies Bajos)", "sets": "3 x 10-12", "rest": "120s", "cue": "No despegues el sacro del respaldo al bajar."},
                    {"name": "Curl Femoral Sentado + Extensión Cuádriceps", "sets": "3 x 12-15", "rest": "90s", "cue": "Control excéntrico estricto de 3 segundos en cada repetición."}
                ]
            },
            {
                "id": "gluteo",
                "muscle": "Glúteo (Potencia y Proyección)",
                "svg_type": "hip_thrust",
                "biomechanics": "Extensión de cadera con pico de tensión en acortamiento máximo y abducción.",
                "exercises": [
                    {"name": "Hip Thrust con Barra Olímpica", "sets": "4 x 8-10", "rest": "150s", "cue": "Mirada al frente, retroversión pélvica arriba, pausa de 2 segundos en contracción."},
                    {"name": "Sentadilla Búlgara con Mancuernas", "sets": "3 x 8-10 / lado", "rest": "90s", "cue": "Paso largo e inclinación ligera del torso para maximizar elongación del glúteo mayor."},
                    {"name": "Patada de Glúteo en Polea Baja", "sets": "3 x 12-15 / lado", "rest": "60s", "cue": "Extiende en diagonal (30° hacia fuera) siguiendo las fibras del glúteo."},
                    {"name": "Abducción de Cadera en Máquina", "sets": "3 x 15-20", "rest": "60s", "cue": "Torso ligeramente inclinado hacia delante para activar glúteo medio."}
                ]
            },
            {
                "id": "brazo",
                "muscle": "Brazo Completo (Bíceps, Tríceps y Braquial)",
                "svg_type": "bicep_curl",
                "biomechanics": "El tríceps representa 2/3 del volumen del brazo; trabajar en estiramiento (cabeza larga) y acortamiento.",
                "exercises": [
                    {"name": "Curl en Banco Inclinado 45° con Mancuernas", "sets": "4 x 8-10", "rest": "90s", "cue": "Codos detrás del torso para estirar la cabeza larga del bíceps."},
                    {"name": "Press Francés con Barra Z o Mancuernas", "sets": "4 x 8-10", "rest": "90s", "cue": "Lleva la barra detrás de la cabeza para tensión constante en cabeza larga del tríceps."},
                    {"name": "Curl Martillo en Polea con Cuerda", "sets": "3 x 10-12", "rest": "75s", "cue": "Enfocado en braquial anterior y braquiorradial para grosor lateral."},
                    {"name": "Extensión de Tríceps en Polea Alta (Barra V)", "sets": "3 x 12-15", "rest": "75s", "cue": "Codos bloqueados a los costados, extensión completa."}
                ]
            },
            {
                "id": "hombro",
                "muscle": "Deltoides 3D (Estética Classic Physique)",
                "svg_type": "lateral_raise",
                "biomechanics": "El deltoides lateral crea la ilusión óptica de cintura estrecha y amplitud clavicular.",
                "exercises": [
                    {"name": "Press Militar Sentado con Mancuernas", "sets": "4 x 6-8", "rest": "120s", "cue": "Codos en plano escapular (30° hacia delante), sin arquear lumbar."},
                    {"name": "Elevaciones Laterales en Polea a la Altura de Muñeca", "sets": "4 x 12-15", "rest": "60s", "cue": "Tensión continua desde el inicio del recorrido; lidera con los codos."},
                    {"name": "Pájaros en Máquina Contractora Inversa", "sets": "4 x 12-15", "rest": "60s", "cue": "Empuja hacia los lados sin juntar en exceso las escápulas."},
                    {"name": "Remo al Mentón Agarre Ancho con Barra Z", "sets": "3 x 10-12", "rest": "75s", "cue": "Sube hasta la línea del pecho para proteger el manguito rotador."}
                ]
            }
        ],
        "american_ppl": {
            "title": "Protocolo Americano Push / Pull / Legs (PPL)",
            "description": "Sistema estándar en culturismo moderno. Agrupa músculos por patrón biomecánico sinérgico, permitiendo alta intensidad y recuperación limpia.",
            "blocks": [
                {
                    "tag": "PUSH (Empuje)",
                    "muscles": "Pectoral + Deltoides Anterior/Lateral + Tríceps",
                    "routine": [
                        "1. Press Inclinado Barra/Multipower: 4 x 6-8",
                        "2. Press Plano Mancuernas: 3 x 8-10",
                        "3. Elevaciones Laterales Mancuernas: 4 x 12-15",
                        "4. Cruces en Polea: 3 x 12-15",
                        "5. Extensión Tríceps Polea Alta: 4 x 10-12"
                    ]
                },
                {
                    "tag": "PULL (Tracción)",
                    "muscles": "Dorsal Ancho + Trapecio + Deltoides Posterior + Bíceps",
                    "routine": [
                        "1. Dominadas Lastradas o Jalón Pecho: 4 x 6-8",
                        "2. Remo en Punta (T-Bar) o Barra: 4 x 8-10",
                        "3. Remo Gironda Agarre Estrecho: 3 x 10-12",
                        "4. Face Pull en Polea Alta: 4 x 15",
                        "5. Curl Bíceps Barra Recta + Curl Predicador: 3 x 10"
                    ]
                },
                {
                    "tag": "LEGS (Tren Inferior)",
                    "muscles": "Cuádriceps + Isquiosurales + Glúteo + Gemelo",
                    "routine": [
                        "1. Sentadilla Libre / Hack: 4 x 6-8",
                        "2. Peso Muerto Rumano: 4 x 8-10",
                        "3. Prensa 45°: 3 x 10-12",
                        "4. Curl Femoral Tumbado: 3 x 12",
                        "5. Elevación de Talones de Pie: 4 x 12-15"
                    ]
                }
            ]
        },
        "frequency_specialization": [
            {
                "name": "Frecuencia 2 Global (Equilibrio Total)",
                "split": "Torso / Pierna / Descanso / Push / Pull / Legs",
                "weekly_sets": "14-16 series efectivas por grupo muscular",
                "ideal_for": "Atletas naturales que buscan hipertrofia simétrica sin saturar el sistema nervioso."
            },
            {
                "name": "Especialización Frecuencia 3 en Brazos",
                "split": "Día 1: Brazos + Hombro | Día 2: Pierna | Día 3: Pecho/Espalda + Bíceps | Día 4: Descanso | Día 5: Brazos + Hombro | Día 6: Pierna",
                "weekly_sets": "20-22 series semanales para Bíceps y Tríceps; mantenimiento (8 series) en torso/pierna.",
                "ideal_for": "Romper estancamientos de perímetro de brazo en bloques de 6 a 8 semanas."
            },
            {
                "name": "Especialización Frecuencia 3 en Pierna y Glúteo",
                "split": "Día 1: Cuádriceps Dominante | Día 2: Torso Completo | Día 3: Glúteo e Isquios | Día 4: Descanso | Día 5: Pierna Completa | Día 6: Torso Bombo",
                "weekly_sets": "22 series semanales en tren inferior; mantenimiento en tren superior.",
                "ideal_for": "Maximizar densidad en cuádriceps, femorales y proyección glútea."
            },
            {
                "name": "Especialización Amplitud V-Taper (Hombro + Dorsal)",
                "split": "Frecuencia 3 en Deltoides Lateral y Dorsal; Frecuencia 1.5 en Pecho/Pierna",
                "weekly_sets": "20 series en deltoides lateral y dorsal.",
                "ideal_for": "Estética Classic Physique y proporción cintura-hombro."
            }
        ]
    }


def build_supplements_matrix():
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "brand_line": "The Blueprint Series: Nutritional Foundation® & The Prestige Protocol®",
        "supplements": [
            {
                "name": "1. Proteína Whey Isolate (Aislado de Suero)",
                "evidence_grade": "Grado A (Evidencia Máxima)",
                "mechanism": "Aporte rápido de aminoácidos esenciales y alto contenido en L-Leucina (>3g por toma) para activar la vía mTOR y la síntesis proteica miofibrilar.",
                "dosage": "30g - 40g post-entreno o para alcanzar requerimiento proteico diario.",
                "synergy": "Combinar con Creatina Monohidrato tras entrenar.",
                "shop_url": f"{STORE_URL}/collections/supplements"
            },
            {
                "name": "2. Creatina Monohidrato (200 Mesh / Pura)",
                "evidence_grade": "Grado A (Evidencia Máxima)",
                "mechanism": "Satura los depósitos de fosfocreatina intramuscular, acelerando la resíntesis de ATP en series pesadas de 1 a 12 repeticiones y aumentando la hidratación celular.",
                "dosage": "0.1g por kg de peso corporal al día (ej. 8g - 9g diarios), todos los días sin descansos.",
                "synergy": "Absorción optimizada junto a carbohidratos o proteína.",
                "shop_url": f"{STORE_URL}/collections/supplements"
            },
            {
                "name": "3. Pre-Entreno de Rendimiento (Citrulina + Cafeína + Beta-Alanina)",
                "evidence_grade": "Grado A (Evidencia Máxima)",
                "mechanism": "La L-Citrulina (6-8g) eleva el óxido nítrico y el flujo sanguíneo; la Cafeína (3-5mg/kg) reduce la percepción de fatiga; la Beta-Alanina tampona la acidez muscular.",
                "dosage": "1 servicio 25-30 minutos antes de la sesión de fuerza.",
                "synergy": "Evitar en las 6 horas previas al sueño para preservar la arquitectura del descanso.",
                "shop_url": f"{STORE_URL}/collections/supplements"
            },
            {
                "name": "4. Omega-3 Alta Pureza (EPA / DHA)",
                "evidence_grade": "Grado A (Salud Cardiovascular y Articular)",
                "mechanism": "Modula la inflamación sistémica post-entrenamiento, mejora la sensibilidad a la insulina y protege la salud endotelial y articular bajo cargas pesadas.",
                "dosage": "2g - 3g combinados de EPA + DHA diarios junto a una comida con grasas.",
                "synergy": "Potencia la absorción de vitaminas liposolubles (D3, K2, E).",
                "shop_url": f"{STORE_URL}/collections/supplements"
            },
            {
                "name": "5. Multivitamínico y Minerales Quelados",
                "evidence_grade": "Grado B+ (Soporte Metabólico)",
                "mechanism": "Cubre micronutrientes críticos (Zinc, Magnesio, Vitamina D3, Complejo B) esenciales para la producción hormonal endógena y el metabolismo energético en déficit o volumen.",
                "dosage": "1 dosis diaria con el desayuno.",
                "synergy": "Previene caídas de rendimiento por carencias subclínicas de micronutrientes.",
                "shop_url": f"{STORE_URL}/collections/supplements"
            },
            {
                "name": "6. Colágeno Hidrolizado + Vitamina C",
                "evidence_grade": "Grado B+ (Tejido Conectivo y Tendones)",
                "mechanism": "Proporciona glicina, prolina e hidroxiprolina necesarios para la regeneración de tendones, ligamentos y cartílago sometidos a alta tensión mecánica.",
                "dosage": "10g - 15g diarios junto con 50-100mg de Vitamina C (cofactor indispensable).",
                "synergy": "Ideal tomar 45 minutos antes del entrenamiento o antes de dormir.",
                "shop_url": f"{STORE_URL}/collections/supplements"
            }
        ]
    }


def build_marketing_showcase():
    campaigns = [
        {
            "badge": "COLECCIÓN OFICIAL • EE. UU.",
            "headline": "INGENIERÍA TEXTIL PARA EL FÍSICO DE ÉLITE",
            "subheadline": "Cortes anatómicos diseñados para resaltar la proporción hombro-cintura. Tejidos de alto gramaje, durabilidad extrema y estética minimalista oscura.",
            "cta_text": "EXPLORAR ROPA DEPORTIVA EN TIENDA",
            "cta_url": STORE_URL,
            "featured_items": [
                {"title": "Oversized Heavyweight Pump Tee", "tag": "Corte Culturismo • Algodón 280 GSM", "url": STORE_URL},
                {"title": "Compression Pro Stringer & Tank", "tag": "Ajuste Anatómico • Secado Rápido", "url": STORE_URL},
                {"title": "The Blueprint Series: Pack Rendimiento", "tag": "Whey Isolate + Creatina 200 Mesh", "url": f"{STORE_URL}/collections/supplements"}
            ]
        },
        {
            "badge": "PROTOCOLO DE RENDIMIENTO • DAZ PREMIUM FIT",
            "headline": "DEL LABORATORIO A LA TARIMA Y AL HIERRO",
            "subheadline": "Sin rellenos ocultos ni fórmulas infradosificadas. Suplementación grado clínico y equipamiento textil diseñado para atletas que exigen resultados medibles.",
            "cta_text": "ACCEDER AL CATÁLOGO OFICIAL",
            "cta_url": STORE_URL,
            "featured_items": [
                {"title": "The Prestige Protocol: Biometric Mastery®", "tag": "Suplementación de Precisión", "url": f"{STORE_URL}/collections/supplements"},
                {"title": "Performance Tapered Joggers", "tag": "Flexibilidad Total en Sentadilla", "url": STORE_URL},
                {"title": "Calzado Técnico de Halterofilia y Gym", "tag": "Base Plana de Máxima Estabilidad", "url": STORE_URL}
            ]
        }
    ]
    idx = get_rotation_index(len(campaigns), step_days=2)
    selected = campaigns[idx]
    selected["updated_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return selected


def build_blog_posts():
    today_str = datetime.date.today().strftime("%d/%m/%Y")
    seed_articles = [
        {
            "id": "hipertrofia-tension-mecanica",
            "category": "BIOMECÁNICA E HIPERTROFIA",
            "date": today_str,
            "read_time": "4 min",
            "title": "Tensión Mecánica vs. Estrés Metabólico: Qué construye tejido contráctil real",
            "summary": "La ciencia actual demuestra que las últimas 5 repeticiones efectivas cerca del fallo muscular reclutan las unidades motoras de alto umbral responsables del crecimiento real.",
            "content": "El error más habitual en sala es acumular series basura sin intensidad real. Para maximizar la hipertrofia miofibrilar, prioriza ejercicios estables donde puedas aplicar sobrecarga progresiva entre 6 y 12 repeticiones, manteniendo un RIR (repeticiones en recámara) de 1 a 2 y controlando la fase excéntrica durante 2-3 segundos."
        },
        {
            "id": "creatina-dosis-real",
            "category": "NUTRICIÓN CLÍNICA",
            "date": today_str,
            "read_time": "3 min",
            "title": "Por qué la dosis estándar de 5g de Creatina se queda corta en atletas de +85 kg",
            "summary": "El cálculo científico basado en peso corporal (0.1g/kg) optimiza la saturación muscular y cognitiva frente a la recomendación genérica de etiqueta.",
            "content": "La mayoría de fabricantes imprimen 5 gramos como dosis universal. Sin embargo, los estudios farmacocinéticos muestran que un atleta de 90 kg requiere entre 8 y 9 gramos diarios de creatina monohidrato pura para mantener los depósitos de fosfocreatina al 100%, acelerando la recuperación entre series pesadas."
        },
        {
            "id": "frecuencia-entrenamiento-natural",
            "category": "PROGRAMACIÓN",
            "date": today_str,
            "read_time": "5 min",
            "title": "Frecuencia 2 vs. Weider Clásica: Cómo gestionar la síntesis proteica en atletas naturales",
            "summary": "La síntesis de proteínas musculares regresa a niveles basales entre 36 y 48 horas después de entrenar. Dividir el volumen semanal duplica las ventanas de crecimiento.",
            "content": "Hacer 20 series de pecho el lunes genera un daño muscular excesivo cuya recuperación consume recursos sin aportar hipertrofia extra. Dividir ese trabajo en 10 series el lunes y 10 series el jueves permite entrenar con cargas más altas y mayor calidad técnica en cada sesión."
        },
        {
            "id": "sueno-cortisol-composicion",
            "category": "RECUPERACIÓN Y HORMONAS",
            "date": today_str,
            "read_time": "4 min",
            "title": "El impacto real del cortisol elevado y la falta de sueño en la pérdida de grasa",
            "summary": "Dormir menos de 6 horas desploma la oxidación de ácidos grasos y aumenta la pérdida de masa libre de grasa durante un déficit calórico.",
            "content": "Durante el sueño profundo se produce el mayor pulso fisiológico de hormona del crecimiento y la regulación del eje hipotálamo-hipófisis. Sin descanso adecuado, el cortisol crónico favorece la retención hídrica y el catabolismo proteico."
        }
    ]

    # Rotación dinámica para que el artículo principal cambie automáticamente cada 2 días
    rot = get_rotation_index(len(seed_articles), step_days=2)
    ordered = seed_articles[rot:] + seed_articles[:rot]
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "posts": ordered
    }


def main():
    ensure_dir(DATA_DIR)

    files_map = {
        "nutrition_matrix.json": build_nutrition_matrix(),
        "fitness_plans.json": build_training_system(),
        "supplement_analysis.json": build_supplements_matrix(),
        "marketing_showcase.json": build_marketing_showcase(),
        "blog_posts.json": build_blog_posts()
    }

    for filename, payload in files_map.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"[OK] Generado: {filepath}")


if __name__ == "__main__":
    main()
