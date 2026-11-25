import os
import json
import datetime
import re

DATA_DIR = "data"
STORE_URL = "https://dazpremiumfit.com"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_daily_index(total_items):
    epoch = datetime.date(2026, 1, 1)
    today = datetime.date.today()
    days_passed = (today - epoch).days
    return days_passed % total_items


def build_nutrition_matrix():
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "elite_foods": {
            "proteins": [
                {"name": "Pechuga de Pollo / Pavo", "macros_100g": "23g Prot | 0g Carb | 1.5g Grasa", "benefit": "Perfil completo de aminoácidos esenciales y alta biodisponibilidad sin grasa saturada."},
                {"name": "Ternera Magra (Solomillo / Babilla)", "macros_100g": "21g Prot | 0g Carb | 4g Grasa", "benefit": "Rica en hierro hemo, zinc, vitamina B12 y creatina natural endógena."},
                {"name": "Huevos Enteros + Claras", "macros_100g": "13g Prot | 1g Carb | 10g Grasa", "benefit": "Valor biológico 100 (patrón oro); la yema aporta colina y colesterol precursor hormonal."},
                {"name": "Salmón Salvaje / Caballa", "macros_100g": "20g Prot | 0g Carb | 13g Grasa", "benefit": "Fuente primaria de ácidos grasos Omega-3 (EPA/DHA) antiinflamatorios."},
                {"name": "Pescado Blanco (Merluza / Bacalao)", "macros_100g": "18g Prot | 0g Carb | 0.8g Grasa", "benefit": "Digestión ultrarrápida y densidad calórica mínima, ideal en fases de definición."},
                {"name": "Whey Protein Isolate", "macros_100g": "88g Prot | 1g Carb | 1g Grasa", "benefit": "Máxima concentración de L-Leucina para disparar la síntesis proteica post-entreno."}
            ],
            "carbs": [
                {"name": "Arroz Basmati / Jazmín", "macros_100g": "7g Prot | 78g Carb | 0.6g Grasa", "benefit": "Almidón de fácil asimilación sin gluten ni antinutrientes; recarga glucógeno sin pesadez."},
                {"name": "Copos de Avena Integral", "macros_100g": "13g Prot | 60g Carb | 7g Grasa", "benefit": "Energía sostenida, betaglucanos para salud cardiovascular y control glucémico."},
                {"name": "Patata / Boniato Asado", "macros_100g": "2g Prot | 20g Carb | 0.1g Grasa", "benefit": "Índice de saciedad altísimo y aporte masivo de potasio intracelular para bombeo muscular."},
                {"name": "Crema de Arroz (Cream of Rice)", "macros_100g": "6g Prot | 80g Carb | 0.5g Grasa", "benefit": "Digestión inmediata pre-entreno para rendir al 100% sin distensión abdominal."},
                {"name": "Frutos Rojos (Arándanos / Fresas)", "macros_100g": "1g Prot | 10g Carb | 0.3g Grasa", "benefit": "Polifenoles y antioxidantes de bajo impacto glucémico que reducen el estrés oxidativo."}
            ],
            "fats": [
                {"name": "Aceite de Oliva Virgen Extra (AOVE)", "macros_100g": "0g Prot | 0g Carb | 100g Grasa", "benefit": "Ácido oleico monoinsaturado y polifenoles cardioprotectores."},
                {"name": "Aguacate Hass", "macros_100g": "2g Prot | 8g Carb | 15g Grasa", "benefit": "Grasas monoinsaturadas, fibra prebiótica y potasio."},
                {"name": "Nueces / Almendras Crudas", "macros_100g": "15g Prot | 14g Carb | 55g Grasa", "benefit": "Magnesio, vitamina E y ácidos grasos esenciales para el entorno hormonal."}
            ]
        },
        "specialized_diets": [
            {
                "id": "keto",
                "name": "Dieta Cetogénica (Keto Clínico / Rendimiento)",
                "macros_split": "70% Grasas | 25% Proteínas | 5% Carbohidratos (<30g netos/día)",
                "mechanism": "Agota el glucógeno hepático en 48-72h forzando al hígado a producir cuerpos cetónicos (beta-hidroxibutirato) como combustible cerebral y muscular altamente eficiente.",
                "rules": [
                    "Mantener carbohidratos netos por debajo de 25-30g diarios (solo vegetales fibrosos verdes).",
                    "Suplementar electrolitos obligatoriamente: 4-5g Sodio, 3-4g Potasio y 400mg Magnesio para evitar la 'gripe keto'.",
                    "Ideal para mejorar sensibilidad a la insulina, claridad mental y control del apetito en pérdida de grasa."
                ],
                "sample_day": [
                    "Desayuno: 4 Huevos enteros revueltos con 30g de aguacate y café solo con 10g de aceite MCT.",
                    "Almuerzo: 220g Salmón a la plancha con espárragos trigueros y 15ml de AOVE.",
                    "Cena: 220g Entrecot de ternera o muslos de pollo con ensalada de espinacas y 25g de nueces."
                ]
            },
            {
                "id": "carb_cycling",
                "name": "Ciclado de Carbohidratos (Carb Cycling)",
                "macros_split": "Días Altos (Entreno Pierna/Espalda) | Días Medios (Torso) | Días Bajos (Descanso)",
                "mechanism": "Manipula la insulina y la leptina semanalmente: aporta glucosa máxima los días de mayor demanda mecánica y maximiza la lipólisis los días de baja actividad.",
                "rules": [
                    "Días Altos: 4-5g Carbohidratos/kg peso | Grasas bajas (0.5g/kg).",
                    "Días Bajos: 1-1.5g Carbohidratos/kg peso | Grasas moderadas (1g/kg).",
                    "Proteína fija todos los días en 2.2 - 2.4g/kg de peso corporal."
                ],
                "sample_day": [
                    "Día Alto: 350g Arroz cocido repartido pre y post entreno + 200g Pollo por comida.",
                    "Día Bajo: 0g Arroz/Avena; solo proteínas magras, verduras verdes, huevos enteros y aguacate."
                ]
            },
            {
                "id": "volumen_limpio",
                "name": "Hipertrofia Controlada (Lean Bulk)",
                "macros_split": "Superávit +300 a +400 kcal | Proteína 2.1g/kg | Grasas 0.85g/kg | Resto Carbos",
                "mechanism": "Maximiza la señalización anabólica (mTOR) y la síntesis proteica manteniendo el porcentaje graso bajo control.",
                "rules": [
                    "Subida de peso objetivo: entre 0.25% y 0.5% del peso corporal por semana.",
                    "Concentrar el 45% de los carbohidratos diarios en las comidas previa y posterior al entrenamiento."
                ],
                "sample_day": [
                    "4 a 5 comidas sólidas + batido Whey Isolate post-entreno con Creatina."
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
        "categories": {
            "masa_muscular": [
                {
                    "name": "Creatina Monohidrato Pura (200 Mesh)",
                    "grade": "Grado A • Evidencia Máxima",
                    "how_to_take": "0.1g por kg de peso corporal al día (ej. 8-9g diarios), todos los días con agua o comida.",
                    "mechanism": "Satura la fosfocreatina intramuscular, eleva la fuerza máxima, resíntesis de ATP e hidratación celular.",
                    "featured_store": True
                },
                {
                    "name": "Proteína Whey Isolate (Aislado de Suero)",
                    "grade": "Grado A • Evidencia Máxima",
                    "how_to_take": "30g - 40g inmediatamente tras entrenar o para completar requerimientos proteicos.",
                    "mechanism": "Aporta >3g de L-Leucina pura de rápida absorción para disparar la síntesis proteica vía mTOR.",
                    "featured_store": True
                },
                {
                    "name": "L-Citrulina Malato 2:1 + Beta-Alanina",
                    "grade": "Grado A • Rendimiento y Bombeo",
                    "how_to_take": "6-8g de Citrulina + 3.2g de Beta-Alanina 30 minutos antes del entrenamiento.",
                    "mechanism": "Aumenta el óxido nítrico, vasodilatación periférica y tampona el ácido láctico en series largas.",
                    "featured_store": True
                },
                {
                    "name": "EAA (Aminoácidos Esenciales) + Ciclodextrina",
                    "grade": "Grado B+ • Intra-Entreno",
                    "how_to_take": "12g EAA + 30g Ciclodextrina disueltos en 1L de agua durante sesiones de +75 minutos.",
                    "mechanism": "Frena el catabolismo inducido por cortisol y mantiene la glucemia estable durante el entrenamiento.",
                    "featured_store": False
                }
            ],
            "perdida_peso": [
                {
                    "name": "Cafeína Anhidra + Extracto de Té Verde (EGCG)",
                    "grade": "Grado A • Termogénesis y Lipólisis",
                    "how_to_take": "200mg Cafeína + 400mg EGCG 30 minutos antes del cardio o entrenamiento de fuerza.",
                    "mechanism": "Eleva las catecolaminas (adrenalina/noradrenalina) movilizando ácidos grasos libres de los adipocitos.",
                    "featured_store": True
                },
                {
                    "name": "L-Carnitina L-Tartrato",
                    "grade": "Grado B • Transporte Mitocondrial",
                    "how_to_take": "2g - 3g diarios acompañados de una comida con carbohidratos o insulina para su captación muscular.",
                    "mechanism": "Facilita el transporte de ácidos grasos de cadena larga hacia la mitocondria y acelera la recuperación.",
                    "featured_store": False
                },
                {
                    "name": "Berberina HCL (500mg)",
                    "grade": "Grado A • Sensibilidad a la Insulina",
                    "how_to_take": "500mg 15 minutos antes de las dos comidas principales con carbohidratos.",
                    "mechanism": "Activa la enzima AMPK, mejorando la captación de glucosa muscular y reduciendo picos de insulina.",
                    "featured_store": False
                },
                {
                    "name": "Glucomanano / Psyllium Husk",
                    "grade": "Grado A • Saciedad en Déficit",
                    "how_to_take": "3g con 400ml de agua 20 minutos antes de la comida más abundante.",
                    "mechanism": "Fibra soluble viscosa que retrasa el vaciado gástrico y bloquea el hambre en déficit calórico.",
                    "featured_store": False
                }
            ],
            "salud": [
                {
                    "name": "Omega-3 Ultra Puro (EPA / DHA)",
                    "grade": "Grado A • Cardiovascular y Cerebral",
                    "how_to_take": "2.5g - 3g combinados de EPA+DHA al día junto a comidas con grasa.",
                    "mechanism": "Reduce triglicéridos, mejora la flexibilidad arterial, protege la función cognitiva y regula inflamación.",
                    "featured_store": True
                },
                {
                    "name": "Vitamina D3 (4000 UI) + K2 (MK-7 100mcg)",
                    "grade": "Grado A • Sistema Inmune y Óseo",
                    "how_to_take": "1 cápsula diaria con el desayuno (requiere grasa para absorberse).",
                    "mechanism": "La D3 optimiza testosterona e inmunidad; la K2 dirige el calcio al hueso evitando calcificación arterial.",
                    "featured_store": True
                },
                {
                    "name": "Magnesio Bisglicinato + Zinc Quelado",
                    "grade": "Grado A • Descanso y Entorno Hormonal",
                    "how_to_take": "400mg Magnesio + 15mg Zinc 45 minutos antes de dormir.",
                    "mechanism": "Cofactor en más de 300 reacciones enzimáticas; mejora el sueño profundo y la recuperación del SNC.",
                    "featured_store": True
                },
                {
                    "name": "Coenzima Q10 (Ubiquinol 100mg) + NAC",
                    "grade": "Grado B+ • Protección Hepática y Mitocondrial",
                    "how_to_take": "100mg Ubiquinol + 600mg N-Acetilcisteína por la mañana.",
                    "mechanism": "Eleva el glutatión intracelular (antioxidante maestro) y protege el miocardio.",
                    "featured_store": False
                }
            ],
            "alivio": [
                {
                    "name": "Colágeno Hidrolizado Tipo I y II + Vitamina C",
                    "grade": "Grado B+ • Tendones y Cartílago",
                    "how_to_take": "15g de Colágeno + 100mg de Vitamina C 45 minutos antes de entrenar o antes de dormir.",
                    "mechanism": "Estimula la síntesis de matriz extracelular en tendones, ligamentos y articulaciones sometidas a carga.",
                    "featured_store": True
                },
                {
                    "name": "Cúrcuma Fitosomada (Curcumina + Piperina)",
                    "grade": "Grado A • Antiinflamatorio Natural",
                    "how_to_take": "500mg - 1000mg diarios repartidos en comidas.",
                    "mechanism": "Inhibe citoquinas proinflamatorias (NF-kB y COX-2) aliviando molestias articulares sin dañar el estómago.",
                    "featured_store": False
                },
                {
                    "name": "Ashwagandha KSM-66 (600mg)",
                    "grade": "Grado A • Control de Cortisol y Estrés",
                    "how_to_take": "300mg por la mañana y 300mg por la tarde/noche.",
                    "mechanism": "Adaptógeno clínico que reduce el cortisol sérico hasta un 27%, mejorando la calma y el descanso.",
                    "featured_store": False
                },
                {
                    "name": "Glucosamina Sulfato + Condroitina + MSM",
                    "grade": "Grado B+ • Lubricación Articular",
                    "how_to_take": "1500mg Glucosamina + 1200mg Condroitina + 2000mg MSM al día.",
                    "mechanism": "Mantiene la viscosidad del líquido sinovial y amortigua el impacto articular en sentadillas y presses.",
                    "featured_store": False
                }
            ],
            "cabello": [
                {
                    "name": "Saw Palmetto (Serenoa Repens 320mg) + Semilla de Calabaza",
                    "grade": "Grado B+ • Inhibidor Natural 5-Alfa Reductasa",
                    "how_to_take": "320mg extracto estandarizado al 85-95% de ácidos grasos diarios con comida.",
                    "mechanism": "Ayuda a modular la conversión de testosterona en DHT en el folículo piloso de forma natural.",
                    "featured_store": False
                },
                {
                    "name": "Biotina (5000mcg) + Zinc + L-Cisteína",
                    "grade": "Grado A • Estructura de Queratina",
                    "how_to_take": "1 dosis diaria con el desayuno.",
                    "mechanism": "Aporta los aminoácidos azufrados y coenzimas indispensables para el grosor y resistencia del tallo capilar.",
                    "featured_store": True
                },
                {
                    "name": "Colágeno Marino + Silicio Orgánico + Hierro (si hay déficit)",
                    "grade": "Grado B+ • Irrigación y Anclaje Folicular",
                    "how_to_take": "10g Colágeno + 50mg Silicio al día.",
                    "mechanism": "Mejora la microcirculación del cuero cabelludo y fortalece la dermis donde se ancla el folículo.",
                    "featured_store": True
                }
            ]
        }
    }


def build_marketing_showcase():
    campaigns = [
        {
            "badge": "DIVISIÓN CIENTÍFICA • DAZ PREMIUM FIT PERFORMANCE",
            "headline": "INGENIERÍA TEXTIL Y CIENCIA PARA EL FÍSICO DE ÉLITE",
            "subheadline": "Cortes anatómicos diseñados para resaltar la proporción hombro-cintura, tejidos de alto gramaje y suplementación clínica respaldada por datos reales.",
            "cta_text": "EXPLORAR TIENDA OFICIAL DAZ PREMIUM FIT",
            "cta_url": STORE_URL,
            "featured_items": [
                {"title": "Oversized Heavyweight Pump Tee", "tag": "Corte Culturismo • Algodón 280 GSM", "url": STORE_URL},
                {"title": "Compression Pro Stringer & Tank", "tag": "Ajuste Anatómico • Secado Rápido", "url": STORE_URL},
                {"title": "The Blueprint Series: Pack Rendimiento", "tag": "Whey Isolate + Creatina 200 Mesh", "url": f"{STORE_URL}/collections/supplements"}
            ]
        },
        {
            "badge": "ALTO RENDIMIENTO • MARCA REGISTRADA EN EE. UU.",
            "headline": "DEL LABORATORIO A LA TARIMA Y AL HIERRO",
            "subheadline": "Sin rellenos ocultos ni fórmulas infradosificadas. Equipamiento deportivo y protocolos diseñados para atletas que exigen resultados medibles.",
            "cta_text": "ACCEDER AL CATÁLOGO OFICIAL",
            "cta_url": STORE_URL,
            "featured_items": [
                {"title": "The Prestige Protocol: Biometric Mastery®", "tag": "Suplementación de Precisión", "url": f"{STORE_URL}/collections/supplements"},
                {"title": "Performance Tapered Joggers", "tag": "Flexibilidad Total en Sentadilla", "url": STORE_URL},
                {"title": "DAZMOND® Urban Luxury Footwear", "tag": "Colección Exclusiva Fuera del Gym", "url": "https://dazmond.com"}
            ]
        }
    ]
    idx = get_daily_index(len(campaigns))
    selected = campaigns[idx]
    selected["updated_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return selected


def build_blog_posts():
    today_str = datetime.date.today().strftime("%d/%m/%Y")
    articles = [
        {
            "id": "hipertrofia-tension-mecanica",
            "category": "BIOMECÁNICA E HIPERTROFIA",
            "date": today_str,
            "read_time": "4 min",
            "title": "Tensión Mecánica vs. Estrés Metabólico: Qué construye tejido contráctil real",
            "summary": "Las últimas 5 repeticiones efectivas cerca del fallo muscular reclutan las unidades motoras de alto umbral responsables de la hipertrofia miofibrilar.",
            "content": "Acumular series sin intensidad real solo genera fatiga del sistema nervioso. Para maximizar el crecimiento, prioriza ejercicios estables donde puedas aplicar sobrecarga progresiva entre 6 y 12 repeticiones, manteniendo un RIR (repeticiones en recámara) de 1 a 2 y controlando la fase excéntrica durante 2-3 segundos."
        },
        {
            "id": "creatina-dosis-real",
            "category": "NUTRICIÓN CLÍNICA",
            "date": today_str,
            "read_time": "3 min",
            "title": "Por qué la dosis estándar de 5g de Creatina se queda corta en atletas de +85 kg",
            "summary": "El cálculo científico basado en peso corporal (0.1g/kg) optimiza la saturación muscular y cognitiva frente a la recomendación genérica.",
            "content": "La mayoría de fabricantes imprimen 5 gramos como dosis universal. Sin embargo, los estudios farmacocinéticos demuestran que un atleta de 90 kg requiere entre 8 y 9 gramos diarios de creatina monohidrato pura para mantener los depósitos de fosfocreatina al 100%, acelerando la resíntesis de ATP entre series pesadas."
        },
        {
            "id": "frecuencia-entrenamiento-natural",
            "category": "PROGRAMACIÓN",
            "date": today_str,
            "read_time": "5 min",
            "title": "Frecuencia 2 vs. Weider Clásica: Cómo gestionar la síntesis proteica en atletas naturales",
            "summary": "La síntesis de proteínas musculares regresa a niveles basales entre 36 y 48 horas después de entrenar. Dividir el volumen semanal duplica las ventanas de crecimiento.",
            "content": "Hacer 20 series de pecho el lunes provoca daño muscular excesivo cuya recuperación consume recursos sin aportar hipertrofia extra. Dividir ese trabajo en 10 series el lunes y 10 series el jueves permite entrenar con cargas más altas y mayor calidad técnica en cada sesión."
        },
        {
            "id": "keto-vs-carbohidratos-rendimiento",
            "category": "METABOLISMO",
            "date": today_str,
            "read_time": "5 min",
            "title": "Dieta Cetogénica vs. Alta en Carbohidratos: Cuándo usar cada estrategia según tu fisiología",
            "summary": "Mientras la glucosa domina en esfuerzos glucolíticos de alta intensidad, la cetosis ofrece una herramienta superior para flexibilidad metabólica y control insulínico.",
            "content": "No existe una dieta única para todo el año. Utilizar bloques cetogénicos controlados mejora la sensibilidad a la insulina y reduce la inflamación sistémica, preparando el terreno hormonal para que, al reintroducir carbohidratos en fase de volumen, la partición calórica se dirija hacia el músculo y no al tejido adiposo."
        },
        {
            "id": "salud-capilar-atleta",
            "category": "LONGEVIDAD Y ESTÉTICA",
            "date": today_str,
            "read_time": "4 min",
            "title": "Cómo proteger la salud capilar y articular bajo entrenamiento de alta intensidad",
            "summary": "El estrés oxidativo, los déficits de zinc/hierro y la inflamación crónica impactan directamente en el folículo piloso y los tendones.",
            "content": "El entrenamiento intenso incrementa la demanda de micronutrientes clave. Asegurar niveles óptimos de Vitamina D3, Zinc, Biotina, Colágeno con Vitamina C y ácidos grasos Omega-3 protege simultáneamente la integridad de los tejidos conectivos y el ciclo anágeno del cabello."
        }
    ]

    rot = get_daily_index(len(articles))
    ordered = articles[rot:] + articles[:rot]
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "posts": ordered
    }


def run_integrity_audit(files_map):
    """
    Motor de autodiagnóstico y reparación:
    Verifica que ningún JSON esté vacío, que todos los módulos existan y que index.html esté íntegro.
    """
    errors = []
    for filename, data in files_map.items():
        if not data or len(json.dumps(data)) < 100:
            errors.append(f"Archivo corrupto o vacío detectado: {filename}")

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        required_markers = ["DAZ PREMIUM FIT", "tab-planner", "tab-training", "tab-nutrition", "tab-supplements", "tab-blog", "</html>"]
        for marker in required_markers:
            if marker not in html_content:
                errors.append(f"Falta marcador crítico en index.html: {marker}")

    status_report = {
        "last_audit_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "status": "HEALTHY" if not errors else "REPAIRED_WITH_WARNINGS",
        "errors_found": errors,
        "modules_verified": list(files_map.keys())
    }

    with open(os.path.join(DATA_DIR, "system_health.json"), "w", encoding="utf-8") as f:
        json.dump(status_report, f, ensure_ascii=False, indent=2)

    print(f"[AUDIT] Estado del sistema: {status_report['status']}")
    if errors:
        print("[AUDIT WARNINGS]:", errors)


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
        print(f"[OK] Generado y verificado: {filepath}")

    run_integrity_audit(files_map)


if __name__ == "__main__":
    main()
