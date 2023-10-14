import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarAPI:
    """
    A class to interact with the Google Calendar API.
    """

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self, token_path="token.json", credentials_path="google_calendar_access.json"):
        """
        Initialize the GoogleCalendarAPI instance.

        :param token_path: Path to the token JSON file for storing authentication data.
        :param credentials_path: Path to the client secrets JSON file for OAuth2 authentication.
        """
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.creds = None

    def authenticate(self):
        """
        Authenticate with the Google Calendar API using OAuth2.

        If authentication is successful, the credentials are saved to a token file.
        """
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

                with open(self.token_path, "w") as token:
                    token.write(self.creds.to_json())

    def create_event(self, event_data):
        """
        Create a new event in the user's Google Calendar.

        :param event_data: A dictionary containing event details.
        :return: The URL of the created event or None if there's an error.
        :raises ValueError: If authentication is required before creating an event.
        """
        if not self.creds:
            raise ValueError("Authentication is required before creating an event.")

        try:
            service = build("calendar", "v3", credentials=self.creds)
            event = service.events().insert(calendarId="primary", body=event_data).execute()
            return event.get("htmlLink")
        except HttpError as error:
            print(f"Error creating event: {error}")
            return None

    def list_events(self):
        """
        List the upcoming events in the user's Google Calendar.

        :raises ValueError: If authentication is required before listing events.
        """
        if not self.creds:
            raise ValueError("Authentication is required before listing events.")

        try:
            service = build("calendar", "v3", credentials=self.creds)
            now = f"{dt.datetime.now().isoformat()}Z"
            event_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True,
                                                 orderBy="startTime").execute()
            print("================== List of next 10 days events! ==================")
            events = event_result.get("items", [])
            if not events:
                print("No upcoming events!")
                return

            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
        except HttpError as error:
            print("Something went wrong!", error)


if __name__ == "__main__":
    calendar_api = GoogleCalendarAPI()

    # Authenticate or re-authenticate as needed
    calendar_api.authenticate()

    if calendar_api.creds:
        event_data = {
            "summary": "Google Calendar API Event With Python",
            "location": "Waterloo",
            "description": "All details of the Google Calendar API",
            "colorId": 7,
            "start": {
                "dateTime": "2023-10-16T10:00:00+01:00",
                "timeZone": "Europe/London"
            },
            "end": {
                "dateTime": "2023-10-16T15:00:00+01:00",
                "timeZone": "Europe/London"
            },
            "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
            "attendees": [
                {"email": "test1@gmail.com"},
                {"email": "test2@hotmail.com"}
            ]
        }

        if event_link := calendar_api.create_event(event_data):
            print(f"Event has been created! {event_link}")

        # List upcoming events
        calendar_api.list_events()
