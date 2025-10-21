# 🚀 INICIO RÁPIDO - Schedule Agent

## ✅ Todo está listo en este directorio!

### Paso 1️⃣: Asegúrate de estar en el directorio correcto

```bash
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
pwd  # Debe mostrar: /Users/ian.hdzzz/Prometheus/scheduleAgent
```

### Paso 2️⃣: Prueba la conexión con Google Calendar

```bash
python test_system.py
```

Si ves tus eventos del calendario, ¡todo está bien! ✅

### Paso 3️⃣: Inicia el servidor Flask

**Opción A - Script automatizado:**
```bash
./start_server.sh
```

**Opción B - Manual:**
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
```

### Paso 4️⃣: Prueba los endpoints (en otra terminal)

```bash
cd /Users/ian.hdzzz/Prometheus/scheduleAgent

# Test calendar
curl http://localhost:5000/test-calendar

# O abre en navegador:
# http://localhost:5000/test-calendar
```

### Paso 5️⃣: Inicia ngrok (en otra terminal)

```bash
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
python start_ngrok.py
```

Copia la URL que aparece, ejemplo:
```
https://abc123.ngrok-free.app/whatsapp
```

### Paso 6️⃣: Configura Twilio

1. Ve a https://console.twilio.com/
2. WhatsApp Sandbox
3. "When a message comes in": `https://abc123.ngrok-free.app/whatsapp`
4. Método: **POST**
5. Guardar

### Paso 7️⃣: ¡Pruébalo!

Envía un mensaje de WhatsApp a: **+1 415 523 8886**

---

## 🎯 Resumen de Comandos

```bash
# 1. Navegar al directorio
cd /Users/ian.hdzzz/Prometheus/scheduleAgent

# 2. Probar
python test_system.py

# 3. Terminal 1: Servidor
python app.py

# 4. Terminal 2: ngrok
python start_ngrok.py
```

---

## 📱 Endpoints Disponibles

- `GET  /` - Status del servidor
- `GET  /health` - Health check
- `GET  /test-calendar` - Ver eventos en JSON
- `POST /whatsapp` - Webhook de WhatsApp
- `GET  /webhook-test` - Test del webhook

---

## 🐛 Problemas Comunes

### "No such file or directory: app.py"
```bash
# Asegúrate de estar en el directorio correcto
cd /Users/ian.hdzzz/Prometheus/scheduleAgent
```

### "No module named 'my_agent'"
```bash
# Verifica que my_agent existe
ls my_agent/

# Asegúrate de que __init__.py existe
ls my_agent/__init__.py
```

### No ve eventos del calendario
```bash
# Prueba primero
python test_system.py

# Verifica que las credenciales existen
ls hack-475720-a80832b916e2.json
```

---

## ✅ Estructura de Archivos

```
scheduleAgent/
├── app.py ✅
├── .env ✅
├── hack-475720-a80832b916e2.json ✅
├── requirements.txt ✅
├── my_agent/
│   ├── __init__.py ✅
│   └── agent.py ✅
├── start_ngrok.py ✅
├── test_system.py ✅
└── README.md ✅
```

---

**¡Todo listo! Comienza con el Paso 1.** 🚀
