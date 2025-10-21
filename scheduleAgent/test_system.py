"""
Script de prueba para verificar que la integración con Google Calendar funciona correctamente.
"""

from my_agent.agent import check_calendar_availability
from dotenv import load_dotenv

load_dotenv()


def test_calendar_connection():
    """Prueba la conexión con Google Calendar"""
    print("\n" + "=" * 60)
    print("PRUEBA DE CONEXIÓN CON GOOGLE CALENDAR")
    print("=" * 60 + "\n")
    
    try:
        print("🔄 Consultando eventos del calendario...\n")
        events = check_calendar_availability()
        
        if events:
            print(f"✅ Conexión exitosa! Se encontraron {len(events)} eventos:\n")
            print("-" * 60)
            
            for i, event in enumerate(events, 1):
                start = event["start"].get("dateTime", event["start"].get("date"))
                summary = event.get("summary", "Sin título")
                print(f"{i}. {summary}")
                print(f"   📅 {start}")
                print()
            
            print("-" * 60)
            print("\n✅ Todo funciona correctamente!")
            print("\nAhora puedes:")
            print("1. Configurar Twilio (ver GOOGLE_SETUP.md)")
            print("2. Ejecutar: python app.py")
            print("3. Usar ngrok para exponer tu servidor: python start_ngrok.py")
            
        else:
            print("⚠️  No se encontraron eventos próximos en tu calendario.")
            print("Pero la conexión con Google Calendar funciona correctamente!")
            
    except Exception as e:
        print(f"\n❌ Error al conectar con Google Calendar:\n{e}\n")
        print("Posibles soluciones:")
        print("1. Asegúrate de haber habilitado la API de Google Calendar")
        print("2. Si usas cuenta de servicio, comparte tu calendario con el email de la cuenta")
        print("3. Si usas OAuth, ejecuta: python setup_google_auth.py")
        print("4. Revisa el archivo .env y las credenciales")
        print("\nVer más detalles en GOOGLE_SETUP.md")
        return False
    
    print("\n" + "=" * 60 + "\n")
    return True


if __name__ == "__main__":
    test_calendar_connection()
