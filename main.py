##Imports from other files 
from calendarUser import startCal
from emailManager import startEmail
from smsManager import buildApptInfo
from articleRecommender import generateLinks  


##  PROJECT BASICS: 
## * Main file searches Google Calendar, returns events with "Coaching Session" & "Teeniors" 
## * Search Gmail inbox, find the most recent email that corresponds to the next calendar event 
## * Read's the email's content, and figures out what the client's problem is 
## * Texts my phone with my appointment with the client like time, date, location, and problem description 
## * Uses chatGPT to recommend articles that will help with the problem, then text those to me as well. 


##Extracts Calendar / Client Data  
client = startCal()   
print(client)    


##Extracts Client's Problem Description from the invite email 
prompt = startEmail()




##Send SMS Message with Client Detals:  
buildApptInfo(client[0],client[1],client[2])


##Send prompt to articleRecommender to generate links 
generateLinks(prompt)