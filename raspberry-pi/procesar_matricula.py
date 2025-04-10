import os
import subprocess
import requests
import time

SERVIDOR = "https://matriculas.dsermar0808.tech/recibir_matricula"
CAPTURA = "captura.jpg"

def capturar_imagen():
    os.system(f"fswebcam -r 1280x720 --no-banner {CAPTURA}")
    return CAPTURA

def detectar_matricula(imagen):
    resultado = subprocess.run(["alpr", "-c", "eu", imagen], capture_output=True, text=True)
    lineas = resultado.stdout.split("\n")
    if len(lineas) > 1 and len(lineas[1].split()) > 1:
        return lineas[1].split()[1]
    return None

def enviar_matricula(matricula, imagen):
    try:
        with open(imagen, "rb") as archivo_imagen:
            archivos = {'imagen': archivo_imagen}
            datos = {'matricula': matricula}
            respuesta = requests.post(SERVIDOR, files=archivos, data=datos, timeout=5)
            print("📡 Respuesta del servidor:", respuesta.json())
    except Exception as e:
        print("❌ Error enviando datos:", e)

if __name__ == "__main__":
    ultima_matricula = None

    while True:
        print("📸 Capturando imagen...")
        imagen = capturar_imagen()

        print("🔍 Detectando matrícula...")
        matricula_detectada = detectar_matricula(imagen)

        if matricula_detectada:
            print(f"🚗 Matrícula detectada: {matricula_detectada}")
            if matricula_detectada != ultima_matricula:
                enviar_matricula(matricula_detectada, imagen)
                ultima_matricula = matricula_detectada
            else:
                print("⏩ Matrícula repetida, no se envía de nuevo.")
        else:
            print("⚠️ No se detectó ninguna matrícula.")
            ultima_matricula = None

        time.sleep(1)
