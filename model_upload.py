import modal
from modal import App,Image

app = modal.App("Llama_Pricer")
IMAGE = Image.debian_slim().pip_install('transformers','torch','bitsandbytes','peft','huggingface_hub')
GPU = 'T4'
SECRETS = [modal.Secret.from_name('hf-secret')]

BASE_MODEL = "meta-llama/Llama-3.1-8B"
HUB_ID = "MuhammadAmmar002"
PROJECT_NAME = "pricer"
RUN_NAME = "2025-06-22_07.05.33"
PROJECT_RUN_NAME = f"{PROJECT_NAME}-{RUN_NAME}"
FINE_TUNED_MODEL = f"{HUB_ID}/{PROJECT_RUN_NAME}"
REVISION = "d09f83a032845a691ae4c86aa62042d052da9ef8"
MODEL_DIR = "hf-cache/"
BASE_DIR = f"{MODEL_DIR}+{BASE_MODEL}"
FINE_TUNED_DIR = f"{MODEL_DIR}+{FINE_TUNED_MODEL}"

PREFIX = "How much does this cost to the nearest dollar?"
SUFFIX = "Price is $"

@app.cls(image=IMAGE,secrets=SECRETS,gpu=GPU)
class Price_Predict:
    @modal.build()
    def download_models(self):
        import os
        from huggingface_hub import snapshot_download
        os.makedirs(MODEL_DIR,exist_ok=True)
        snapshot_download(BASE_MODEL,local_dir = BASE_DIR)
        snapshot_download(FINE_TUNED_MODEL,revision=REVISION,local_dir = FINE_TUNED_DIR)

    @modal.enter()
    def setup(self):
        from transformers import AutoTokenizer,AutoModelForCausalLM ,BitsAndBytesConfig
        import torch
        from peft import PeftModel
        
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_DIR)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.pad_side = 'right'
    
        quant_config = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_use_double_quant = True,
            bnb_4bit_compute_dtype = torch.bfloat16,
            bnb_4bit_quant_type = "nf4",
            
        )

        self.base_model = AutoModelForCausalLM.from_pretrained(
            BASE_DIR,
            quantization_config = quant_config,
            device_map = 'auto'
        )

        self.finetuned_model = PeftModel.from_pretrained(self.base_model,FINE_TUNED_DIR)

        
    @modal.method()
    def price(self,desc):
        import torch
        import re
        from transformers import set_seed


        set_seed(42)
        PROMPT = f"{PREFIX}\n{desc}\n{SUFFIX}"
        inputs = self.tokenizer.encode(PROMPT,return_tensors='pt').to('cuda')
        attention_mask = torch.ones(inputs.shape,device='cuda')
        output = self.finetuned_model.generate(inputs,attention_mask = attention_mask,max_new_tokens=5,num_return_sequences=1)
        result = self.tokenizer.decode(output[0])

        contents = result.split("Price is $")[1]
        contents = contents.replace(',','')
        match = re.search(r"[-+]?\d*\.\d+|\d+", contents)
        return float(match.group()) if match else 0
        
        