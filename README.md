# **Sistema de Control de Acceso por Reconocimiento de Matrículas**

**Autor:** Daniel Serrano Marín

**I.E.S. Francisco Romero Vargas**
**Administración de Sistemas Informáticos en Red**
**Curso: 2024/2025**


## **1. Introducción**

Este proyecto consiste en un **sistema de control de acceso** basado en el reconocimiento automático de matrículas (LPR - License Plate Recognition).

El sistema capturará imágenes de matrículas mediante una **cámara conectada a una Raspberry Pi**. A través de **OpenALPR**, se detectará la matrícula y se comparará con una **base de datos MySQL** para determinar si el acceso es autorizado o denegado.

Además, los usuarios podrán **solicitar el registro de su matrícula** mediante una aplicación web, y un administrador podrá aprobar o rechazar el acceso.


## **2. Finalidad**

El objetivo principal es mejorar la **automatización del acceso** mediante el reconocimiento de matrículas.

### **Beneficios del sistema:**

- **Acceso automatizado**, eliminando la necesidad de tarjetas o mandos.

- **Mayor seguridad**, permitiendo solo la entrada de vehículos autorizados.

- **Gestión eficiente**, con un sistema centralizado para administrar accesos.

- **Registro detallado** de todos los accesos.


## **3. Objetivos**

Desde un punto de vista técnico, el proyecto se centrará en:

- **Capturar imágenes de matrículas** con una **cámara en Raspberry Pi 3B**.

- **Detectar matrículas automáticamente** con **OpenALPR**.

- **Almacenar y gestionar matrículas** en una **base de datos MySQL**.

- **Desarrollar un script en Python** que compare matrículas con la base de datos.

- **Crear una API con Flask** para la gestión de matrículas.

- **Desarrollar una interfaz web** para que los usuarios puedan solicitar el registro de su matrícula.

- **Implementar un panel de administración** donde se aprueben o rechacen matrículas.


## **4. Medios Necesarios**

Para llevar a cabo este proyecto, se necesitará:

**Hardware:**

- Raspberry Pi 3B con Ubuntu Server.
    
- Cámara Raspberry Pi HQ.
    
- MicroSD de al menos 16GB con sistema operativo instalado.
    
- VPS en DigitalOcean para alojar la base de datos y la API.
    

**Software:**

- Python, Flask (API), MySQL (base de datos).
    
- OpenALPR para reconocimiento de matrículas.
    
- HTML + Bootstrap + Flask para la interfaz web.
    
- Servidor web.
    


## **5. Planificación**

| **Semanas**   | **Tareas**                                                                                                                                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **2 semanas** | - Instalación y pruebas de OpenALPR en Raspberry Pi.<br>- Creación de la base de datos MySQL con matrículas de prueba.<br>- Desarrollo de un script en Python para capturar imágenes y detectar matrículas.                 |
| **3 semanas** | - Creación de una API con Flask para gestionar la base de datos.<br>- Desarrollo de una web donde los usuarios puedan solicitar acceso.<br>- Implementación de un panel de administración para aprobar/rechazar matrículas. |
| **1 semana**  | - Configuración del sistema de notificaciones por Telegram o email. (Opcional)<br>- Implementación del registro de accesos con fotos.<br>- Pruebas de acceso restringido por horario.                                       |
| **2 semanas** | - Integración final del sistema en la Raspberry Pi.<br>- Pruebas de rendimiento con diferentes condiciones de luz y ángulos de cámara.<br>- Documentación final y optimización del sistema.                                 |


## **6. Estructura del repositorio**

```
/control-acceso-matriculas
├── README.md                  # Documentación del proyecto
├── .gitignore                 # Archivos ignorados por Git
├── 📁 canvas/                    # Diagrama de rutas en Obsidian Canvas
│   └── rutasaplicacion.canvas
├── 📁 docs/                     # Documentación técnica
│   ├── 📁 capturas_documentacion/
│   ├── 📁 Raspberry/
│   │   ├── EjecucionAutomaticaScript.md
│   │   ├── ExplicacionProcesarMatricula.md
│   │   └── 📁 OpenALPR/
│   │       └── InstalacionOpenALPR.md
│   └── 📁 VPS/
│       └── DespliegueAplicacionFlaskconGunicorn.md
├── 📁 backend/                  # Aplicación Flask (API y frontend integrado)
│   ├── app.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── 📁 routes/               # Blueprints Flask: auth, api, admin, main, matriculas
│   ├── 📁 templates/            # Plantillas HTML
│   ├── 📁 static/               # CSS, iconos, imágenes
│   └── 📁 utils/                # db_utils.py y funciones auxiliares
├── 📁 raspberry-pi/             # Script de captura en Raspberry Pi
│   └── procesar_matricula.py
```

--- 
## **Documentación del proyecto**

### **1. Propósito**

Este documentación proporciona una visión general completa del sistema _Control Acceso Matrículas_, una solución de control de acceso basada en el reconocimiento automático de matrículas. El sistema permite una gestión segura del acceso a instalaciones mediante la captura de imágenes de matrículas con una Raspberry Pi, su procesamiento con **OpenALPR** y la verificación de autorización en una base de datos centralizada.

### **2. Resumen de la Arquitectura del Sistema**

El sistema _Control Acceso Matrículas_ consta de tres componentes principales:

- **Aplicación Web**: Un servidor basado en Flask que gestiona la autenticación de usuarios, la gestión de matrículas y la lógica de control de acceso.
   
- **Componente Raspberry Pi**: Captura imágenes, procesa las matrículas y se comunica con el servidor.

- **Interfaz de Usuario**: Interfaces web tanto para usuarios normales como para administradores.

### **3. Aplicación Web**

#### Arquitectura MVC:

La arquitectura **MVC** (Modelo-Vista-Controlador) es un patrón de diseño muy común en el desarrollo de aplicaciones web, incluido en mi proyecto con Flask. Divide la lógica de una aplicación en tres componentes separados:

- **Modelos** 
	
	- ¿Qué es?
	
		Representa **los datos** y la lógica de la base de datos de la aplicación.

	- En mi proyecto:
	
		- Se gestiona con funciones de acceso a la [base de datos](db_tfg/control_acceso.sql) en [db_utils.py](backend/utils/db_utils.py).
		    
		- Se encarga de:
		    
		    - Conectarse a MySQL.
		        
		    - Recuperar y guardar información sobre usuarios, matrículas, accesos.
		
		**Ejemplo:**
		
		```python
		def conectar_db():
		
		    return mysql.connector.connect(
		        host="localhost",
		        user="flask_user",
		        password="flask_user",
		        database="control_acceso"
		    )
		```
		
 		> Código extraído del archivo: [db_utils.py](backend/utils/db_utils.py#L6-L12).

- **Vistas**

	- ¿Qué es?
	
		Es la **interfaz visual** con la que interactúa el usuario: HTML, CSS y Flask (Python).
	
	 - En mi proyecto:
	
		- Están en la carpeta [templates](backend/templates/).
		    
		- Se usan con **Jinja2** para insertar dinámicamente datos en las páginas.
		    
		- Muestran matrículas, formularios de login, tablas de usuarios, etc.
		    
	    **Ejemplo:**

		```html
		<h4 class="text-white mb-0">Mis Matrículas Registradas</h4>
		{% for matricula, estado in todas %}
		  <tr>
		    <td>{{ matricula }}</td>
		    <td>{{ estado }}</td>
		  </tr>
		{% endfor %}
		```

 		> Código extraído del archivo: [index.html](backend/templates/index.html#L80-L109).

- **Controladores**

	- ¿Qué es?
	
		Es el **puente entre el Modelo y la Vista**. Gestiona la lógica de la aplicación: recibe peticiones del usuario, actualiza modelos y decide qué vista mostrar.
	
	-  En mi proyecto:
	
		- Están en [routes/](backend/routes/): [auth.py](backend/routes/auth.py), [main.py](backend/routes/main.py), [admin.py](backend/routes/admin.py), etc.
		    
		- Cada archivo define rutas (`@app.route`) y qué hacer cuando se accede a ellas.
			
	    **Ejemplo:**

		```python
		@main.route("/")
		@login_required
		def index():
		    conexion = conectar_db()
		    cursor = conexion.cursor()
		...
		```

		> Código extraído del archivo: [main.py](backend/routes/main.py#L12-L16).

### **4. Componente Raspberry Pi**

Es el **sensor inteligente del sistema**. Se encarga de capturar la matrícula de un vehículo en tiempo real y comunicarse con el servidor para validar el acceso.
#### 1. Funcionamiento paso a paso

- La Raspberry Pi utiliza una [cámara](https://www.amazon.es/dp/B081Q8ZT9J) conectada físicamente.
    
- El script [procesar_matricula.py](raspberry-pi/procesar_matricula.py) ejecuta continuamente este comando:

```python
fswebcam -r 1280x720 --no-banner {CAPTURA}
```

> Código extraído del archivo: [procesar_matricula.py](raspberry-pi/procesar_matricula.py#L12).

Y con ese comando, se guarda una imagen de la matricula que está frente a la cámara.

#### 2. Reconocimiento de matrícula

- Se analiza la imagen usando **OpenALPR**, un sistema de reconocimiento automático de matrículas.

```python
resultado = subprocess.run(["alpr", "-c", "eu", imagen], capture_output=True, text=True)
```

> Código extraído del archivo: [procesar_matricula.py](raspberry-pi/procesar_matricula.py#L16).

OpenALPR detecta si hay una matrícula en la imagen y extrae el texto, por ejemplo `1234ABC`.

#### 3. Comunicación con el servidor

- Si se detecta una matrícula válida, la Raspberry Pi **envía la matrícula y la imagen** al servidor web (Flask) mediante una petición **HTTP POST**:

```python
SERVIDOR="https://matriculas.dsermar0808.tech/recibir_matricula"
...
respuesta = requests.post(SERVIDOR, files=archivos, data=datos, timeout=5)
```

> Código extraído del archivo: [procesar_matricula.py](raspberry-pi/procesar_matricula.py#L27).

El servidor se encarga de comprobar si esa matrícula está autorizada o no.

#### 4. Repetición automática

- Este proceso se ejecuta [cada segundo](raspberry-pi/procesar_matricula.py#L53) en un bucle infinito.

- También se evita repetir matrículas si son consecutivas.

```python
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
```

> Código extraído del archivo: [procesar_matricula.py](raspberry-pi/procesar_matricula.py#L42-L51).

#### 5. ¿Cómo se ejecuta automáticamente?

Se configura como **servicio `systemd`**, es decir, se inicia solo cuando se enciende la Raspberry.

Este es el archivo de configuración [matricula.service](systemd/matricula.service).

```service
[Unit]
Description=Script de detección de matrículas
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/dsermar/control-acceso-matriculas/raspberry-pi/procesar_matricula.py
WorkingDirectory=/home/dsermar/control-acceso-matriculas/raspberry-pi
StandardOutput=append:/var/log/matricula.log
StandardError=append:/var/log/matricula.log
Restart=always
User=dsermar

[Install]
WantedBy=multi-user.target
```

#### 6. Ventajas de este diseño

- **Descentralizado**: la Raspberry Pi toma decisiones rápidamente sin depender de cámaras IP complejas.
    
- **Flexible**: puedes cambiar la lógica del servidor sin tocar el script.
    
- **Escalable**: puedes añadir más Raspberrys en otras entradas fácilmente.

### **5. Interfaz web**

La interfaz de usuario está desarrollada con HTML, CSS (combinándolo con Bootstrap también), y el motor de plantillas Jinja2 integrado en Flask. Su diseño adapta dinámicamente los elementos mostrados según el rol del usuario: `admin` o `usuario`.

**Para usuarios normales:**

- Página principal ([/](backend/routes/main.py#L12-L71)) que muestra un resumen de sus matrículas registradas, divididas por estado ([autorizadas](backend/routes/main.py#L26-L32), [pendientes](backend/routes/main.py#L42-L48), [denegadas](backend/routes/main.py#L34-L40)).

	![tabla de matriculas registradas](capturas/matriculas_registradas.png)

- Un gráfico con sus accesos diarios, generado con **Chart.js**.

	![gráfico entradas por dia](capturas/graficaentradas.png)

	- Código del gráfico:
	
	```html
	<script>
	const ctxEntradas = document.getElementById('graficoEntradas').getContext('2d');
	
	new Chart(ctxEntradas, {
	
	  type: 'line',
	  data: {
	    labels: {{ fechas|tojson }},
	
	    datasets: [{
	      label: 'Entradas por Día',
	      data: {{ cantidades|tojson }},
	      fill: true,
	      backgroundColor: 'rgba(20, 179, 242, 0.15)',
	      borderColor: '#14b3f2',
	      tension: 0.4
	    }]
	
	  },
	
	  options: {
	    responsive: true,
	
	    plugins: {
	      legend: { labels: { color: 'white' } },
	      title: { display: false }
	    },
	
	  scales: {
	    x: { ticks: { color: '#fff' } },
	
	    y: {
	      beginAtZero: true,
	
	      ticks: {
	        color: '#fff',
	        stepSize: 1,
	        callback: function(value) {
	          return Number.isInteger(value) ? value : null;
	        }
	      }
	    }
	  }
	  }
	});
	</script>
	```
	
	> Código extraído del archivo: [index.html](backend/templates/index.html#L215-L251).


- Formulario para solicitar nuevas matrículas.

	![solicitar matricula](capturas/solicitar_matricula.png)

	- Código del backend para solicitar matricula:

	```python
	@matriculas.route('/solicitar_matricula', methods=['GET', 'POST'])
	@login_required
	def solicitar_matricula():
		...
	```
	> Código extraído del archivo: [matriculas.py](backend/routes/matriculas.py#L21-L78).

- Página de historial con filtros de fechas y visualización de imágenes asociadas a cada acceso.

--- 
### 3. **Autenticación y Roles**

- Basada en `Flask-Login`.
    
- Al iniciar sesión, el usuario recibe su rol (`admin` o `usuario`) que determina qué puede hacer y ver.
    
- Las sesiones se protegen con un `secret_key` y validaciones de acceso en cada vista.
    

### 4. **Funcionalidades de Usuario**

- Solicita nuevas matrículas (validación por regex).
    
- Visualiza:
    
    - Estado de sus matrículas (pendiente, autorizada, denegada).
        
    - Historial de accesos con imágenes y fechas.
        
    - Gráfico de accesos diarios (`Chart.js`).
        
- Puede eliminar sus matrículas si están denegadas o pendientes.
    
- Cambia su foto de perfil.
    

### 5. **Funcionalidades de Administrador**

- Visualiza todas las matrículas del sistema.
    
- Puede aprobar o rechazar nuevas solicitudes.
    
- Edita matrículas ya autorizadas.
    
- Crea y modifica usuarios.
    
- Limpia el historial completo.
    
- Usa filtros para buscar por estado o usuario en el panel.


### **4. Componentes Principales**

#### **1. Sistema de Autenticación**  

El sistema implementa un control de acceso basado en roles con dos roles principales de usuario:

- **Usuario (Usuario Regular):** Puede solicitar el registro de matrículas y ver sus matrículas personales.

- **Admin:** Puede gestionar usuarios, aprobar o rechazar solicitudes de matrícula y acceder a todas las funciones del sistema.
   
La autenticación se gestiona a través de **Flask-Login**, con rutas definidas en el _blueprint_ de autenticación ([auth.py](backend/routes/auth.py)).

### **5. Gestión de Matrículas** 

El sistema permite a los usuarios solicitar el registro de sus matrículas, los cuales deben ser **aprobadas por los administradores** antes de conceder acceso. Las matrículas siguen un formato estándar español de **cuatro números seguidos de tres letras** (por ejemplo: `1234ABC`).

#### **Flujos de trabajo clave:**

- **Usuarios:**  
    Solicitan el registro de su matrícula a través de la interfaz web.

- **Administradores:**  
    Revisan cada solicitud y pueden **aprobarla o rechazarla** según los criterios establecidos.
   
- **Gestión:**  
    Los administradores pueden consultar, modificar o eliminar matrículas ya registradas en el sistema.

