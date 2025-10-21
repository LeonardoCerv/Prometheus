import datetime
import os
from typing import Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Scopes necesarios para Google Calendar (read and write)
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    """
    Obtiene las credenciales de Google OAuth.
    
    Returns:
        Credentials: Credenciales de Google OAuth
    """
    creds = None
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_file = os.path.join(current_dir, "token.json")
    credentials_file = os.path.join(current_dir, "credentials.json")
    
    # Intenta cargar el token existente
    if os.path.exists(token_file):
        print(f"📄 Cargando token desde: {token_file}")
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Si no hay credenciales válidas disponibles, solicita al usuario que inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refrescando token expirado...")
            creds.refresh(Request())
        else:
            print("🔐 Iniciando flujo de autenticación OAuth...")
            if not os.path.exists(credentials_file):
                raise Exception(f"No se encontró el archivo de credenciales: {credentials_file}")
            
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guarda las credenciales para la próxima ejecución
        print(f"💾 Guardando token en: {token_file}")
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def check_calendar_availability():
    """
    Obtiene los próximos eventos del calendario de Google.
    
    Returns:
        list: Lista de eventos próximos del calendario
    """
    try:
        creds = get_credentials()

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


def schedule_meeting(summary: str, start_time: str, end_time: str, attendees: list[str] = []) -> dict:
    """
    Programa una nueva reunión en el calendario de Google.

    Args:
        summary (str): Título del evento.
        start_time (str): Hora de inicio del evento en formato ISO 8601 (ej. "2023-10-27T09:00:00-07:00").
        end_time (str): Hora de finalización del evento en formato ISO 8601.
        attendees (list[str]): Lista de correos electrónicos de los asistentes.

    Returns:
        dict: Información del evento creado o mensaje de error.
    """
    try:
        creds = get_credentials()
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
    model='gemini-2.0-flash-exp',  # Changed to a more stable model
    name='calendar_agent',
    description='A helpful assistant for calendar availability and scheduling.',
    instruction="""You are a calendar scheduling assistant. When scheduling meetings:
1. Always confirm all details: title, date, time, and attendees
2. For dates and times, convert them to ISO 8601 format: YYYY-MM-DDTHH:MM:SS-07:00
3. Current timezone is America/Los_Angeles (PST/PDT)
4. When calling schedule_meeting, use proper ISO format for start_time and end_time
5. Example: For October 22, 2025 at 9:00 AM, use "2025-10-22T09:00:00-07:00"
6. Always provide helpful confirmation messages after scheduling

Answer user questions about calendar availability and scheduling to the best of your knowledge. Use the available tools to fetch real-time information.""",
    tools=[check_calendar_availability, schedule_meeting],
)

