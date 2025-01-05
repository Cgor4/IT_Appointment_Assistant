##Client key 
import vonage
##from nexmoConfig import client_key, secret_key
import os 
from dotenv import load_dotenv 
load_dotenv() 

client = vonage.Client(key=os.getenv("vonage_client"), secret=os.getenv("vonage_secret")) 
sms = vonage.Sms(client)





## CREATES A REMINDER MESSAGE FROM CLIENT'S DATA, 
## THEN SENDS IT AS AN SMS MESSAGE THROUGH SENDMESSAGE()
def buildApptInfo(name,date,address):
    ##ARRAY FOR MESSAGES TO SEND OUT
    current = "Your Teeniors coaching session is in 24 hours.\n\nClient Name : " + name + "\n\nAddress : " + address + "\n\nDate : " + date + "\n\n"
    sendMessage(current)
    return current



##Main message sender  

def sendMessage(msg):
    ##print("check")

    ## FROM : VONTAGE API 
    ## TO : NUMBER OF TEENIOR YOU'RE SENDING TO 
    ## TEXT : CONTENT OF THE SMS YOU WANT TO SEND 
    responseData = sms.send_message(
    {
        "from": "FROM_NUMBER",
        "to": "5052200411", 
        "text": msg, 
    }
)
    
    if responseData["messages"][0]["status"] == "0":
        print("Message sent.")
    else:
        print(f"Message failed to send with error:{responseData['messages'][0]['error-text']}")


