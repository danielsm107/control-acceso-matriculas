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

El objetivo principal es mejorar la **seguridad y automatización del acceso** mediante el reconocimiento de matrículas.

### **Beneficios del sistema:**

- **Acceso automatizado**, eliminando la necesidad de tarjetas o mandos.

- **Mayor seguridad**, permitiendo solo la entrada de vehículos autorizados.

- **Gestión eficiente**, con un sistema centralizado para administrar accesos.

- **Registro detallado** de todos los accesos, con fechas y horas.


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

- Raspberry Pi 3B con Raspberry Pi OS Lite.
    
- Cámara Raspberry Pi HQ o cámara USB compatible.
    
- MicroSD de al menos 16GB con sistema operativo instalado.
    
- Servidor o PC para alojar la base de datos y la API.
    

**Software:**

- Python, Flask (API), MySQL (base de datos).
    
- OpenALPR para reconocimiento de matrículas.
    
- HTML + Bootstrap + Flask para la interfaz web.
    
- Servidor web.
    
- Bot de Telegram para alertas de accesos no autorizados (opcional).


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
│── 📁 docs/     # Documentación del Proyecto
│── 📁 backend/               # API Flask (VPS DigitalOcean)
│   │── app.py                # Servidor Flask principal
│   │── database.py            # Conexión a la base de datos
│   │── config.py              # Configuración de la app
│   │── requirements.txt       # Dependencias de Python
│   │── wsgi.py                # Entrada para Gunicorn
│   ├── 📁 static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── 📁 templates/          # Plantillas HTML (Jinja2)
│   ├── 📁 routes/             # Rutas de la API Flask
│       ├── auth.py            # Rutas de autenticación
│       ├── matriculas.py      # Rutas para gestionar matrículas
│       ├── admin.py           # Rutas de administrador
│
│── 📁 frontend/               # Interfaz Web (VPS DigitalOcean)
│   │── index.html             # Página principal
│   │── panel.html             # Panel de administración
│   ├── 📁 assets/             # CSS, imágenes, JS
│       ├── style.css          # Estilos CSS
│       ├── app.js             # Código JavaScript
│
│── 📁 raspberry-pi/           # Código en la Raspberry Pi
│   │── procesar_matricula.py  # Captura de imagen y envío al servidor
│   │── detectar_matricula.py  # Reconocimiento con OpenALPR
│   │── config.py              # Configuración de la Raspberry
│
│── 📁 scripts/                # Scripts útiles para despliegue
│   │── deploy.sh              # Script para actualizar código en el VPS
│   │── setup.sh               # Instalación automática en la Raspberry
│
│── 📁 docker/                 # Configuración Docker (Opcional)
│   │── Dockerfile             # Contenedor Flask API
│   │── docker-compose.yml     # Orquestación (si se usa Docker)
│
│── .gitignore                 # Archivos a ignorar en Git
│── README.md                  # Documentación del proyecto
│── .github/workflows/deploy.yml # GitHub Actions para despliegue automático (Revisar)
```


## **Por hacer:**

- [x] Arreglar redireccionamiento a la pagina principal cuando eres admin.
- [x] Añadir botón para modificación de usuarios desde admin.
- [x] Evitar duplicados de correos electrónicos.
- [x] Añadir botón para poder crear usuarios desde admin_panel.
- [x] Cambiar estilos botones admin panel.
- [x] Añadir imágenes en historial.html.
- [x] Crear una página con todas las matriculas existentes.
- [x] Arreglar las imagenes en historial.
- [x] Añadir columna de acciones en matriculas_admin.
- [x] Añadir filtros en matriculas_admin.
- [x] Añadir botón de limpiar historial en historial.html.
- [x] Arreglar mensaje de fallo de contraseña en el login.
- [x] Arreglar las matriculas pendientes aparezcan como pendientes en mis_matriculas.html.
- [ ] Añadir filtro historial.html
- [x] Arreglar que cuando un admin registre una nueva matricula en admin_matriculas esté como autorizada automáticamente.
- [x] Modificar pagina index.html para que muestre la información del usuario actual. (**PRIORITARIO**)
- [x] Creación de gráficas para matriculas. (**PRIORITARIO**)
- [x] Arreglar que no se puedan cambiar permisos admin principal
- [x] Cambiar estilos mensajes flash

--- 
## **Documentación del proyecto**

### **1. Propósito**

Este documentación proporciona una visión general completa del sistema _Control Acceso Matrículas_, una solución de control de acceso basada en el reconocimiento automático de matrículas. El sistema permite una gestión segura del acceso a instalaciones mediante la captura de imágenes de matrículas con una Raspberry Pi, su procesamiento con **OpenALPR** y la verificación de autorización en una base de datos centralizada. Esta página cubre la arquitectura general, los componentes clave, los flujos de trabajo y cómo interactúan estos componentes.

### **2. Resumen de la Arquitectura del Sistema**

El sistema _Control Acceso Matrículas_ consta de tres componentes principales:

- **Aplicación Web**: Un servidor basado en Flask que gestiona la autenticación de usuarios, la gestión de matrículas y la lógica de control de acceso.
   
- **Componente Raspberry Pi**: Captura imágenes, procesa las matrículas y se comunica con el servidor.

- **Interfaz de Usuario**: Interfaces web tanto para usuarios normales como para administradores.

### **3. Aplicación Web**

#### Arquitectura MVC:

La arquitectura **MVC** (Modelo-Vista-Controlador) es un patrón de diseño muy común en el desarrollo de aplicaciones web, incluido en mi proyecto con Flask. Divide la lógica de una aplicación en tres componentes separados:

- **Modelos**: Gestión en `db_utils.py` y base de datos MySQL.
    
- **Vistas**: Plantillas HTML renderizadas con Jinja2 (`templates/`).
    
- **Controladores**: Blueprints organizados en [routes/](backend/routes/) ([auth.py](backend/routes/auth.py), `admin.py`, `main.py`, `matriculas.py`, `api.py`).
    

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

