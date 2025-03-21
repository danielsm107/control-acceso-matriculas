# **Como ejecutar el script automáticamente**

## **1️. Crear un Servicio `systemd`**

1. **Abre un nuevo archivo de servicio en `/etc/systemd/system/`**

```bash
sudo nano /etc/systemd/system/matricula.service
```

2. **Copia y pega este contenido (ajusta la ruta de tu script)**:

```bash
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


3. **Guarda y cierra (`CTRL + X`, `Y`, `ENTER`).**

## **2. Habilitar y Iniciar el Servicio**

1. **Recargar `systemd` para detectar el nuevo servicio:**

```bash
sudo systemctl daemon-reload
```

2. **Activar el servicio para que inicie automáticamente al arrancar la Raspberry Pi:**

```bash
sudo systemctl enable matricula.service
```

3. **Iniciar el servicio manualmente (para probar que funciona):**

```bash
sudo systemctl start matricula.service
```

4. **Verificar que está corriendo correctamente:**

```bash
sudo systemctl status matricula.service
```

 Si todo está bien, deberías ver algo como:
	```
	● matricula.service - Script de detección de matrículas
	  Loaded: loaded (/etc/systemd/system/matricula.service; enabled)
	  Active: active (running) since ...
	```

## **3. Probar Reiniciando la Raspberry Pi**

```
sudo reboot
```

Después del reinicio, verifica que el script se está ejecutando automáticamente con:

```
sudo systemctl status matricula.service
```

## **4. Como ver los logs**

Ejecuta el siguiente comando para ver los logs:

```bash
tail -f /var/log/matricula.log
```

