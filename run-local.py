import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_checkpoint = "dtts-trained"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint)

eval_prompt = "\"What is the last line of Canto IX?\""

model_input = tokenizer(eval_prompt, return_tensors="pt").to("mps")

model.eval()
with torch.no_grad():
    output = model.generate(**model_input, max_new_tokens=100, repetition_penalty=1.15)[0]
    print(tokenizer.decode(output, skip_special_tokens=True))
