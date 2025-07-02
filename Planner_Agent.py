from agent import Agent
from Scrapping_Agent import Scrapping_Agent
from Ensemble_Agent import Ensemble_Agent
from Messaging_Agent import Messaging_Agent
from typing import List,Optional
from deals import Deal,Opportunity


class Planner_Agent(Agent):
    name = "Planner Agent"
    color = Agent.WHITE
    DISCOUNT_THRESHOLD = 50

    def __init__(self,collection):
        self.log("PLANNER AGENT IS INITIALIZING")
        
        self.scrapping_agent = Scrapping_Agent()
        self.en_agent = Ensemble_Agent(collection)
        self.msg_agent = Messaging_Agent()
        
        self.log("PLANNER AGENT HAS INITIALIZED")

    def make_opportunity(self,deal:Deal) -> Opportunity:
        prod_desc = deal.product_description
        estimate = self.en_agent.price(prod_desc)
        discount = estimate - deal.price
        self.log(f"PLANNER AGENT HAS FOUND A DEAL WITH ${discount:.2f} DISCOUNT")
        return Opportunity(deal=deal,estimate=estimate,discount=discount)
    
    def plan(self,memory) -> Optional[Opportunity]:
        self.log("PLANNER AGENT HAS CALLED SCRAPPER AGENT")
        deals_list = self.scrapping_agent.scan(memory = memory)
        if deals_list:
            opportunities = [self.make_opportunity(deal) for deal in deals_list.deals[:5]]
            opportunities.sort(key=lambda opp: opp.discount,reverse=True)
            best = opportunities[0]
            self.log(f"PLANNER AGENT HAS FOUND THE BEST DEAL HAS DISCOUNT ${best.discount:.2f}")
            if best.discount >= self.DISCOUNT_THRESHOLD:
                self.msg_agent.alert(best)

            self.log("PLANNING AGENT HAS COMPLETED A RUN")
            return best if best.discount >= self.DISCOUNT_THRESHOLD else None
        else:
            return None
    