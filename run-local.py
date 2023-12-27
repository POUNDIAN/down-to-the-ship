import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_checkpoint = "dtts-trained"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, locals=True)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

eval_prompt = "\"What is the last line of Canto IX?\""
model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")

model.eval()
with torch.no_grad():
    print(tokenizer.decode(model.generate(**model_input, max_new_tokens=100, repetition_penalty=1.15)[0], skip_special_tokens=True))
