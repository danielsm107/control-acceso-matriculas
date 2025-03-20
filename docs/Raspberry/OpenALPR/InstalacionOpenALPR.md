# Instalación de OpenALPR en Ubuntu Server

## **Requisitos previos**

- Un servidor con **Ubuntu Server** instalado (versión 20.04 o superior recomendada).
- Acceso a una terminal con permisos de superusuario (`sudo`).
- Conexión a Internet para descargar dependencias.

---

## **1\. Actualizar el sistema**

Antes de comenzar, asegúrate de que tu sistema esté actualizado:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## **2\. Instalar dependencias**

OpenALPR requiere varias dependencias para funcionar correctamente. Instálalas ejecutando el siguiente comando:

```bash
sudo apt install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev liblog4cplus-dev libcurl3-dev
```

- **build-essential**: Herramientas de compilación (gcc, make, etc.).
- **cmake**: Herramienta para gestionar la compilación.
- **git**: Para clonar el repositorio de OpenALPR.
- **libopencv-dev**: Bibliotecas de OpenCV para procesamiento de imágenes.
- **libtesseract-dev**: Motor de reconocimiento óptico de caracteres (OCR).
- **libleptonica-dev**: Bibliotecas para procesamiento de imágenes (requeridas por Tesseract).
- **liblog4cplus-dev**: Bibliotecas para logging.
- **libcurl4-openssl-dev**: Bibliotecas para manejar solicitudes HTTP.

---

## **3\. Clonar el repositorio de OpenALPR**

Clona el repositorio oficial de OpenALPR desde GitHub:

```bash
git clone https://github.com/openalpr/openalpr.git
```

---

## **4\. Compilar OpenALPR**

Sigue estos pasos para compilar OpenALPR desde el código fuente:

### a) Crear un directorio de compilación

```bash
cd openalpr/src
mkdir build
cd build
```

### b) Configurar CMake

Ejecuta CMake para configurar el proyecto:

```bash
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
```

- `-DCMAKE_INSTALL_PREFIX:PATH=/usr`: Instala OpenALPR en el directorio `/usr`.
- `-DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc`: Coloca los archivos de configuración en `/etc`.

### c) Compilar el proyecto

Compila OpenALPR usando `make`:

```bash
make
```

Este proceso puede tardar varios minutos, dependiendo del rendimiento de tu servidor.

### d) Instalar OpenALPR

Una vez que la compilación haya terminado, instala OpenALPR en el sistema:

```bash
sudo make install
```

---

## **5\. Verificar la instalación**

Para asegurarte de que OpenALPR se ha instalado correctamente, ejecuta el siguiente comando:

```bash
alpr --version
```

Deberías ver la versión de OpenALPR instalada, por ejemplo:

```bash
alpr 2.3.0
```

---

## **6\. Probar OpenALPR con una imagen**

Para probar que OpenALPR funciona correctamente, usa una imagen que contenga una matrícula.

### a) Descargar una imagen de prueba

Puedes usar una imagen de matrícula desde Internet o crear la tu propia. Por ejemplo:

```bash
wget https://ejemplo.com/ruta/a/imagen.jpg
```

### b) Analizar la imagen con OpenALPR

Ejecuta el siguiente comando para analizar la imagen:

```bash
alpr -c eu imagen.jpg
```

- `-c eu`: Especifica que se usará el modelo de reconocimiento para matrículas europeas (incluye España).
- `imagen.jpg`: Es la imagen que contiene la matrícula.

### c) Ejemplo de salida

Si la matrícula es reconocida correctamente, verás una salida similar a esta:

```bash
plate0: 10 resultados
    - ABC1234     confianza: 92.5%
    - ABC123      confianza: 88.2%
    - ABC12       confianza: 85.0%
```


---

## **7\. Automatizar el proceso con un script en Python**

Puedes automatizar el análisis de matrículas usando Python para llamar a OpenALPR. Aquí tienes un ejemplo de script:

```python
import subprocess

def analizar_matricula(imagen):
    # Ejecutar OpenALPR desde Python
    resultado = subprocess.run(['alpr', '-c', 'eu', imagen], capture_output=True, text=True)
    
    # Mostrar la salida de OpenALPR
    if resultado.returncode == 0:
        print(resultado.stdout)
    else:
        print("Error al analizar la matrícula:", resultado.stderr)

# Llamar a la función con una imagen
analizar_matricula('imagen.jpg')
```

---

## **8\. Posibles problemas

Si encuentras algún problema durante la instalación o el uso de OpenALPR, aquí tienes algunas soluciones comunes:

#### a) **Error de dependencias faltantes**

Si falta alguna dependencia, instálala manualmente usando `apt`. Por ejemplo:

```bash
sudo apt install libopencv-dev
```

#### b) **Problemas de compilación**

Si la compilación falla, asegúrate de que todas las dependencias estén instaladas y que estás usando una versión compatible de Ubuntu.

#### c) **Baja precisión en el reconocimiento**

- Asegúrate de usar imágenes de alta calidad.
- Recorta la imagen para que la matrícula ocupe la mayor parte del frame.
- Ajusta el contraste y el brillo de la imagen.

