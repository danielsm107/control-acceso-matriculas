# **Sistema de Control de Acceso por Reconocimiento de Matrículas**

**Autor:** Daniel Serrano Marín

**I.E.S. Francisco Romero Vargas**
**Administración de Sistemas Informáticos en Red**
**Curso: 2024/2025**

---

## **Índice**

1. [[#**1. Introducción**|Introducción]]

2. [[#**2. Finalidad**|Finalidad]]

3. [[#**3. Objetivos**|Objetivos]]
 
4. [[#**4. Medios Necesarios**|Medios Necesarios]]

5. [[#**5. Planificación**|Planificación]]


---

## **1. Introducción**

Este proyecto consiste en un **sistema de control de acceso** basado en el reconocimiento automático de matrículas (LPR - License Plate Recognition).

El sistema capturará imágenes de matrículas mediante una **cámara conectada a una Raspberry Pi**. A través de **OpenALPR**, se detectará la matrícula y se comparará con una **base de datos MySQL** para determinar si el acceso es autorizado o denegado.

Además, los usuarios podrán **solicitar el registro de su matrícula** mediante una aplicación web, y un administrador podrá aprobar o rechazar el acceso.


---

## **2. Finalidad**

El objetivo principal es mejorar la **seguridad y automatización del acceso** mediante el reconocimiento de matrículas.

### **Beneficios del sistema:**

- **Acceso automatizado**, eliminando la necesidad de tarjetas o mandos.

- **Mayor seguridad**, permitiendo solo la entrada de vehículos autorizados.

- **Gestión eficiente**, con un sistema centralizado para administrar accesos.

- **Registro detallado** de todos los accesos, con fechas y horas.


---

## **3. Objetivos**

Desde un punto de vista técnico, el proyecto se centrará en:

- **Capturar imágenes de matrículas** con una **cámara en Raspberry Pi 3B**.

- **Detectar matrículas automáticamente** con **OpenALPR**.

- **Almacenar y gestionar matrículas** en una **base de datos MySQL**.

- **Desarrollar un script en Python** que compare matrículas con la base de datos.

- **Crear una API con Flask** para la gestión de matrículas.

- **Desarrollar una interfaz web** para que los usuarios puedan solicitar el registro de su matrícula.

- **Implementar un panel de administración** donde se aprueben o rechacen matrículas.


---

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

---

## **5. Planificación**

| **Semanas**   | **Tareas**                                                                                                                                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **2 semanas** | - Instalación y pruebas de OpenALPR en Raspberry Pi.<br>- Creación de la base de datos MySQL con matrículas de prueba.<br>- Desarrollo de un script en Python para capturar imágenes y detectar matrículas.                 |
| **3 semanas** | - Creación de una API con Flask para gestionar la base de datos.<br>- Desarrollo de una web donde los usuarios puedan solicitar acceso.<br>- Implementación de un panel de administración para aprobar/rechazar matrículas. |
| **1 semana**  | - Configuración del sistema de notificaciones por Telegram o email. (Opcional)<br>- Implementación del registro de accesos con fotos.<br>- Pruebas de acceso restringido por horario.                                       |
| **2 semanas** | - Integración final del sistema en la Raspberry Pi.<br>- Pruebas de rendimiento con diferentes condiciones de luz y ángulos de cámara.<br>- Documentación final y optimización del sistema.                                 |

