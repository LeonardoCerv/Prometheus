# 🤖 Schedule Agent - WhatsApp Calendar Bot

Bot de WhatsApp para consultar disponibilidad de Google Calendar.

## 📁 Estructura

```
scheduleAgent/
├── app.py                          # Servidor Flask principal
├── .env                            # Variables de entorno
├── requirements.txt                # Dependencias
├── hack-475720-a80832b916e2.json   # Credenciales de Google
├── my_agent/
│   ├── __init__.py
│   └── agent.py                    # Lógica del agente y Google Calendar
├── start_ngrok.py                  # Script para iniciar ngrok
├── test_system.py                  # Script de prueba
└── venv/                           # Entorno virtual (si existe)
```

## 🚀 Inicio Rápido

### 1. Navega al directorio:
```bash
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
```

### 2. Activa el entorno virtual (si existe):
```bash
source venv/bin/activate
```

### 3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 4. Verifica la configuración:
```bash
# Asegúrate de que .env tiene las credenciales de Twilio
cat .env
```

### 5. Prueba la conexión con Google Calendar:
```bash
python test_system.py
```

### 6. Inicia el servidor Flask:
```bash
python app.py
```

Deberías ver:
```
========================================
🚀 WhatsApp Calendar Bot Server
========================================
📍 Server starting on port 5000
🌐 Local URL: http://localhost:5000
📱 Webhook endpoint: http://localhost:5000/whatsapp
🧪 Test endpoint: http://localhost:5000/test-calendar
```

### 7. En otra terminal, inicia ngrok:
```bash
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
python start_ngrok.py
```

## 🧪 Probar Endpoints

### Desde el navegador:
- http://localhost:5000/
- http://localhost:5000/health
- http://localhost:5000/test-calendar

### Desde la terminal:
```bash
curl http://localhost:5000/test-calendar
```

## 📱 Configurar Twilio

1. Copia la URL de ngrok (ej: `https://abc123.ngrok-free.app`)
2. Ve a https://console.twilio.com/
3. WhatsApp Sandbox → "When a message comes in"
4. URL: `https://abc123.ngrok-free.app/whatsapp`
5. Método: **POST**
6. Guardar

## 🔧 Variables de Entorno

Archivo `.env`:
```bash
# Twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Google Calendar
GOOGLE_CREDENTIALS_FILE=your-credentials-file.json
CALENDAR_ID=primary

# Google Cloud & GenAI
GOOGLE_CLOUD_PROJECT=hack-475720
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyAo3Q6TYfzbsYZ4qAX366VXLC6BOuRcUzw
```

## 🐛 Solución de Problemas

### Error: "No module named 'my_agent'"
```bash
# Asegúrate de estar en el directorio correcto
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
python app.py
```

### Error: "No such file or directory: .env"
```bash
# Verifica que .env existe
ls -la .env

# Si no existe, cópialo desde el directorio padre
cp ../.env .
```

### Error al importar
```bash
# Asegúrate de que my_agent/__init__.py existe
touch my_agent/__init__.py
```

## 📋 Comandos Útiles

```bash
# Navegar al directorio
cd /Users/ian.hdzzz/Prometheus/scheduleAgent

# Probar sistema
python test_system.py

# Iniciar servidor
python app.py

# Iniciar ngrok (en otra terminal)
python start_ngrok.py

# Ver logs en tiempo real
# Los verás directamente en la terminal donde corre app.py

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

## ✅ Checklist

- [ ] Navegado a `/Users/ian.hdzzz/Prometheus/scheduleAgent`
- [ ] Archivo `.env` existe con credenciales
- [ ] Archivo `hack-475720-a80832b916e2.json` existe
- [ ] `python test_system.py` funciona
- [ ] `python app.py` inicia sin errores
- [ ] http://localhost:5000/test-calendar muestra eventos
- [ ] ngrok corriendo
- [ ] Webhook configurado en Twilio

## 🎯 Todo debe ejecutarse desde este directorio

**Importante:** Todos los comandos deben ejecutarse desde:
```bash
/Users/ian.hdzzz/Prometheus/scheduleAgent
```

No desde `/Users/ian.hdzzz/Prometheus/`

---

¡Listo para usar! 🚀
