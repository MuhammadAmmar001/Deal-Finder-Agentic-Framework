import os 
from dotenv import load_dotenv
from Planner_Agent import Planner_Agent
import json
import logging
import sys
from deals import Opportunity
import chromadb

def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [Agents] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

class Agentic_Framework:
    name = "Agentic Framework"
    BG_BLUE = '\033[44m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    MEMORY_FILENAME = "memory.json"
    DB = "product_vectorstore"
    COLLECTION_NAME = "products"
    
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    def __init__(self):
        init_logging()
        self.log("AGENTIC FRAMEWORK IS INITIALIZING")
        self.planner_agent = None

        self.client = chromadb.PersistentClient(self.DB)
        self.collection = self.client.get_or_create_collection(self.COLLECTION_NAME)
        self.memory = self.read_memory()
        
        self.log("AGENTIC FRAMEWORK IS READY")

    def ready_planner_agent(self,collection):
        if not self.planner_agent:
            self.log("AGENTIC FRAMEWORK IS INITIALIZING PLANNER AGENT")
            self.planner_agent = Planner_Agent(self.collection)    
            self.log("AGENTIC FRAMEWORK HAS INITIALIZED PLANNER AGENT")

    def read_memory(self):
        if os.path.exists(self.MEMORY_FILENAME):
            with open(self.MEMORY_FILENAME,'r') as file:
                data = json.load(file)
                results = [Opportunity(**opp) for opp in data]
                return results
        return []

    def write_memory(self):
        data = [opp.model_dump() for opp in self.memory]
        with open(self.MEMORY_FILENAME,'w') as file:
            json.dump(data,file,indent=2)

    def log(self,message):
        text = f"{self.BG_BLUE}{self.WHITE} [AGENTIC FRAMEWORK] {message} {self.RESET}"
        logging.info(text)

    def run(self):
        self.log("KICKING OFF PLANNER AGENT")
        self.ready_planner_agent(self.collection)
        best_opp = self.planner_agent.plan(memory = self.memory)
        self.log(f"PLANNER AGENT HAS RETURNED WITH {best_opp}")
        if best_opp:
            self.memory.append(best_opp)
            self.write_memory()
        return self.memory

if __name__ == "__main__":
    Agentic_Framework().run()
        

    