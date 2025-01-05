from simplegmail import Gmail # type: ignore
from simplegmail.query import construct_query #type: ignore
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import calendarUser 
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/calendar.readonly"]  

##import client name 



##SEARCHES A GMAIL MESSAGE'S CONTENT TO FIND 
# A CLIENT'S PROBLEM DESCRIPTION 
def problemPrompt(msgs): 
    
    ##print(calendarUser.data[0])

    ##Finds all messages with client name mentioned 
    ##print(len(msgs))
    for m in msgs: 

      ##BOTH OF THESE STATEMENTS WORK SEPARATE, BUT DON'T WORK 
      ##print("Client Found")
      ##print("Match has been found")
      ##prompt for chatgpt will be spliced from "how to" to "You'll be a great coach to fit his/her needs!"
      ##print(m.plain)
      splice = m.plain[m.plain.find("how to"):m.plain.find("You'll be a great coach")] 
      print("Prompt : " + splice)
      return splice

      ##if(m.subject.find("Your Teeniors Private Coaching Session") != -1 and m.plain.find(str(calendarUser.data[0])) != -1): 

      


def startEmail():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
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
    # Call the Gmail API / Edit it to make the build for other user's credentials
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    ##data


    ##Filter to teeniors@gmail.com for sender, then retrieve problem description from client name.  
    gmail = Gmail()  

    ##get date time format 
    dt = datetime.datetime.fromisoformat(calendarUser.data[1])  # Parse the ISO string
    day_of_week = dt.strftime("%a")  # Get day name (e.g., "Monday")
    date = dt.strftime("%d")  # Get date (e.g., "2023-12-20")
    time = dt.strftime("%H")  # Get time (e.g., "14:30") 
    month = dt.strftime("%b") 
    moneker = ["th"]
    
    ##Sets up denoter for day of the month
    if(int(date) == 1):
      moneker[0] = "st"
    elif(int(date) == 2 or int(date) == 22):
      moneker[0] = "nd"
    elif(int(date) == 3 or int(date) == 23): 
      moneker[0] = "rd"

    ## Removes leading zeroes from single-digit days 
    if date[0] == "0":
      date = date[1]    


    ## A for AM, P for PM 
    pmNotation = 'a' 
    
    hr = int(time) 
    if hr > 12: 
      hr %= 12  
      pmNotation = 'p'

    
  
    ##Put together date for subject search 
    paramDate = "(" + day_of_week + ". " + month + ". " + date + moneker[0] + " @ " + str(hr) + pmNotation + ")"


    ##Query parameters 
    query_params = {
      "sender":"teeniors@gmail.com",
      "subject" : "Your Teeniors Private Coaching Session @ " + paramDate or "Your Teeniors Private Coaching Session @ Fatpipe " + paramDate

 
    }
    ##print(query_params)

    ##CREATES FILTER FOR EMAIL SEARCHES
    msgs = gmail.get_messages(query=construct_query(query_params)) 
    print(msgs)
    prblm = problemPrompt(msgs) 
    return prblm

##ERROR EXCEPTION 
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")



