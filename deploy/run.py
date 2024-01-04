import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model_id = "HuggingFaceH4/zephyr-7b-beta"
peft_model_id = "poundian/down-to-the-ship"


parser = argparse.ArgumentParser()
parser.add_argument('prompt')
args = parser.parse_args()
prompt = f'"{args.prompt}"'


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_config
)
model.load_adapter(peft_model_id)

tokenizer = AutoTokenizer.from_pretrained(model_id, add_bos_token=True)


model_input = tokenizer(prompt, return_tensors="pt").to("cuda")
model.eval()

with torch.no_grad():
    output = model.generate(**model_input, max_new_tokens=100, repetition_penalty=1.15)[0]
    print(tokenizer.decode(output, skip_special_tokens=True))
