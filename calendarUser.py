import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/gmail.readonly"]

data = []


## Search in Teenior's Calendar events for events 
# involving coaching sessions

def searchCalendar(events):
    
   # If event contains Teeniors Coaching Session keyword, 
   # send SMS notification with scraped data 
    for event in events: 
      if event["summary"].find("Coaching Session") != -1: 

        ##Retrieves Appointment Time 
        start = event["start"].get("dateTime", event["start"].get("date"))
        
        ##Retrieves Appointment Location
        location = event["location"]

        ##Checks if Appointment Time is Within 24 Hours 
        

        ##Retrieves Client Name 
        startIDX = event["summary"].find("w/") + 2
        endIDX = event["summary"].find("+")
        ##print(str(startIDX) + " " + str(endIDX))
        nPlaceHolder = str(event["summary"])  
        clientName = nPlaceHolder[startIDX:endIDX] 
        data.append(clientName) 
        data.append(start)
        data.append(location)

        ##Send client name to email manager 

        
        return data
      

      
## LOADS THE GOOGLE CALENDAR API

def startCal():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    ##print("Gathering Coaching Session Data...")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    ## TRIGGERS SEARCH FOR COACHING SESSION EVENTS 
    if not events:
      print("No upcoming events found.")
      return
    else: 
      return searchCalendar(events)



        ##Prints Event Summary
        ##print(start, event["summary"]) 

  except HttpError as error:
    print(f"An error occurred: {error}") 
    return "Error or No Events"  



##Main
startCal()