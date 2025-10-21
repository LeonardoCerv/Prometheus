"""
Script para configurar la autenticación inicial con Google Calendar API.
Este script solo necesita ejecutarse una vez para generar el archivo token.json.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Si modificas estos scopes, elimina el archivo token.json
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def setup_authentication():
    """
    Configura la autenticación inicial con Google Calendar.
    Genera el archivo token.json que será usado por la aplicación.
    """
    creds = None
    
    # El archivo token.json almacena los tokens de acceso y actualización del usuario
    # y se crea automáticamente cuando el flujo de autorización se completa por primera vez
    if os.path.exists("token.json"):
        print("Se encontró un archivo token.json existente.")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Si no hay credenciales (válidas) disponibles, solicita al usuario que inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Actualizando credenciales expiradas...")
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("\n❌ ERROR: No se encontró el archivo 'credentials.json'")
                print("\nPor favor, sigue estos pasos:")
                print("1. Ve a https://console.developers.google.com/")
                print("2. Crea un nuevo proyecto o selecciona uno existente")
                print("3. Habilita la API de Google Calendar")
                print("4. Crea credenciales OAuth 2.0 para aplicación de escritorio")
                print("5. Descarga el archivo JSON y renómbralo como 'credentials.json'")
                print("6. Coloca 'credentials.json' en la raíz de este proyecto\n")
                return False
            
            print("Iniciando flujo de autenticación OAuth...")
            print("Se abrirá una ventana del navegador para que autorices la aplicación.")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Guarda las credenciales para la próxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        print("\n✅ Token guardado exitosamente en 'token.json'")

    # Prueba la conexión obteniendo el calendario
    try:
        service = build("calendar", "v3", credentials=creds)
        print("\n🔄 Probando conexión con Google Calendar...")
        
        # Obtiene información del calendario principal
        calendar = service.calendars().get(calendarId='primary').execute()
        print(f"✅ Conexión exitosa! Calendario: {calendar.get('summary', 'Sin nombre')}")
        
        return True
    except Exception as error:
        print(f"\n❌ Error al conectar con Google Calendar: {error}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURACIÓN DE AUTENTICACIÓN DE GOOGLE CALENDAR")
    print("=" * 60)
    print()
    
    success = setup_authentication()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print("\nAhora puedes ejecutar tu aplicación Flask:")
        print("  python app.py")
        print()
    else:
        print("\n" + "=" * 60)
        print("❌ CONFIGURACIÓN INCOMPLETA")
        print("=" * 60)
        print("\nPor favor, completa los pasos indicados arriba.")
        print()
