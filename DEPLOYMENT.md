# Guia de Despliegue - PDF Template API

## Dependencias del Sistema

Este proyecto requiere:
- **Python 3.11+**
- **PostgreSQL 15+**
- **Dependencias de WeasyPrint** (para generacion de PDFs):
  - libpango, libcairo, libgdk-pixbuf, libffi

## Dependencias de Python

Ver archivo `requirements.txt`:
- FastAPI (framework web)
- SQLAlchemy (ORM)
- WeasyPrint (generacion PDF)
- Jinja2 (templates)
- python-jose (JWT tokens)
- bcrypt (hashing passwords)
- boto3 (S3 opcional)
- uvicorn (servidor ASGI)
- psycopg2-binary (PostgreSQL)

---

## Opcion 1: Despliegue con Docker (Recomendado)

### Requisitos
- Docker y Docker Compose instalados

### Pasos

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd pdf-template-api
```

2. **Configurar variables de entorno (opcional):**
Crear archivo `.env`:
```env
SESSION_SECRET=tu-clave-secreta-muy-segura-minimo-32-caracteres
AWS_ACCESS_KEY_ID=tu-access-key      # Opcional, para S3
AWS_SECRET_ACCESS_KEY=tu-secret-key  # Opcional, para S3
S3_BUCKET=tu-bucket                  # Opcional
```

3. **Iniciar los servicios:**
```bash
docker-compose up -d
```

4. **Verificar:**
```bash
docker-compose logs -f app
```

5. **Acceder a la aplicacion:**
- Aplicacion: http://localhost:8080
- Documentacion API: http://localhost:8080/docs

### Comandos utiles
```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Reiniciar
docker-compose restart
```

---

## Opcion 2: Despliegue Manual (sin Docker)

### 1. Instalar dependencias del sistema (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    fonts-liberation
```

### 2. Crear base de datos PostgreSQL
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE pdfapi;
CREATE USER pdfuser WITH PASSWORD 'tu-password-seguro';
GRANT ALL PRIVILEGES ON DATABASE pdfapi TO pdfuser;
\q
```

### 3. Configurar la aplicacion
```bash
# Clonar repositorio
git clone <tu-repositorio>
cd pdf-template-api

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio para almacenamiento local
mkdir -p local_storage
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raiz del proyecto:
```env
DATABASE_URL=postgresql://pdfuser:tu-password-seguro@localhost:5432/pdfapi
SESSION_SECRET=tu-clave-secreta-muy-segura-minimo-32-caracteres

# Opcional - Si usas S3 para almacenar templates
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_REGION=us-east-1
S3_BUCKET=pdf-templates
```

### 5. Iniciar la aplicacion
```bash
# Desarrollo
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Produccion (con Gunicorn)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080
```

---

## Opcion 3: Despliegue con Systemd (Produccion Linux)

### 1. Crear servicio systemd
```bash
sudo nano /etc/systemd/system/pdfapi.service
```

Contenido:
```ini
[Unit]
Description=PDF Template API
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/pdf-template-api
Environment="PATH=/opt/pdf-template-api/venv/bin"
EnvironmentFile=/opt/pdf-template-api/.env
ExecStart=/opt/pdf-template-api/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 2. Habilitar e iniciar
```bash
sudo systemctl daemon-reload
sudo systemctl enable pdfapi
sudo systemctl start pdfapi
sudo systemctl status pdfapi
```

---

## Configuracion de Nginx (Proxy Inverso)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Para PDFs grandes
        client_max_body_size 50M;
        proxy_read_timeout 300;
    }
}
```

Con SSL (Let's Encrypt):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## Variables de Entorno

| Variable | Requerido | Descripcion |
|----------|-----------|-------------|
| `DATABASE_URL` | Si | URL de conexion PostgreSQL |
| `SESSION_SECRET` | Si | Clave secreta para JWT (min 32 caracteres) |
| `AWS_ACCESS_KEY_ID` | No | Access key de AWS para S3 |
| `AWS_SECRET_ACCESS_KEY` | No | Secret key de AWS para S3 |
| `AWS_REGION` | No | Region de AWS (default: us-east-1) |
| `S3_BUCKET` | No | Nombre del bucket S3 (default: pdf-templates) |

**Nota:** Si no configuras S3, los templates se guardan localmente en `local_storage/`.

---

## Estructura del Proyecto

```
pdf-template-api/
├── app/
│   ├── core/           # Configuracion, DB, seguridad
│   ├── models/         # Modelos SQLAlchemy
│   ├── routes/         # Endpoints API
│   ├── schemas/        # Schemas Pydantic
│   ├── services/       # Logica de negocio
│   ├── static/         # CSS, JS
│   ├── templates/      # Templates HTML (UI)
│   ├── utils/          # Utilidades (PDF, Jinja)
│   └── main.py         # Punto de entrada
├── local_storage/      # Almacenamiento local de templates
├── requirements.txt    # Dependencias Python
├── Dockerfile          # Imagen Docker
├── docker-compose.yml  # Orquestacion Docker
└── .env               # Variables de entorno (crear)
```

---

## Soporte

Para problemas comunes:

1. **Error de WeasyPrint:** Instalar dependencias del sistema (pango, cairo)
2. **Error de conexion DB:** Verificar DATABASE_URL y que PostgreSQL este corriendo
3. **Error 500 en render:** Verificar que el template HTML sea valido
