from agent import Agent
from LLAMA_Agent import LLAMA_Agent
from Frontier_Agent import Frontier_Agent
from RandomForest_Agent import RandomForest_Agent
import joblib
import pandas as pd

class Ensemble_Agent(Agent):
    name = "ENSEMBLE AGENT"
    color = Agent.YELLOW
    
    def __init__(self,collection):
        self.log("Ensemble Agent is Initializing ")
        self.rf_model = RandomForest_Agent()
        self.fr_model = Frontier_Agent(collection)
        self.ll_model = LLAMA_Agent()
        self.lr_model = joblib.load("lr_model.pkl")
        self.log("Ensemble Agent Is Ready ")

    def price(self,desc):
        self.log("ENSEMBLE AGENT IS ESTIMATING PRICE")
        rf_pred = self.rf_model.price(desc)  
        fr_pred = self.fr_model.price(desc)
        ll_pred = self.ll_model.price(desc)
        Min = min(rf_pred,fr_pred,ll_pred)
        Max = max(rf_pred,fr_pred,ll_pred)
        X = pd.DataFrame({
        "Llama":[ll_pred],
        "Frontier":[fr_pred],
        "RandomForest":[rf_pred],
        "Mins":[Min],
        "Max":[Max]            
        })

        Y = self.lr_model.predict(X)[0]
        self.log(f"ENSEMBLE AGENT HAS ESTIMATED ${Y:.2f}")
        return Y