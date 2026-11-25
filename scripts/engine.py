import os
import json
import datetime

DATA_DIR = "data"
STORE_DPF = "https://dazpremiumfit.com"
STORE_DAZMOND = "https://dazmond.com"
STORE_VALMONT = "https://valmontco.com"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_daily_index(total_items):
    epoch = datetime.date(2026, 1, 1)
    today = datetime.date.today()
    return (today - epoch).days % total_items


def ex(name, sets, rest, cue, steps, mistake):
    return {
        "name": name,
        "sets": sets,
        "rest": rest,
        "cue": cue,
        "steps": steps,
        "mistake": mistake
    }


def build_training_system():
    return {
        "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "by_days": [
            {"days": "Rutina 01 • 3 Días Full Body Fuerza-Hipertrofia", "level": "Intermedio / Agenda Ocupada", "schedule": "Lunes - Miércoles - Viernes", "focus": "Básicos multiarticulares pesados con frecuencia 3 global.", "sessions": ["Día 1: Sentadilla Barra (4x6), Press Banca (4x6), Remo Barra (4x8), Curl Barra Z (3x10)", "Día 2: Peso Muerto Rumano (4x8), Press Militar (4x6), Jalón Pecho (4x10), Fondos (3x10)", "Día 3: Prensa 45° (4x10), Press Inclinado (4x8), Remo Polea (4x10), Elevaciones Laterales (4x15)"]},
            {"days": "Rutina 02 • 3 Días Empuje / Tracción / Pierna", "level": "Principiante - Intermedio", "schedule": "Lunes - Miércoles - Viernes", "focus": "Sesiones limpias de 55 minutos sin fatiga acumulada.", "sessions": ["Día 1 (Push): Press Inclinado (4x8), Press Militar (3x8), Cruces Polea (3x12), Tríceps Cuerda (3x12)", "Día 2 (Pull): Jalón Neutro (4x8), Remo Mancuerna (3x10), Face Pull (3x15), Curl Inclinado (3x10)", "Día 3 (Legs): Hack Squat (4x8), Curl Femoral (4x10), Hip Thrust (3x10), Gemelo Pie (4x15)"]},
            {"days": "Rutina 03 • 4 Días Torso / Pierna Potencia-Hipertrofia", "level": "Intermedio - Avanzado", "schedule": "Lunes, Martes, Jueves, Viernes", "focus": "Frecuencia 2 real por grupo muscular combinando cargas altas y volumen.", "sessions": ["Día 1 (Torso Fuerza): Press Banca (4x5), Remo Pendlay (4x6), Press Hombro (3x8), Dominadas (3x8)", "Día 2 (Pierna Fuerza): Sentadilla (4x6), Peso Muerto Rumano (4x8), Prensa (3x10), Gemelo (4x12)", "Día 3 (Torso Bombo): Press Inclinado (4x10), Jalón Pecho (4x10), Laterales (4x15), Brazo (3x12)", "Día 4 (Pierna Bombo): Hack Squat (4x10), Hip Thrust (4x10), Femoral Sentado (4x12), Extensión (3x15)"]},
            {"days": "Rutina 04 • 4 Días Empuje / Tracción (Upper/Lower Split)", "level": "Intermedio", "schedule": "Lunes, Martes, Jueves, Viernes", "focus": "Ideal para mejorar postura, espalda y densidad de tren superior.", "sessions": ["Día 1: Pecho + Hombro Anterior/Lateral + Tríceps", "Día 2: Cuádriceps + Isquios + Gemelo", "Día 3: Espalda + Deltoides Posterior + Bíceps", "Día 4: Glúteo + Femoral + Cuádriceps Unilateral"]},
            {"days": "Rutina 05 • 4 Días Arnold Split Compacto", "level": "Intermedio - Avanzado", "schedule": "Lunes, Martes, Jueves, Viernes", "focus": "Pecho/Espalda antagonista y Hombros/Brazos con máximo bombeo.", "sessions": ["Día 1: Pecho y Espalda (Superseries antagonistas)", "Día 2: Hombros y Brazos Completos", "Día 3: Pierna Completa Pesada", "Día 4: Torso Estético (Enfoque clavicular y amplitud)"]},
            {"days": "Rutina 06 • 5 Días PHAT (Power Hypertrophy Adaptive)", "level": "Avanzado", "schedule": "Lunes a Viernes (Fin de semana libre)", "focus": "Dos días de fuerza máxima + tres días de hipertrofia pura.", "sessions": ["Día 1: Torso Fuerza", "Día 2: Pierna Fuerza", "Día 3: Espalda y Hombros Hipertrofia", "Día 4: Pierna y Glúteo Hipertrofia", "Día 5: Pecho y Brazos Bombo Máximo"]},
            {"days": "Rutina 07 • 5 Días Push / Pull / Legs + Upper / Lower", "level": "Avanzado", "schedule": "Lunes a Viernes", "focus": "Frecuencia 2 completa en 5 días dejando sábado y domingo de descanso.", "sessions": ["Día 1: Push", "Día 2: Pull", "Día 3: Legs", "Día 4: Torso Completo", "Día 5: Pierna Completa"]},
            {"days": "Rutina 08 • 5 Días Classic Physique Estética V-Taper", "level": "Avanzado", "schedule": "Lunes a Viernes", "focus": "Prioridad total en deltoides lateral, dorsal ancho, pectoral superior y pierna.", "sessions": ["Día 1: Pecho Superior y Deltoides Lateral", "Día 2: Espalda Amplitud y Deltoides Posterior", "Día 3: Cuádriceps y Gemelo", "Día 4: Brazos Completos y Hombro 3D", "Día 5: Isquios, Glúteo y Espalda Grosor"]},
            {"days": "Rutina 09 • 6 Días Push / Pull / Legs Frecuencia 2", "level": "Atleta Avanzado", "schedule": "6 Días Activos / 1 Descanso", "focus": "Estándar de oro para hipertrofia máxima repartiendo el volumen semanal.", "sessions": ["Lunes/Jueves: Pecho, Hombro y Tríceps", "Martes/Viernes: Espalda, Deltoides Posterior y Bíceps", "Miércoles/Sábado: Cuádriceps, Isquios, Glúteo y Gemelo"]},
            {"days": "Rutina 10 • 6 Días Arnold Split Clásico x2", "level": "Atleta Avanzado", "schedule": "6 Días Activos / 1 Descanso", "focus": "Frecuencia 2 con días dedicados exclusivamente a hombros y brazos.", "sessions": ["Lunes/Jueves: Pecho y Espalda", "Martes/Viernes: Hombros y Brazos", "Miércoles/Sábado: Piernas Completas"]}
        ],
        "by_muscle_group": [
            {
                "id": "pecho",
                "muscle": "Pectoral (Estética y Densidad)",
                "svg_type": "bench_press",
                "biomechanics": "Aducción horizontal y flexión del húmero. Priorizar el haz clavicular (inclinación 30°) construye un pecho alto y estético.",
                "exercises": [
                    ex("Press Inclinado con Mancuernas (30°)", "4 x 8-10", "120s", "Retracción escapular firme y estiramiento profundo abajo.", ["1. Ajusta el banco exactamente a 30 grados (un punto por encima del plano).", "2. Junta los omóplatos contra el respaldo y saca el pecho.", "3. Baja las mancuernas en 3 segundos hasta que queden a la altura del pecho exterior.", "4. Empuja hacia arriba y ligeramente hacia dentro sin chocar las mancuernas."], "Poner el banco a 45° o más, lo que traslada todo el trabajo al deltoides anterior."),
                    ex("Press Banca Plano con Barra Olímpica", "4 x 6-8", "150s", "Codos a 45° respecto al torso, empuje explosivo.", ["1. Agarra la barra ligeramente más ancho que tus hombros.", "2. Mantén glúteos, espalda alta y pies firmemente apoyados.", "3. Desciende la barra hasta tocar suavemente la línea media del esternón.", "4. Extiende los codos con potencia manteniendo los hombros atrás."], "Abrir los codos a 90° en forma de T, lo que compromete el manguito rotador."),
                    ex("Press Inclinado en Máquina Convergente", "3 x 10-12", "90s", "Máxima estabilidad para llevar las series cerca del fallo.", ["1. Regula el asiento para que los agarres queden a la altura de la parte superior del pecho.", "2. Mantén los codos alineados con las muñecas.", "3. Empuja hasta la convergencia máxima y sostén 1 segundo la contracción."], "Despegar la espalda del respaldo en las últimas repeticiones."),
                    ex("Cruces en Polea Alta a Baja", "3 x 12-15", "75s", "Tensión constante en fibras esternales e inferiores.", ["1. Da un paso al frente para estabilizar el torso e inclínate ligeramente.", "2. Con codos semiflexionados fijos, junta las manos frente a la cadera.", "3. Abre los brazos de forma controlada hasta sentir estiramiento pectoral."], "Flexionar y extender los codos convirtiendo el ejercicio en un press."),
                    ex("Aperturas en Máquina Contractora (Pec Deck)", "3 x 12-15", "75s", "Aislamiento puro de aducción horizontal sin fatiga estabilizadora.", ["1. Ajusta los brazos de la máquina para permitir un estiramiento cómodo atrás.", "2. Mantén el pecho alto y los hombros lejos de las orejas.", "3. Junta los brazos al frente apretando el pectoral durante 1 segundo."], "Encoger los trapecios hacia arriba al cerrar los brazos."),
                    ex("Fondos en Paralelas Lastrados", "3 x 8-10", "120s", "Inclinación frontal de 20° para enfatizar pectoral inferior.", ["1. Sujeta las paralelas e inclina el torso hacia delante.", "2. Baja hasta que el hombro quede ligeramente por debajo del codo.", "3. Empuja hacia arriba sin bloquear violentamente los codos."], "Mantener el torso totalmente vertical, lo que enfoca el tríceps en lugar del pecho."),
                    ex("Press Plano con Mancuernas", "3 x 8-10", "120s", "Mayor rango de recorrido y libertad articular que la barra.", ["1. Túmbate con retracción escapular y pies anclados al suelo.", "2. Baja las mancuernas abriendo ligeramente los codos hasta estirar el pectoral.", "3. Sube siguiendo un arco natural hasta alinear sobre los hombros."], "Dejar caer los codos demasiado rápido perdiendo tensión en la parte baja."),
                    ex("Cruces en Polea Baja a Alta (Haz Clavicular)", "3 x 12-15", "60s", "Trayectoria ascendente siguiendo las fibras superiores.", ["1. Coloca las poleas en la posición más baja.", "2. Eleva los brazos hacia delante y arriba hasta la altura de la barbilla.", "3. Controla el descenso resistiendo la carga."], "Usar impulso de cadera para subir los cables."),
                    ex("Press Declinado con Barra o Máquina", "3 x 8-10", "90s", "Alta activación del pectoral esternal con menor estrés en hombro.", ["1. Asegura las piernas en los rodillos y retrae escápulas.", "2. Baja la barra hacia la parte baja del esternón.", "3. Empuja en línea recta hacia arriba."], "Rebotar la barra sobre las costillas inferiores."),
                    ex("Flexiones Lastradas con Déficit (Push-Ups)", "3 x al fallo RIR 1", "60s", "Finalizador metabólico con estiramiento extra.", ["1. Coloca las manos sobre dos discos o agarraderas para bajar más profundo.", "2. Mantén el abdomen y glúteos en bloque rígido.", "3. Baja hasta que el pecho pase la línea de las manos y empuja."], "Dejar caer la cadera arqueando la zona lumbar.")
                ]
            },
            {
                "id": "espalda",
                "muscle": "Espalda (Amplitud en V y Grosor)",
                "svg_type": "lat_pulldown",
                "biomechanics": "Aducción en plano frontal para amplitud dorsal; tracción horizontal y retracción escapular para densidad central.",
                "exercises": [
                    ex("Jalón al Pecho Agarre Neutro / Mag", "4 x 8-10", "120s", "Inicia deprimiendo los hombros y lleva los codos a la cadera.", ["1. Sujeta el agarre neutro y bloquea las rodillas bajo los rodillos.", "2. Saca el pecho ligeramente hacia arriba sin balancearte atrás.", "3. Tira de los codos hacia abajo hasta que el agarre toque la clavícula."], "Tirar con los bíceps encorvando los hombros hacia delante al final."),
                    ex("Remo con Barra Inclinado", "4 x 6-8", "150s", "Torso a 45°, tracción dirigida hacia el ombligo.", ["1. Flexiona ligeramente rodillas e inclina el torso con espalda neutra.", "2. Tira de la barra hacia la parte baja del abdomen.", "3. Aprieta las escápulas arriba y baja en 2 segundos."], "Levantar el torso en cada repetición usando impulso lumbar."),
                    ex("Dominadas Lastradas Pronas", "4 x 6-8", "150s", "Rey de la amplitud dorsal y fuerza relativa.", ["1. Agarra la barra un poco más ancho que los hombros.", "2. Inicia subiendo el pecho hacia la barra mientras bajas los hombros.", "3. Desciende hasta extender completamente los brazos."], "Hacer medias repeticiones sin bajar hasta la extensión completa."),
                    ex("Remo Unilateral en Polea Baja", "3 x 10-12", "90s", "Estiramiento completo del dorsal en cada repetición.", ["1. Siéntate erguido con un agarre individual.", "2. Deja que el hombro avance ligeramente al estirar para elongar el dorsal.", "3. Tira del codo pegado al costado hasta pasarlo detrás del torso."], "Rotar excesivamente la columna para ganar recorrido artificial."),
                    ex("Remo en Punta (T-Bar Row) con Apoyo", "4 x 8-10", "120s", "Densidad brutal de espalda media y trapecio sin fatiga lumbar.", ["1. Apoya el pecho firmemente sobre la almohadilla.", "2. Agarra las asas anchas y tira llevando los codos hacia atrás.", "3. Mantén 1 segundo la contracción escapular arriba."], "Despegar el pecho del soporte durante el tirón."),
                    ex("Pull-Over en Polea Alta con Cuerda", "3 x 12-15", "75s", "Aislamiento puro del dorsal ancho sin intervención del bíceps.", ["1. Inclina el torso 30° hacia delante con brazos semirrígidos.", "2. Lleva la cuerda en arco hasta los muslos apretando los dorsales.", "3. Sube controladamente hasta estirar por encima de la cabeza."], "Doblar los codos convirtiendo el ejercicio en extensión de tríceps."),
                    ex("Remo con Mancuerna a una Mano en Banco", "3 x 8-10 / lado", "90s", "Permite mover cargas pesadas con recorrido completo.", ["1. Apoya rodilla y mano del mismo lado sobre un banco plano.", "2. Tira de la mancuerna en diagonal hacia la cadera, no hacia el pecho.", "3. Baja controlando el peso hasta estirar el dorsal."], "Girar el hombro hacia arriba al levantar la mancuerna."),
                    ex("Jalón Unilateral en Polea Alta", "3 x 10-12 / lado", "75s", "Corrige asimetrías y alinea perfectamente las fibras dorsales.", ["1. Arrodíllate o siéntate lateral a la polea alta.", "2. Tira del maneral llevando el codo pegado al costado.", "3. Acompaña el retorno hasta el estiramiento completo."], "Inclinarse lateralmente para bajar el peso."),
                    ex("Remo Gironda Agarre Estrecho Neutro", "3 x 10-12", "90s", "Trabajo equilibrado de dorsal bajo y romboides.", ["1. Mantén el torso vertical con ligera extensión torácica.", "2. Lleva el triángulo hasta el abdomen bajo.", "3. Extiende los brazos hacia delante sin redondear la lumbar."], "Balancearse como un péndulo hacia delante y atrás."),
                    ex("Encogimientos de Trapecio con Mancuernas", "4 x 12-15", "60s", "Construye el yugo superior de espalda y cuello.", ["1. Sujeta dos mancuernas pesadas a los lados con torso ligeramente inclinado.", "2. Eleva los hombros hacia las orejas y ligeramente hacia atrás.", "3. Sostén 2 segundos arriba antes de bajar."], "Rotar los hombros en círculos, lo cual irrita la articulación.")
                ]
            },
            {
                "id": "pierna",
                "muscle": "Pierna Completa (Cuádriceps e Isquios)",
                "svg_type": "squat",
                "biomechanics": "Máxima flexión de rodilla bajo carga para vastos del cuádriceps; bisagra de cadera y flexión de rodilla para isquiosurales.",
                "exercises": [
                    ex("Sentadilla Libre con Barra Trasera", "4 x 6-8", "180s", "Profundidad paralela o superior con core presurizado.", ["1. Coloca la barra sobre los trapecios y toma aire bloqueando el abdomen.", "2. Inicia bajando cadera y rodillas simultáneamente.", "3. Rompe el paralelo manteniendo el peso repartido en todo el pie.", "4. Sube empujando el suelo con fuerza."], "Dejar que las rodillas colapsen hacia dentro (valgo) al subir."),
                    ex("Peso Muerto Rumano con Barra (RDL)", "4 x 8-10", "150s", "Bisagra de cadera pura para isquiosurales y glúteo.", ["1. Con rodillas semirrígidas (15° flexión), empuja la cadera hacia atrás.", "2. Mantén la barra pegada a los muslos y tibias en todo momento.", "3. Baja hasta que tu cadera deje de retroceder (máximo estiramiento isquio).", "4. Extiende la cadera con potencia hasta quedar erguido."], "Bajar más redondeando la espalda baja una vez que la cadera ya no retrocede."),
                    ex("Sentadilla Hack en Máquina", "4 x 8-10", "150s", "Estabilidad total para llevar los cuádriceps al límite.", ["1. Coloca los pies en la zona media-baja de la plataforma.", "2. Baja hasta que los isquios toquen los gemelos.", "3. Empuja sin despegar la zona lumbar del respaldo."], "Despegar los talones de la plataforma en el fondo."),
                    ex("Prensa Inclinada 45°", "3 x 10-12", "120s", "Carga alta en tren inferior sin estrés axial en columna.", ["1. Apoya toda la planta del pie a la anchura de hombros.", "2. Desciende la plataforma controladamente sin levantar el sacro.", "3. Extiende las piernas dejando una microflexión de rodilla arriba."], "Bloquear completamente las rodillas en hiperextensión arriba."),
                    ex("Curl Femoral Sentado en Máquina", "4 x 10-12", "90s", "Trabaja el isquio en posición estirada (mayor hipertrofia).", ["1. Ajusta el rodillo sobre los tobillos y fija bien el soporte de muslos.", "2. Flexiona las rodillas llevando los talones debajo del asiento.", "3. Regresa en 3 segundos resistiendo el peso."], "Levantar los glúteos del asiento al iniciar la flexión."),
                    ex("Extensión de Cuádriceps en Máquina", "4 x 12-15", "75s", "Aísla el recto femoral y vastos con pico de contracción.", ["1. Alinea el eje de la máquina exactamente con tu rodilla.", "2. Extiende hasta bloquear arriba y sostén 1 segundo.", "3. Baja de forma controlada sin que las placas choquen."], "Dar patadas bruscas usando inercia."),
                    ex("Zancadas Caminando con Mancuernas", "3 x 12 pasos / pierna", "90s", "Estímulo unilateral completo de cuádriceps y glúteo.", ["1. Da un paso amplio manteniendo el torso erguido.", "2. Baja hasta que la rodilla trasera roce el suelo.", "3. Impúlsate con el talón de la pierna delantera."], "Cruzar los pies en línea recta perdiendo el equilibrio."),
                    ex("Curl Femoral Tumbado", "3 x 10-12", "90s", "Énfasis en la porción corta del bíceps femoral.", ["1. Mantén la cadera pegada al banco durante todo el recorrido.", "2. Lleva los talones hacia los glúteos.", "3. Desciende lentamente."], "Arquear la zona lumbar levantando la pelvis al subir."),
                    ex("Elevación de Talones de Pie (Gemelo)", "4 x 12-15", "60s", "Pausa de 2 segundos abajo para eliminar el rebote del tendón de Aquiles.", ["1. Baja los talones todo lo posible y mantén 2 segundos estirado.", "2. Sube hasta quedar sobre la punta de los dedos.", "3. Sostén 1 segundo arriba."], "Rebotar rápido arriba y abajo sin pausa."),
                    ex("Gemelo Sentado en Máquina", "3 x 15-20", "60s", "Enfocado específicamente en el sóleo.", ["1. Coloca la almohadilla sobre los muslos cerca de las rodillas.", "2. Realiza recorrido completo desde estiramiento máximo hasta contracción."], "Hacer repeticiones cortas sin llegar al estiramiento inferior.")
                ]
            },
            {
                "id": "gluteo",
                "muscle": "Glúteo (Potencia y Proyección)",
                "svg_type": "hip_thrust",
                "biomechanics": "Extensión de cadera con pico de tensión en acortamiento (Hip Thrust) combinada con estiramiento bajo carga (Búlgara) y abducción.",
                "exercises": [
                    ex("Hip Thrust con Barra Olímpica", "4 x 8-10", "150s", "Retroversión pélvica arriba y pausa de 2 segundos.", ["1. Apoya el borde inferior de las escápulas en el banco.", "2. Coloca las espinillas verticales cuando la cadera esté arriba.", "3. Empuja con los talones manteniendo la barbilla pegada al pecho.", "4. Contrae los glúteos al máximo arriba durante 2 segundos."], "Mirar hacia el techo hiperextendiendo la zona lumbar."),
                    ex("Sentadilla Búlgara con Mancuernas", "3 x 8-10 / lado", "90s", "Paso largo e inclinación leve del torso para glúteo mayor.", ["1. Apoya el empeine trasero en un banco bajo.", "2. Inclina el torso 15° hacia delante y baja profundo.", "3. Sube empujando exclusivamente con la pierna delantera."], "Empujar con el pie de atrás en lugar del delantero."),
                    ex("Peso Muerto Rumano con Mancuernas", "4 x 10", "120s", "Elongación máxima de fibras inferiores del glúteo.", ["1. Empuja la cadera hacia atrás manteniendo espinillas verticales.", "2. Baja hasta la mitad de la espinilla con espalda plana.", "3. Sube contrayendo glúteos sin hiperextender la espalda."], "Flexionar demasiado las rodillas convirtiéndolo en sentadilla."),
                    ex("Patada de Glúteo en Polea Baja", "3 x 12-15 / lado", "60s", "Extensión diagonal a 30° siguiendo las fibras del glúteo.", ["1. Coloca la tobillera e inclina ligeramente el torso apoyado en la estructura.", "2. Extiende la pierna hacia atrás y ligeramente hacia fuera.", "3. Regresa sin perder tensión en el cable."], "Arquear la espalda baja para levantar más la pierna."),
                    ex("Abducción de Cadera en Máquina", "4 x 15-20", "60s", "Construye el glúteo medio y la redondez lateral.", ["1. Siéntate inclinando el torso ligeramente hacia delante.", "2. Abre las piernas con fuerza y mantén 1 segundo abierto.", "3. Cierra de forma controlada."], "Usar impulso del torso para abrir las almohadillas."),
                    ex("Hiperextensiones 45° Enfoque Glúteo", "3 x 12-15", "75s", "Pies ligeramente rotados hacia fuera y espalda alta redondeada.", ["1. Ajusta el soporte por debajo de la cadera.", "2. Baja con la espalda alta ligeramente redondeada para desactivar lumbares.", "3. Sube contrayendo únicamente los glúteos."], "Subir arqueando excesivamente la zona lumbar."),
                    ex("Step-Up Alto en Cajón (Subida al Banco)", "3 x 10 / lado", "75s", "Máxima flexión de cadera con control excéntrico lento.", ["1. Coloca un pie completo sobre un cajón a la altura de la rodilla.", "2. Sube sin impulsarte con la pierna del suelo.", "3. Baja en 3 segundos controlados."], "Saltar con el pie de apoyo inferior."),
                    ex("Puente de Glúteo en Máquina (Glute Drive)", "3 x 10-12", "120s", "Tensión constante y comodidad lumbar.", ["1. Abrocha el cinturón firmemente sobre la pelvis.", "2. Empuja con los talones hasta alinear rodillas, cadera y hombros.", "3. Pausa de 1 segundo arriba."], "Colocar los pies demasiado cerca o demasiado lejos."),
                    ex("Abducción en Polea Baja de Pie", "3 x 15 / lado", "60s", "Estabilidad pélvica y trabajo profundo de glúteo medio.", ["1. Sujétate a la columna de la polea.", "2. Eleva la pierna lateralmente unos 45° sin inclinar el torso.", "3. Baja despacio."], "Inclinar el tronco hacia el lado contrario."),
                    ex("Pull-Through en Polea Baja con Cuerda", "3 x 12-15", "75s", "Patrón de bisagra con resistencia horizontal continua.", ["1. Da dos pasos hacia delante de espaldas a la polea baja.", "2. Lleva la cuerda entre las piernas empujando la cadera atrás.", "3. Extiende la cadera con fuerza apretando glúteos."], "Tirar de la cuerda con los brazos.")
                ]
            },
            {
                "id": "brazo",
                "muscle": "Brazo Completo (Bíceps, Tríceps y Braquial)",
                "svg_type": "bicep_curl",
                "biomechanics": "El tríceps supone dos tercios del perímetro del brazo. Combinar estiramiento (cabeza larga) y acortamiento maximiza el tamaño.",
                "exercises": [
                    ex("Curl en Banco Inclinado 45° con Mancuernas", "4 x 8-10", "90s", "Estira la cabeza larga del bíceps detrás del torso.", ["1. Apoya la espalda en un banco a 45-60° dejando colgar los brazos.", "2. Supina las muñecas al subir sin adelantar los codos.", "3. Baja hasta la extensión completa en 3 segundos."], "Adelantar los codos hacia delante al subir las mancuernas."),
                    ex("Press Francés con Barra Z en Banco", "4 x 8-10", "90s", "Lleva la barra detrás de la cabeza para tensión continua en tríceps.", ["1. Túmbate y lleva los brazos ligeramente inclinados hacia atrás.", "2. Flexiona los codos bajando la barra detrás de la coronilla.", "3. Extiende los brazos manteniendo los codos apuntando al techo."], "Abrir los codos hacia los lados al bajar."),
                    ex("Curl con Barra Recta o Barra Z de Pie", "4 x 8-10", "90s", "Sobrecarga progresiva directa sobre ambas cabezas del bíceps.", ["1. Sujeta la barra a la anchura de hombros con codos pegados al costado.", "2. Sube la barra contrayendo el bíceps sin balancear el torso.", "3. Desciende controladamente."], "Usar impulso lumbar echando el cuerpo hacia atrás."),
                    ex("Extensión de Tríceps en Polea Alta (Barra V)", "4 x 10-12", "75s", "Bloqueo de codos a los costados y extensión completa.", ["1. Inclínate ligeramente hacia delante con los codos pegados a las costillas.", "2. Empuja la barra hacia abajo hasta bloquear los tríceps.", "3. Sube hasta formar un ángulo de 90° en el codo."], "Dejar que los codos se desplacen hacia delante al subir."),
                    ex("Curl Martillo en Polea con Cuerda", "3 x 10-12", "75s", "Desarrolla el braquial anterior y braquiorradial (grosor lateral).", ["1. Sujeta la cuerda con agarre neutro (palmas enfrentadas).", "2. Sube las manos hacia los hombros separando ligeramente la cuerda arriba.", "3. Baja resistiendo el cable."], "Girar las muñecas perdiendo el agarre neutro."),
                    ex("Extensión de Tríceps Sobre la Cabeza en Polea", "3 x 12-15", "75s", "Máximo estiramiento de la cabeza larga del tríceps.", ["1. De espaldas a la polea, lleva los brazos por encima de la cabeza.", "2. Extiende completamente los codos hacia delante y arriba.", "3. Flexiona detrás de la cabeza sintiendo el estiramiento."], "Arquear la zona lumbar durante el empuje."),
                    ex("Curl Predicador (Banco Scott) Unilateral", "3 x 10-12 / lado", "75s", "Elimina cualquier trampa y ataca la porción corta del bíceps.", ["1. Apoya toda la parte posterior del brazo sobre el pupitre.", "2. Baja hasta casi extender el brazo sin golpear el codo.", "3. Sube hasta la vertical."], "Despegar el codo del apoyo acolchado."),
                    ex("Fondos entre Bancos o Máquina de Tríceps", "3 x 10-12", "90s", "Gran densidad en las tres cabezas del tríceps.", ["1. Mantén el torso erguido y los codos apuntando hacia atrás.", "2. Baja hasta 90° y extiende con fuerza."], "Adelantar demasiado los hombros estresando la cápsula anterior."),
                    ex("Curl Araña (Spider Curl) en Banco Inclinado", "3 x 12", "60s", "Pico de contracción máximo en acortamiento.", ["1. Apoya el pecho sobre un banco inclinado dejando brazos verticales.", "2. Sube las mancuernas apretando 1 segundo arriba."], "Balancear los brazos como un péndulo."),
                    ex("Curl Invertido con Barra Z (Antebrazo)", "3 x 12-15", "60s", "Fortalece braquiorradial y extensores de muñeca.", ["1. Agarra la barra en pronación (palmas hacia abajo).", "2. Sube manteniendo las muñecas rectas y firmes."], "Doblar las muñecas hacia abajo al subir.")
                ]
            },
            {
                "id": "hombro",
                "muscle": "Deltoides 3D (Estética Classic Physique)",
                "svg_type": "lateral_raise",
                "biomechanics": "El deltoides lateral crea la amplitud clavicular y el aspecto 3D; el posterior equilibra la postura escapular.",
                "exercises": [
                    ex("Press Militar Sentado con Mancuernas", "4 x 6-8", "120s", "Codos en plano escapular (30° hacia delante).", ["1. Coloca el respaldo a 80-85° y apoya firmemente la espalda.", "2. Lleva los codos ligeramente adelantados respecto al torso.", "3. Empuja hasta que las mancuernas queden sobre la cabeza sin chocarlas."], "Abrir los codos completamente en línea recta con las orejas."),
                    ex("Elevaciones Laterales en Polea a la Altura de Muñeca", "4 x 12-15", "60s", "Tensión continua desde el primer grado de abducción.", ["1. Coloca la polea a la altura de tu muñeca.", "2. Eleva el brazo hacia el lado liderando con el codo hasta la altura del hombro.", "3. Baja en 3 segundos sin dejar caer el peso."], "Encoger el trapecio hacia el cuello al subir."),
                    ex("Elevaciones Laterales con Mancuernas Sentado", "4 x 12-15", "60s", "Elimina el impulso de piernas para aislar el deltoides medio.", ["1. Siéntate al borde del banco con leve inclinación frontal.", "2. Sube las mancuernas hacia los lados como si vertieras dos jarras.", "3. Detente a la altura de los hombros y baja despacio."], "Balancear el tronco hacia atrás para lanzar las mancuernas."),
                    ex("Pájaros en Máquina Contractora Inversa", "4 x 12-15", "60s", "Aísla el deltoides posterior sin retracción escapular excesiva.", ["1. Ajusta el asiento para que los brazos queden paralelos al suelo.", "2. Empuja hacia los lados pensando en alejar las manos del cuerpo.", "3. Controla el regreso sin juntar las placas."], "Juntar demasiado las escápulas, lo que traslada el trabajo al romboides."),
                    ex("Face Pull en Polea Alta con Cuerda", "4 x 15", "60s", "Salud del manguito rotador y densidad posterior.", ["1. Agarra la cuerda con pulgares apuntando hacia atrás.", "2. Tira hacia la frente separando las manos y rotando externamente.", "3. Sostén 1 segundo atrás."], "Tirar hacia el pecho en lugar de hacia la frente."),
                    ex("Press Militar de Pie con Barra Olímpica", "4 x 6-8", "150s", "Fuerza estructural de hombro y estabilidad de core.", ["1. Aprieta glúteos y abdomen para evitar arquear la lumbar.", "2. Empuja la barra en línea recta pasando cerca de la barbilla.", "3. Mete ligeramente la cabeza al pasar la barra."], "Convertir el ejercicio en un press inclinado arqueando la espalda."),
                    ex("Remo al Mentón Agarre Ancho con Barra Z", "3 x 10-12", "75s", "Sube solo hasta la línea del pecho liderando con los codos.", ["1. Sujeta la barra Z a una anchura ligeramente superior a los hombros.", "2. Eleva los codos hacia los lados hasta la altura del pecho.", "3. Baja controladamente."], "Subir la barra hasta la barbilla con agarre muy estrecho."),
                    ex("Elevaciones Laterales Unilaterales Inclinado", "3 x 12-15 / lado", "60s", "Maximiza la tensión en el tramo más difícil del movimiento.", ["1. Sujétate a un poste con una mano e inclina el cuerpo 20°.", "2. Eleva la mancuerna hasta la horizontal."], "Usar un peso que obligue a doblar excesivamente el codo."),
                    ex("Pájaros con Mancuernas Pecho Apoyado", "3 x 12-15", "60s", "Cero impulso lumbar y aislamiento posterior total.", ["1. Apoya el pecho en un banco inclinado a 30°.", "2. Abre los brazos hacia los lados con codos semiflexionados."], "Subir las mancuernas hacia atrás pegadas al cuerpo."),
                    ex("Press Arnold con Mancuernas", "3 x 10-12", "90s", "Recorrido amplio que activa deltoides anterior y lateral.", ["1. Inicia con las palmas mirando hacia ti frente a los hombros.", "2. Rota las muñecas hacia fuera mientras empujas arriba."], "Hacer la rotación demasiado brusca con exceso de peso.")
                ]
            }
        ],
        "american_ppl": {
            "title": "Protocolo Americano Push / Pull / Legs (PPL)",
            "description": "Sistema estándar en culturismo moderno. Agrupa músculos por patrón biomecánico sinérgico, permitiendo alta intensidad y recuperación limpia.",
            "blocks": [
                {"tag": "PUSH (Empuje)", "muscles": "Pectoral + Deltoides Anterior/Lateral + Tríceps", "routine": ["1. Press Inclinado Mancuernas (30°): 4 x 8-10 (Descanso 120s)", "2. Press Banca Plano con Barra: 4 x 6-8 (Descanso 150s)", "3. Elevaciones Laterales en Polea: 4 x 12-15 (Descanso 60s)", "4. Cruces en Polea Alta a Baja: 3 x 12-15 (Descanso 75s)", "5. Extensión de Tríceps en Polea Alta: 4 x 10-12 (Descanso 75s)"]},
                {"tag": "PULL (Tracción)", "muscles": "Dorsal Ancho + Trapecio + Deltoides Posterior + Bíceps", "routine": ["1. Dominadas Lastradas o Jalón Pecho: 4 x 6-8 (Descanso 120s)", "2. Remo con Barra Inclinado: 4 x 8-10 (Descanso 150s)", "3. Remo Unilateral en Polea Baja: 3 x 10-12 (Descanso 90s)", "4. Face Pull en Polea Alta: 4 x 15 (Descanso 60s)", "5. Curl Bíceps Banco Inclinado 45°: 4 x 8-10 (Descanso 75s)"]},
                {"tag": "LEGS (Tren Inferior)", "muscles": "Cuádriceps + Isquiosurales + Glúteo + Gemelo", "routine": ["1. Sentadilla Libre o Hack Squat: 4 x 6-8 (Descanso 180s)", "2. Peso Muerto Rumano con Barra: 4 x 8-10 (Descanso 150s)", "3. Prensa Inclinada 45°: 3 x 10-12 (Descanso 120s)", "4. Curl Femoral Tumbado: 3 x 12 (Descanso 75s)", "5. Elevación de Talones de Pie: 4 x 12-15 (Descanso 60s)"]}
            ]
        },
        "frequency_specialization": [
            {"name": "Bloque 01 • Frecuencia 2 Global (Equilibrio Simétrico)", "split": "Torso / Pierna / Descanso / Push / Pull / Legs", "weekly_sets": "14-16 series efectivas por grupo muscular", "ideal_for": "Hipertrofia equilibrada en todo el cuerpo sin fatiga excesiva del SNC."},
            {"name": "Bloque 02 • Especialización Frecuencia 3 en Brazos", "split": "Día 1: Brazos+Hombro | Día 2: Pierna | Día 3: Torso+Bíceps | Día 4: Descanso | Día 5: Brazos+Hombro | Día 6: Pierna", "weekly_sets": "20-22 series semanales en Bíceps y Tríceps; 8 series de mantenimiento en el resto.", "ideal_for": "Aumentar el perímetro de brazo en ciclos de 6 a 8 semanas."},
            {"name": "Bloque 03 • Especialización Frecuencia 3 en Pierna y Glúteo", "split": "Día 1: Cuádriceps | Día 2: Torso | Día 3: Glúteo e Isquios | Día 4: Descanso | Día 5: Pierna Completa | Día 6: Torso", "weekly_sets": "22 series semanales en tren inferior; mantenimiento en tren superior.", "ideal_for": "Densidad máxima de cuádriceps, femorales y proyección glútea."},
            {"name": "Bloque 04 • Especialización Amplitud V-Taper (Hombro + Dorsal)", "split": "Frecuencia 3 en Deltoides Lateral y Dorsal; Frecuencia 1.5 en Pecho/Pierna", "weekly_sets": "20 series en deltoides lateral y dorsal.", "ideal_for": "Crear cintura visualmente estrecha y hombros 3D."},
            {"name": "Bloque 05 • Especialización Pectoral Superior (Clavicular)", "split": "Lunes: Pecho Inclinado | Miércoles: Pecho Poleas/Mancuernas | Viernes: Torso Completo", "weekly_sets": "18-20 series semanales en pectoral.", "ideal_for": "Rellenar la parte alta del pecho bajo las clavículas."},
            {"name": "Bloque 06 • Especialización Espalda Densidad y Grosor", "split": "3 sesiones semanales alternando tracciones verticales y remos pesados", "weekly_sets": "20 series semanales en dorsal, trapecio y romboides.", "ideal_for": "Lograr profundidad muscular en la espalda vista de perfil."},
            {"name": "Bloque 07 • Especialización Glúteo Estético", "split": "Lunes: Empuje de cadera pesado | Miércoles: Unilateral | Viernes: Abducción y metabólico", "weekly_sets": "18-22 series semanales directas en glúteo.", "ideal_for": "Maximizar fuerza y forma en glúteo mayor y medio."},
            {"name": "Bloque 08 • Bloque de Fuerza Pura (Básicos)", "split": "4 días centrados en progresión lineal 5x5 en Sentadilla, Banca y Peso Muerto", "weekly_sets": "12-15 series pesadas al 80-87% 1RM.", "ideal_for": "Elevar los techos de fuerza antes de una fase de volumen."},
            {"name": "Bloque 09 • Definición (Mantenimiento de Carga Pesada)", "split": "Torso / Pierna 4 días manteniendo pesos altos y reduciendo volumen un 20%", "weekly_sets": "10-12 series muy intensas por grupo muscular.", "ideal_for": "Retener el 100% de la masa muscular en déficit calórico."},
            {"name": "Bloque 10 • Descarga Estratégica (Deload Week)", "split": "3-4 días al 60% del volumen habitual y RIR 3-4", "weekly_sets": "6-8 series por grupo muscular.", "ideal_for": "Disipar fatiga acumulada cada 8-10 semanas y supercompensar."}
        ]
    }
