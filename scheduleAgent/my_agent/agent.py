import datetime
import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Scopes necesarios para Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def check_calendar_availability():
    """
    Obtiene los próximos eventos del calendario de Google.
    
    Returns:
        list: Lista de eventos próximos del calendario
    """
    creds = None
    
    # Obtener la ruta base del proyecto
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    credentials_filename = os.getenv("GOOGLE_CREDENTIALS_FILE", "hack-475720-a80832b916e2.json")
    credentials_file = os.path.join(current_dir, credentials_filename)
    
    print(f"Buscando credenciales en: {credentials_file}")
    
    try:
        # Intenta usar credenciales de cuenta de servicio si existe el archivo
        if os.path.exists(credentials_file):
            print(f"✅ Archivo de credenciales encontrado: {credentials_file}")
            creds = service_account.Credentials.from_service_account_file(
                credentials_file, scopes=SCOPES
            )
            print("✅ Credenciales de cuenta de servicio cargadas correctamente")
        # Si no, intenta usar el flujo OAuth con token.json
        elif os.path.exists(os.path.join(current_dir, "token.json")):
            print("Usando token.json")
            creds = Credentials.from_authorized_user_file(
                os.path.join(current_dir, "token.json"), SCOPES
            )
        
        # Verificar si se cargaron las credenciales
        if not creds:
            raise Exception(f"No se pudieron cargar las credenciales desde: {credentials_file}")
        
        # Para cuentas de servicio, no necesitamos refrescar
        # Solo verificamos si hay refresh_token para OAuth
        if hasattr(creds, 'expired') and creds.expired and hasattr(creds, 'refresh_token') and creds.refresh_token:
            print("Refrescando credenciales expiradas...")
            creds.refresh(Request())

        # Construir el servicio de Calendar API
        print("🔄 Construyendo servicio de Google Calendar...")
        service = build("calendar", "v3", credentials=creds)

        # Llamar a la API de Calendar
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indica tiempo UTC
        calendar_id = os.getenv("CALENDAR_ID", "primary")
        
        print(f"📅 Consultando calendario: {calendar_id}")
        print(f"Obteniendo los próximos 10 eventos...")
        
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("ℹ️  No se encontraron eventos próximos.")
            return []

        print(f"✅ Se encontraron {len(events)} eventos.")
        return events

    except Exception as error:
        print(f"❌ Ocurrió un error al consultar el calendario: {error}")
        import traceback
        traceback.print_exc()
        raise error


def schedule_meeting(summary: str, start_time: str, end_time: str, attendees: list = None) -> dict:
    """
    Programa una nueva reunión en el calendario de Google.

    Args:
        summary (str): Título del evento.
        start_time (str): Hora de inicio del evento en formato ISO 8601 (ej. "2023-10-27T09:00:00-07:00").
        end_time (str): Hora de finalización del evento en formato ISO 8601.
        attendees (list): Lista de correos electrónicos de los asistentes.

    Returns:
        dict: Información del evento creado o mensaje de error.
    """
    creds = None
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    credentials_filename = os.getenv("GOOGLE_CREDENTIALS_FILE", "hack-475720-a80832b916e2.json")
    credentials_file = os.path.join(current_dir, credentials_filename)

    try:
        if os.path.exists(credentials_file):
            creds = service_account.Credentials.from_service_account_file(
                credentials_file, scopes=SCOPES
            )
        elif os.path.exists(os.path.join(current_dir, "token.json")):
            creds = Credentials.from_authorized_user_file(
                os.path.join(current_dir, "token.json"), SCOPES
            )

        if not creds:
            raise Exception(f"No se pudieron cargar las credenciales desde: {credentials_file}")

        if hasattr(creds, 'expired') and creds.expired and hasattr(creds, 'refresh_token') and creds.refresh_token:
            creds.refresh(Request())

        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',  # Ajusta la zona horaria según sea necesario
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',  # Ajusta la zona horaria según sea necesario
            },
            'attendees': [{'email': att} for att in attendees] if attendees else [],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
        print(f"✅ Evento creado: {event.get('htmlLink')}")
        return {"status": "success", "event_link": event.get('htmlLink'), "event_id": event.get('id')}

    except Exception as error:
        print(f"❌ Ocurrió un error al programar la reunión: {error}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(error)}


# Google ADK Agent
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='calendar_agent',
    description='A helpful assistant for calendar availability and scheduling.',
    instruction='Answer user questions about calendar availability and scheduling to the best of your knowledge. Use the available tools to fetch real-time information.',
    tools=[check_calendar_availability, schedule_meeting],
)

