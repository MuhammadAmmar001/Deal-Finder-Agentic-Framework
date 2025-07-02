import re
from bs4 import BeautifulSoup
import requests
from typing import List,Dict,Self
from tqdm import tqdm
import feedparser
import time
from pydantic import BaseModel


feeds = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
        "https://www.dealnews.com/c39/Computers/?rss=1",
        "https://www.dealnews.com/c238/Automotive/?rss=1",
        "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
        "https://www.dealnews.com/c196/Home-Garden/?rss=1",
       ]

def extract_summary(html_snippet:str):
    soup = BeautifulSoup(html_snippet,"html.parser")
    summary_div = soup.find("div",class_="snippet summary")
    if summary_div:
        summary_div_text = summary_div.get_text(strip=True)
        # summary = BeautifulSoup(summary_div_text,'html.parser').get_text()
        cleaned_summary = re.sub("<[^<]+?>","",summary_div_text)
        result = cleaned_summary.strip()
    else:
        result = html_snippet.strip()
    return result.replace('\n'," ")

class ScrappedDeals:

    title:str
    summary:str
    url:str
    details:str
    features:str

    def __init__(self,entry:Dict[str,str]):
        self.title = entry['title']
        self.summary = extract_summary(entry['summary'])
        self.url = entry['links'][0]['href']
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content,'html.parser')
        content = soup.find("div",class_="content-section").get_text()
        content = content.replace("\nmore","").replace('\n','')
        
        if "Features" in content:
            self.details,self.features = content.split("Features")
        else:
            self.details = content
            self.features = ""

    def __repr__(self):
        return f"<{self.title}>"

    def describe(self):
        return f"<TITLE: {self.title}\nDETAILS: {self.details.strip()}\nFEATURES: {self.features}\nURL: {self.url}>"

    @classmethod
    def fetch(cls,show_progress:bool = False) -> List[Self]:
        deals = []
        feed_iter = tqdm(feeds) if show_progress else feeds
        for feed_urls in feed_iter:
            feed = feedparser.parse(feed_urls)
            for entry in feed.entries[:10]:
                deals.append(cls(entry))
                time.sleep(0.5)
        return deals


class Deal(BaseModel):
    product_description:str
    price:float
    url:str
    
class DealSelection(BaseModel):
    deals:List[Deal]
    
class Opportunity(BaseModel):
    deal:Deal
    estimate:float
    discount:float
        






        
        
    
    
    
    