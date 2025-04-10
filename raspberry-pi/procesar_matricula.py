import os
import subprocess
import requests
import time
from datetime import datetime

# Dirección del servidor en DigitalOcean
SERVIDOR = "https://matriculas.dsermar0808.tech/recibir_matricula"

def capturar_imagen():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"captura_{timestamp}.jpg"
    ruta = os.path.join("imagenes", nombre_archivo)
    os.system(f"fswebcam -r 1280x720 --no-banner {ruta}")
    return ruta

def detectar_matricula(imagen):
    resultado = subprocess.run(["alpr", "-c", "eu", imagen], capture_output=True, text=True)
    lineas = resultado.stdout.split("\n")
    if len(lineas) > 1 and len(lineas[1].split()) > 1:
        return lineas[1].split()[1]  # Extrae la matrícula detectada
    return None

def enviar_matricula(matricula):
    datos = {
        "matricula": matricula,
        "imagen": os.path.basename(imagen),
        }
    try:
        respuesta = requests.post(SERVIDOR, json=datos, timeout=5)
        print("📡 Respuesta del servidor:", respuesta.json())
    except requests.exceptions.RequestException as e:
        print("❌ Error enviando matrícula:", e)

if __name__ == "__main__":
    ultimo_matricula = None
    
    while True:
        print("📸 Capturando imagen...")
        imagen = capturar_imagen()

        print("🔍 Detectando matrícula...")
        matricula_detectada = detectar_matricula(imagen)

        if matricula_detectada:
            print(f"🚗 Matrícula detectada: {matricula_detectada}")
            enviar_matricula(matricula_detectada)
            ultimo_matricula = matricula_detectada
            
        else:
            print("⚠️ No se detectó ninguna matrícula.")
            ultimo_matricula = None

<<<<<<< HEAD
        time.sleep(1)  # Espera 1 segundos antes de volver a capturar
=======
        time.sleep(1)  # Espera 1 segundo antes de volver a capturar
>>>>>>> 50aa593bd2b567af16a8cd257b86669ff5c6200a

