from openai import OpenAI
from smsManager import sendMessage  
import os
from dotenv import load_dotenv

load_dotenv()




## ASKS CHATGPT API TO SUGGEST 4 ARTICLES TO SEND TO A TEENIOR, 
# BASED ON THE PROBLEM DESCRIPTION FROM THE EMAIL
def generateLinks(prom): 
    client = OpenAI(api_key=os.getenv("gpt_key"))

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful Information Technology assistant"},
            {
            "role": "user",
            "content": "Provide a list of four links for " + str(prom) + "without further description"
          }
        ]   
    ) 

    ##print(completion)

    ##Send links to SMS
    sendMessage("We'll send you some articles that might help with " + str(prom) + " shortly.]\\n\n")
    sendMessage(completion.choices[0].message)