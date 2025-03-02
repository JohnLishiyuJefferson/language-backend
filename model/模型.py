import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


device = "mps" if torch.backends.mps.is_available() else "cpu"

model_name = "mistralai/Mistral-7B-v0.1"  # 试试这个

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 测试输入
input_text = "What is the meaning of life?"
inputs = tokenizer(input_text, return_tensors="pt").to(device)

# 生成输出
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=50)

# 解码输出
print(tokenizer.decode(output[0], skip_special_tokens=True))
