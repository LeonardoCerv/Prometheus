import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from datetime import datetime

from my_agent.agent import check_calendar_availability

load_dotenv()

app = Flask(__name__)

# Configuración de Flask
app.config['JSON_AS_ASCII'] = False  # Para que soporte caracteres especiales

@app.route("/", methods=["GET"])
def home():
    """Endpoint principal para verificar que el servidor está corriendo."""
    return jsonify({
        "status": "online",
        "service": "WhatsApp Calendar Bot",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "webhook": "/whatsapp (POST)",
            "test_calendar": "/test-calendar (GET)"
        }
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check para monitoreo."""
    try:
        # Intenta conectar con Google Calendar
        events = check_calendar_availability()
        calendar_status = "connected"
    except Exception as e:
        calendar_status = f"error: {str(e)}"
    
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Calendar Bot",
        "timestamp": datetime.now().isoformat(),
        "google_calendar": calendar_status,
        "twilio_configured": bool(os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN"))
    }), 200

@app.route("/test-calendar", methods=["GET"])
def test_calendar():
    """Endpoint GET para probar la conexión con Google Calendar."""
    try:
        events = check_calendar_availability()
        
        if events:
            events_list = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                events_list.append({
                    "summary": event.get("summary", "Sin título"),
                    "start": start,
                    "description": event.get("description", "Sin descripción")
                })
            
            return jsonify({
                "status": "success",
                "message": f"Se encontraron {len(events)} eventos",
                "events": events_list
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": "No hay eventos próximos",
                "events": []
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al consultar el calendario: {str(e)}"
        }), 500

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Responde a los mensajes entrantes de WhatsApp desde Twilio."""
    try:
        # Obtener datos del mensaje
        incoming_msg = request.values.get("Body", "").strip()
        from_number = request.values.get("From", "")
        
        # Log para debugging
        print(f"📱 Mensaje recibido de {from_number}: {incoming_msg}")
        
        resp = MessagingResponse()
        msg = resp.message()

        # Si no hay mensaje, responder con ayuda
        if not incoming_msg:
            msg.body("👋 ¡Hola! Envíame cualquier mensaje y te mostraré tu calendario.\n\nComandos:\n• 'calendario' o 'eventos' - Ver próximos eventos\n• 'ayuda' - Ver este mensaje")
            return str(resp)

        # Procesar el mensaje
        incoming_msg_lower = incoming_msg.lower()
        
        if "ayuda" in incoming_msg_lower or "help" in incoming_msg_lower:
            msg.body("🤖 *Bot de Calendario*\n\nComandos disponibles:\n• 'calendario' - Ver próximos eventos\n• 'eventos' - Ver próximos eventos\n• 'ayuda' - Ver este mensaje\n\n💡 Envía cualquier mensaje para ver tu calendario.")
        else:
            # Consultar el calendario
            try:
                availability = check_calendar_availability()
                
                if availability:
                    response_text = "📅 *Tus próximos eventos:*\n\n"
                    for i, event in enumerate(availability[:10], 1):  # Limitar a 10 eventos
                        start = event["start"].get("dateTime", event["start"].get("date"))
                        summary = event.get("summary", "Sin título")
                        
                        # Formatear la fecha de manera más legible
                        try:
                            if "T" in start:
                                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                                formatted_date = dt.strftime("%d/%m/%Y %H:%M")
                            else:
                                dt = datetime.fromisoformat(start)
                                formatted_date = dt.strftime("%d/%m/%Y")
                        except:
                            formatted_date = start
                        
                        response_text += f"{i}. *{summary}*\n   📆 {formatted_date}\n\n"
                    
                    response_text += f"Total: {len(availability)} evento(s)"
                else:
                    response_text = "📅 No tienes eventos próximos en tu calendario.\n\n¡Perfecto para relajarte! 😊"
                
                msg.body(response_text)
                print(f"✅ Respuesta enviada exitosamente")
                
            except Exception as e:
                error_msg = f"❌ Hubo un error al consultar tu calendario.\n\nError: {str(e)}\n\nPor favor, verifica la configuración."
                msg.body(error_msg)
                print(f"❌ Error al consultar calendario: {e}")

        return str(resp)
        
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(f"❌ Error en el servidor: {str(e)}")
        return str(resp), 500

@app.route("/webhook-test", methods=["GET"])
def webhook_test():
    """Endpoint GET para verificar que el webhook es accesible desde Twilio."""
    return jsonify({
        "status": "success",
        "message": "Webhook is reachable!",
        "note": "Use POST method for actual WhatsApp messages"
    }), 200

# Manejador de errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": ["/", "/health", "/whatsapp", "/test-calendar"]
    }), 404

# Manejador de errores 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print("=" * 60)
    print("🚀 WhatsApp Calendar Bot Server")
    print("=" * 60)
    print(f"📍 Server starting on port {port}")
    print(f"🌐 Local URL: http://localhost:{port}")
    print(f"📱 Webhook endpoint: http://localhost:{port}/whatsapp")
    print(f"🧪 Test endpoint: http://localhost:{port}/test-calendar")
    print(f"❤️  Health check: http://localhost:{port}/health")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("1. Start ngrok in another terminal: ngrok http 5000")
    print("2. Configure Twilio webhook with ngrok URL + /whatsapp")
    print("3. Send a WhatsApp message to test!")
    print("\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
