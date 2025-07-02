import logging 

class Agent():

    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background color
    BG_BLACK = '\033[40m'
    
    # Reset code to return to default color
    RESET = '\033[0m'
    name:str = ""
    color:str = WHITE

    def log(self,message):
        named_message = f"[{self.name}] {message}"
        color_code = self.BG_BLACK + self.color
        logging.info(color_code+named_message+self.RESET)