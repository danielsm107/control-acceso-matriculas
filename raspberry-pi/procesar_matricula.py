import os
import subprocess
import requests
import time

# Dirección del servidor en DigitalOcean
SERVIDOR = "https://matriculas.dsermar0808.tech/recibir_matricula"

def capturar_imagen():
    imagen = "captura.jpg"
    os.system("fswebcam -r 1280x720 --no-banner " + imagen)  # Captura imagen con fswebcam
    return imagen

def detectar_matricula(imagen):
    resultado = subprocess.run(["alpr", "-c", "eu", imagen], capture_output=True, text=True)
    lineas = resultado.stdout.split("\n")
    if len(lineas) > 1 and len(lineas[1].split()) > 1:
        return lineas[1].split()[1]  # Extrae la matrícula detectada
    return None

def enviar_matricula(matricula):
    datos = {"matricula": matricula}
    try:
        respuesta = requests.post(SERVIDOR, json=datos, timeout=5)
        print("📡 Respuesta del servidor:", respuesta.json())
    except requests.exceptions.RequestException as e:
        print("❌ Error enviando matrícula:", e)

if __name__ == "__main__":
    while True:
        print("📸 Capturando imagen...")
        imagen = capturar_imagen()

        print("🔍 Detectando matrícula...")
        matricula_detectada = detectar_matricula(imagen)

        if matricula_detectada:
            print(f"🚗 Matrícula detectada: {matricula_detectada}")
            enviar_matricula(matricula_detectada)
        else:
            print("⚠️ No se detectó ninguna matrícula.")

        time.sleep(5)  # Espera 5 segundos antes de volver a capturar

