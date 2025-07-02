from deals import ScrappedDeals,Deal,Opportunity,DealSelection
from agent import Agent 
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

class Scrapping_Agent(Agent):
    MODEL = "gpt-4.1-2025-04-14"

    SYSTEM_PROMPT = """You identify and summarize the 5 most detailed deals from a list, by selecting deals that have the most detailed, high quality description and the most clear price.
    Respond strictly in JSON with no explanation, using this format. You should provide the price as a number derived from the description. If the price of a deal isn't clear, do not include that deal in your response.
    Most important is that you respond with the 5 deals that have the most detailed product description with price. It's not important to mention the terms of the deal; most important is a thorough description of the product.
    Be careful with products that are described as "$XXX off" or "reduced by $XXX" - this isn't the actual price of the product. Only respond with products when you are highly confident about the price. 
    
    {"deals": [
        {
            "product_description": "Your clearly expressed summary of the product in 4-5 sentences. Details of the item are much more important than why it's a good deal. Avoid mentioning discounts and coupons; focus on the item itself. There should be a paragpraph of text for each item you choose.",
            "price": 99.99,
            "url": "the url as provided"
        },
        ...
    ]}"""
    
    USER_PROMPT_PREFIX = """Respond with the most promising 5 deals from this list, selecting those which have the most detailed, high quality product description and a clear price that is greater than 0.
    Respond strictly in JSON, and only JSON. You should rephrase the description to be a summary of the product itself, not the terms of the deal.
    Remember to respond with a paragraph of text in the product_description field for each of the 5 items that you select.
    Be careful with products that are described as "$XXX off" or "reduced by $XXX" - this isn't the actual price of the product. Only respond with products when you are highly confident about the price. 
    
    Deals:
    
    """

    USER_PROMPT_SUFFIX = "\n\nStrictly respond in JSON and include exactly 5 deals, no more."

    name = "Scanner Agent"
    color = Agent.MAGENTA

    def __init__(self):
        self.log("SCANNER AGENT IS INITIALIZING")
        load_dotenv()
        self.openai = OpenAI()
        self.log("SCANNER AGENT HAS INITIALIZED")

    def make_prompt(self,deals:List[ScrappedDeals]):
        SYSTEM_PROMPT = self.SYSTEM_PROMPT
        USER_PROMPT = self.USER_PROMPT_PREFIX
        USER_PROMPT += ('\n\n').join([deal.describe() for deal in deals])
        USER_PROMPT += self.USER_PROMPT_SUFFIX
        return [
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':'user','content':USER_PROMPT}
        ]
        

    def scrap_deals(self,memory) -> List[ScrappedDeals]:
        scrapped_deals = ScrappedDeals.fetch(show_progress=True)
        existing_urls = [opp.deal.url for opp in memory]
        new_deals = [scrape for scrape in scrapped_deals if scrape.url not in existing_urls]
        return new_deals

    def scan(self,memory):
        self.log("SCRAPPING AGENT IS SCRAPPING DEALS")
        new_deals = self.scrap_deals(memory)
        if new_deals:
            result = self.openai.beta.chat.completions.parse(
                model = self.MODEL,
                messages = self.make_prompt(new_deals),
                response_format = DealSelection
            )

            result = result.choices[0].message.parsed
            result.deals = [deal for deal in result.deals if deal.price>0]
            
            self.log(f"SCRAPPING AGENT HAS SCRAPPED {len(result.deals)} DEALS")
            return result
            
        else:
            return None
            
            
            
            
            







        