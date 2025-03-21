
# Despliegue de una aplicacion con Flask y Gunicorn + certificado SSL con Let's Encrypt

## 1. Configurar Gunicorn para ejecutar la aplicación 

### Creación de un punto de entrada de WSGI

Creamos al archivo `wsgi.py:`

```bash
nano ~/control-acceso-matricula/backend/wsgi.py
```

En él, importaremos la instancia de Flask desde nuestra aplicación y luego la ejecutaremos:

```python
from app import app  
  
if __name__ == "__main__":  
   app.run(debug=True)
```

El `from app import app` hay que poner **NOMBRE DEL ARCHIVO .PY DE NUESTRA**


**1.1 Probar la aplicación con Gunicorn** 
Ejecuta:

```bash
cd ~/control-acceso-matricula/backend
gunicorn --bind 0.0.0.0:5000 app
```

Debería ver un resultado como el siguiente:

```
Output[2020-05-20 14:13:00 +0000] [46419] [INFO] Starting gunicorn 20.0.4
[2020-05-20 14:13:00 +0000] [46419] [INFO] Listening at: http://0.0.0.0:5000 (46419)
[2020-05-20 14:13:00 +0000] [46419] [INFO] Using worker: sync
[2020-05-20 14:13:00 +0000] [46421] [INFO] Booting worker with pid: 46421
```

Visite de nuevo la dirección IP de su servidor con `:5000` agregado al final en su navegador web:

```output
http://your_server_ip:5000
```

Ya completamos las tareas de nuestro entorno virtual, por lo que podemos desactivarlo:

```bash
deactivate
```

**1.2 Configurar Gunicorn como un servicio** 
Crea un archivo de servicio:

```bash
sudo nano /etc/systemd/system/app.service
```

Añade lo siguiente (ajusta rutas según tu aplicación):


```
[Unit]
Description=Gunicorn instance to serve flask app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/control-acceso-matriculas/backend
Environment="PATH=/root/control-acceso-matriculas/backend/venv/bin"
ExecStart=/root/control-acceso-matriculas/backend/venv/bin/gunicorn --workers 3 --bind unix:/root/control-acceso-matriculas/backend/app.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

Guarda y cierra (`CTRL+X`, `Y`, `Enter`).
Habilita y arranca el servicio:


```bash
sudo systemctl start app
sudo systemctl enable app
```

Verifica que Gunicorn está corriendo:


```bash
sudo systemctl status app
```


---

## 2. Instalar y configurar Nginx como proxy inverso 

**2.1 Instalar Nginx** 

```bash
sudo apt install nginx -y
```
**2.2 Crear archivo de configuración en Nginx** 

```bash
sudo nano /etc/nginx/sites-available/app
```

Añade:

```
server {
    listen 80;
    server_name matriculas.dsermar0808.tech;

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/control-acceso-matriculas/backend/app.sock;
    }
}
```

Guarda y activa la configuración:


```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

Por último, ajustaremos el firewall de nuevo. Ya no necesitamos acceso a través del puerto `5000`, por lo que podemos eliminar esta regla. Luego, podemos permitir el acceso completo al servidor de Nginx:

```bash
sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'
```

Ahora debería poder visitar el nombre de dominio de su servidor en su navegador web:

```
http://matriculas.dsermar0808.tech
```

---

**==PENDIENTE==**
## 3. Configurar HTTPS con Let's Encrypt y Certbot 

**3.1 Instalar Certbot** 

```bash
sudo apt install python3-certbot-nginx
```

**3.2 Obtener certificado SSL** 
Ejecuta:

```bash
sudo certbot --nginx -d matriculas.dsermar0808.tech
```

Si siguió las instrucciones de instalación de Nginx en los requisitos previos, ya no necesitará la asignación de perfil HTTP redundante:

```bash
sudo ufw delete allow 'Nginx HTTP'
```

Para verificar la configuración, acceda una vez más a su dominio utilizando `https://`:

```
https://matriculas.dsermar0808.tech
```


---

## Posible errores

Si da el error de `13 permission denied`, ponemos los siguiente comandos:

```bash
sudo -u www-data ls -lah /root/control-acceso-matriculas/backend/app.sock
```

```bash
sudo chown ubuntu:www-data /root/control-acceso-matriculas/backend
```

 **IMPORTANTE ESTE COMANDO:**
 
```bash
sudo chmod o+x /root 
```

```bash
sudo chmod -R 660 /root/control-acceso-matriculas/backend/app.sock 
```

```bash
sudo chmod -R 750 /root/control-acceso-matriculas/backend
```

Reiniciar servicios:

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl restart app
```

```bash
sudo systemctl restart nginx
```

LOGS:

```bash
sudo tail -f /var/log/nginx/error.log
```

