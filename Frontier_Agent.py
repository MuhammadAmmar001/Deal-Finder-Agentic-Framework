from agent import Agent
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import re
from sentence_transformers import SentenceTransformer


class Frontier_Agent(Agent):
    name = "FRONTIER AGENT"
    color = Agent.BLUE
    
    MODEL = "gpt-4.1-mini"
    
    def __init__(self,collection):
        self.log(f"INITIALIZING FRONTIER AGENT")
        load_dotenv()
        self.openai = OpenAI()
        self.collection = collection 
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")
        self.log(f"FRONTIER AGENT IS READY")

    def fetch_relevant_docs(self,description):
        self.log('FRONTIER AGENT IS PERFORMING RAG SEARCH TO FIND 5 NEAREST PRODUCTS')
        vector = self.encoder.encode(description)
        results = self.collection.query(
         query_embeddings=vector,
         n_results=5,          
        )
        docs = results['documents'][0][:]
        prices = [m['price'] for m in results['metadatas'][0][:]]
        
        self.log(f'FRONTIER AGENT RETURNED WITH {len(docs)} NEAREST PRODUCTS')
        return docs,prices

    def make_context(self,docs,prices):
        message = "To provide some context, here are some products that might be relevant in estimating the products price"
        for d,p in zip(docs,prices):
            message += f'Potentially Relevant Product\n{d}\nPrice is ${p:.2f}\n\n' 
        return message
        
    def make_user_prompt(self,desc,docs,prices):
        
        self.SYSTEM_PROMPT = "You are a helpful assistant that estimates the price of the products based on their description. You only have to estimate the price of the product and nothing else is required. No explanation, no description nothing except price. For better estimation, you will be provided 5 closest items with their price and description that are relevant to the query product." 

        self.USER_PROMPT = f"Given the description of the product, estimate its price. Dont explain anything just estimate the price only."
        context = self.make_context(docs,prices)
        self.USER_PROMPT += context
        self.USER_PROMPT += f"Now your task is to estimate the price of this product:\n{desc}"

        return [
            {'role':'system','content':self.SYSTEM_PROMPT},
            {'role':'user','content':self.USER_PROMPT},
            {'role':'assistant','content':"Price is $"}
        ]
        
    def get_price(self, s) -> float:
        """
        A utility that plucks a floating point number out of a string
        """
        s = s.replace('$','').replace(',','')
        match = re.search(r"[-+]?\d*\.\d+|\d+", s)
        return float(match.group()) if match else 0.0
        
    def price(self,description):
        docs,prices = self.fetch_relevant_docs(description)
        response = self.openai.chat.completions.create(
            model = self.MODEL,
            messages = self.make_user_prompt(description,docs,prices),
            max_tokens = 5,
            seed = 42
        )
        result = response.choices[0].message.content
        prd_price = self.get_price(result)
        self.log(f"FRONTIER AGENT ESTIMATED ${prd_price}")
        return prd_price
        