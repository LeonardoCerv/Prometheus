import datetime
import os
from zoneinfo import ZoneInfo
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Scopes necesarios para Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


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


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# Google ADK Agent
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='calendar_weather_agent',
    description='A helpful assistant for calendar availability, weather and time questions.',
    instruction='Answer user questions about calendar availability, time and weather to the best of your knowledge. Use the available tools to fetch real-time information.',
    tools=[check_calendar_availability, get_weather, get_current_time],
)

