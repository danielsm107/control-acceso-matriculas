# Explicación del script procesar_matricula.py
## Descripción

Este script se ejecuta en una **Raspberry Pi** y se encarga de:  
1. **Capturar una imagen** con la cámara utilizando `fswebcam`.  
2. **Detectar la matrícula** en la imagen usando OpenALPR.  
3. **Enviar la matrícula** a un servidor remoto en DigitalOcean para su validación.  
4. **Ejecutarse en bucle**, repitiendo el proceso cada 5 segundos.

---

## **Explicación del código**

### **1️. Importación de módulos**

```python
import os
import subprocess
import requests
import time
```

El script usa las siguientes librerías:

- **`os`** → Para ejecutar comandos del sistema (captura de imagen).
- **`subprocess`** → Para ejecutar OpenALPR y procesar la imagen.
- **`requests`** → Para enviar la matrícula detectada al servidor.
- **`time`** → Para pausar la ejecución y hacer que el script corra en intervalos.

### **2️. Configuración del servidor**

```python
SERVIDOR = "http://209.38.115.116:5000/recibir_matricula"
```

**Esta variable almacena la URL del servidor** en DigitalOcean, donde se enviarán las matrículas detectadas.

### **3️. Función para capturar una imagen**

```python
def capturar_imagen():
    imagen = "captura.jpg"
    os.system("fswebcam -r 1280x720 --no-banner " + imagen)  # Captura imagen con fswebcam
    return imagen
```

**¿Qué hace?**  
1. Toma una **foto** con la cámara usando `fswebcam`.  
2. Guarda la imagen con el nombre `"captura.jpg"`.  
3. **Evita mostrar texto sobre la imagen** (`--no-banner`).

### **4️. Función para detectar la matrícula en la imagen**

```python
def detectar_matricula(imagen):
    resultado = subprocess.run(["alpr", "-c", "eu", imagen], capture_output=True, text=True)
    lineas = resultado.stdout.split("\n")
    if len(lineas) > 1 and len(lineas[1].split()) > 1:
        return lineas[1].split()[1]  # Extrae la matrícula detectada
    return None
```

**¿Qué hace?**  
1. Usa **OpenALPR** (`alpr -c eu`) para **analizar la imagen** y buscar una matrícula.  
2. **Si se detecta una matrícula**, devuelve el número de la matrícula sin espacios.  
3. **Si no se detecta**, devuelve `None`.

### **5️. Función para enviar la matrícula al servidor**

```python
def enviar_matricula(matricula):
    datos = {"matricula": matricula}
    try:
        respuesta = requests.post(SERVIDOR, json=datos, timeout=5)
        print("📡 Respuesta del servidor:", respuesta.json())
    except requests.exceptions.RequestException as e:
        print("❌ Error enviando matrícula:", e)
```

**¿Qué hace?**  
1. **Envía la matrícula detectada** al servidor a través de una petición HTTP `POST`.  
2. Si la conexión falla, muestra un **mensaje de error**.

### **6️. Bucle principal**

```python
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
```

**¿Qué hace?**  
1. **Captura una imagen** cada 5 segundos.  
2. **Detecta la matrícula** y la envía al servidor si existe.  
3. **Muestra mensajes en la terminal** para indicar el estado del proceso.

---

## **Resumen del flujo del script**

1. **Captura una imagen con la cámara (`fswebcam`).**  
2. **Analiza la imagen con OpenALPR para detectar una matrícula.**  
3. **Si se detecta una matrícula, la envía al servidor en DigitalOcean.**  
4. **Repite el proceso cada 5 segundos.**

