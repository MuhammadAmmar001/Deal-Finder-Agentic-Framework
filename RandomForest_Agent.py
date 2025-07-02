from sentence_transformers import SentenceTransformer
from agent import Agent
import pickle

class RandomForest_Agent(Agent):

    name = "Random_Forest_Agent"
    color =  Agent.GREEN

    def __init__(self):
        self.log("RANDOM FOREST AGENT IS INITIALIZING")
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        with open('rf_model.pkl','rb')as f:
            self.rf_model = pickle.load(f)
        
        self.log("RANDOM FOREST AGENT IS READY")

    def price(self,desc):
        self.log("RANDOM FOREST AGENT IS ESTIMATING PRICE")
        description_vector = self.encoder.encode([desc])
        price = max(self.rf_model.predict(description_vector)[0],0)
        
        self.log(f"RANDOM FOREST AGENT HAS ESTIMATED {price:.2f}")
        return price