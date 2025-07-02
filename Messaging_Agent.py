from agent import Agent
import os 
from dotenv import load_dotenv
import http.client
import urllib

from deals import Opportunity

class Messaging_Agent(Agent):
    name = "MESSAGING AGENT"
    color = Agent.CYAN

    def __init__(self):
        self.log("MESSAGING AGENT IS INITIALIZING")
        load_dotenv()
        self.push_token = os.getenv("PUSHOVER_APP_TOKEN")
        self.push_user = os.getenv("PUSHOVER_USER_TOKEN")
        self.log("MESSAGING AGENT HAS INITIALIZED")

    def push(self,text):
        self.log("MESSAGING AGENT IS SENDING NOTIFICATION")
        
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": self.push_token,
            "user": self.push_user,
            "message": text,
            "sound": "cashregister"
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

    def alert(self,Opp:Opportunity):
        text = f"Deal Alert! Price is ${Opp.deal.price}"
        text += f"Estimated Price is ${Opp.estimate}"
        text += f"Discount on deal is ${Opp.discount}"
        text += f"About Product: {Opp.deal.product_description[:10]} ..."
        text += f"Url of deal is {Opp.deal.url}"
        self.push(text)
        self.log("MESSAGING AGENT SENT A NOTIFICATION")
        