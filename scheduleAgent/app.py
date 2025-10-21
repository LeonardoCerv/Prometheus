import asyncio
import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
from datetime import datetime

from my_agent.agent import check_calendar_availability, root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

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

runner = InMemoryRunner(agent=root_agent, app_name="whatsapp_calendar_bot")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Responde a los mensajes entrantes de WhatsApp desde Twilio."""
    # Validar que la solicitud proviene de Twilio
    # TEMPORARILY DISABLED FOR DEBUGGING - ENABLE IN PRODUCTION!
    validator = RequestValidator(os.getenv("TWILIO_AUTH_TOKEN"))
    url = request.url
    post_vars = request.form.to_dict()
    twilio_signature = request.headers.get("X-Twilio-Signature", "")

    # Comment this out for local testing, uncomment for production
    # if not validator.validate(url, post_vars, twilio_signature):
    #     return "Error: Invalid signature", 403

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

        # Procesar el mensaje con el agente inteligente usando ADK Runner
        incoming_msg_lower = incoming_msg.lower()
        
        if "ayuda" in incoming_msg_lower or "help" in incoming_msg_lower:
            msg.body("🤖 *Bot de Calendario*\n\nComandos disponibles:\n• 'calendario' - Ver próximos eventos\n• 'eventos' - Ver próximos eventos\n• 'schedule' o 'programar' - Crear una reunión\n• 'ayuda' - Ver este mensaje\n\n💡 Ejemplo para programar:\n'Schedule a call on October 22, 2025, from 9 to 9:30 AM with enayala12@gmail.com, title: Test Meeting'")
        else:
            # Usar el Runner de ADK para procesar el mensaje con el agente
            try:
                print(f"🤖 Procesando mensaje con el agente: {incoming_msg}")
                
                # Usar el número de WhatsApp como user_id
                user_id = from_number.replace('whatsapp:', '')
                
                # Crear un mensaje con el formato correcto
                user_message = Content(
                    role="user",
                    parts=[Part(text=incoming_msg)]
                )
                
                # Explicitly get or create the session
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                session = loop.run_until_complete(runner.session_service.get_session(session_id=user_id, user_id=user_id, app_name="whatsapp_calendar_bot"))
                
                # Ejecutar el agente con el mensaje del usuario
                # runner.run() retorna un generador, necesitamos consumirlo
                response_text = ""
                for event in runner.run(
                    new_message=user_message,
                    user_id=user_id,
                    session_id=user_id
                ):
                    # Procesar eventos del agente
                    if hasattr(event, 'text'):
                        response_text += event.text
                
                # Enviar la respuesta al usuario
                if response_text:
                    msg.body(response_text)
                else:
                    msg.body("Lo siento, no pude procesar tu mensaje. Por favor intenta de nuevo.")
                    
            except Exception as e:
                print(f"❌ Error procesando mensaje con el agente: {str(e)}")
                msg.body("Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta de nuevo más tarde.")
        
        return str(resp)
        
    except Exception as e:
        print(f"❌ Error general en whatsapp_reply: {str(e)}")
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Lo siento, ocurrió un error inesperado. Por favor intenta de nuevo.")
        return str(resp)

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
