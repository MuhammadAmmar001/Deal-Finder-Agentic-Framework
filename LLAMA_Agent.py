from agent import Agent
import modal

class LLAMA_Agent(Agent):

    name = "LLAMA_Agent"
    color =  Agent.MAGENTA

    def __init__(self):
        self.log("LLAMA AGENT IS INITIALIZING")        
        Price_Predict = modal.Cls.lookup("Llama_Pricer","Price_Predict")
        self.pricer_Obj = Price_Predict()
        
        self.log("LLAMA AGENT IS READY")

    def price(self,desc):
        self.log("LLAMA AGENT IS ESTIMATING PRICE")
        price = self.pricer_Obj.price.remote(desc)
        self.log(f"LLAMA AGENT HAS ESTIMATED {price:.2f}")
        return price