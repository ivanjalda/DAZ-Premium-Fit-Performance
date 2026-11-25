import os
import json
import hashlib
import datetime
import subprocess

DATA_DIR = "data"
REQUIRED_JSONS = [
    "nutrition_matrix.json",
    "fitness_plans.json",
    "supplement_analysis.json",
    "marketing_showcase.json",
    "blog_posts.json"
]
REQUIRED_HTMLS = [
    "index.html",
    "entrenamiento.html",
    "nutricion.html",
    "suplementacion.html",
    "ciencia.html",
    "nav.js"
]


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_previous_hashes():
    path = os.path.join(DATA_DIR, "revision_huellas.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    errors = []
    repaired = False

    # 1. Verificar existencia y validez de los JSON; auto-reparar si falta alguno
    for jname in REQUIRED_JSONS:
        jpath = os.path.join(DATA_DIR, jname)
        needs_repair = False
        if not os.path.exists(jpath) or os.path.getsize(jpath) < 100:
            needs_repair = True
        else:
            try:
                with open(jpath, "r", encoding="utf-8") as f:
                    json.load(f)
            except Exception:
                needs_repair = True

        if needs_repair:
            print(f"[REVISOR] Fallo detectado en {jname}. Ejecutando auto-reparación...")
            subprocess.run(["python", "scripts/engine.py"], check=True)
            repaired = True
            break

    # 2. Verificar integridad de las páginas HTML y nav.js
    for hname in REQUIRED_HTMLS:
        if not os.path.exists(hname) or os.path.getsize(hname) < 200:
            errors.append(f"Archivo estructural ausente o incompleto: {hname}")
        elif hname.endswith(".html"):
            with open(hname, "r", encoding="utf-8") as f:
                content = f.read()
            if "nav.js" not in content or "</html>" not in content:
                errors.append(f"Estructura HTML incompleta en {hname}")

    # 3. Calcular huellas SHA-256 actuales y comparar con las anteriores
    prev_hashes = load_previous_hashes()
    current_hashes = {}
    changed_files = []

    for jname in REQUIRED_JSONS:
        jpath = os.path.join(DATA_DIR, jname)
        if os.path.exists(jpath):
            digest = sha256_file(jpath)
            current_hashes[jpath] = digest
            if prev_hashes.get(jpath) != digest:
                changed_files.append(jpath)

    for hname in REQUIRED_HTMLS:
        if os.path.exists(hname):
            digest = sha256_file(hname)
            current_hashes[hname] = digest
            if prev_hashes.get(hname) != digest:
                changed_files.append(hname)

    with open(os.path.join(DATA_DIR, "revision_huellas.json"), "w", encoding="utf-8") as f:
        json.dump(current_hashes, f, indent=2)

    estado = "OK" if not errors else "ALERTA"
    if repaired:
        estado = "AUTO-REPARADO OK"

    report = {
        "fecha_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "estado": estado,
        "archivos_verificados": len(REQUIRED_JSONS),
        "paginas_verificadas": len(REQUIRED_HTMLS),
        "cambios_detectados": changed_files,
        "errores": errors
    }

    with open(os.path.join(DATA_DIR, "revision.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[REVISOR] Auditoría completada -> Estado: {estado} | Cambios: {len(changed_files)}")


if __name__ == "__main__":
    main()
