# Google Calendar API Python Wrapper

This Python wrapper simplifies interaction with the Google Calendar API. You can use this class to authenticate with the Google Calendar API, create events, and list upcoming events in your Google Calendar.

## Setup

Before using this class, you need to set up the Google Calendar API and obtain the necessary credentials. Follow these steps:

1. **Enable the Google Calendar API:**

   Visit [Google Calendar API Quickstart](https://developers.google.com/calendar/api/quickstart/python) and click the "Enable the API" button. This will create a new project and enable the Google Calendar API for your project.

2. **Create Credentials:**

   - Go to the [Google Developer Console](https://console.developers.google.com/).
   - Click on your project (or the project you created in the previous step).
   - In the left sidebar, click on "OAuth consent screen" and set up your application's name and other details.
   - Once the consent screen is configured, go to the "Credentials" tab.
   - Click on "Create Credentials" and select "OAuth client ID."
   - Choose "Desktop app" as the application type.
   - Download the credentials as a JSON file and save it as `google_calendar_access.json` in the same directory as your code.

3. **Install Required Libraries:**

   Install the required Google Client Library for Python using pip:

   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

4. **Usage

   Clone or download this repository to your local machine [https://github.com/projectslist/google-calendar-python-API.git].

   Replace the google_calendar_access.json file with the credentials you downloaded from the Google Developer Console.

   Use the GoogleCalendarAPI class in your Python code to interact with the Google Calendar API.


