import torch
import re
from transformers import pipeline


def generate_max_tokens(prompt: str) -> int:
    base_tokens = 50
    additional_for_char = 1
    return base_tokens + len(prompt) * additional_for_char


class TransformService:
    def __init__(self):
        self.pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v0.6", torch_dtype=torch.bfloat16,
                             device_map="auto")

    def ask(self, question: str) -> str:
        messages = [
            {'role': 'system',
             'content': "You are a chatbot that generates SQL queries based on provided database structures. You "
                        "always response only a query without any explanation"},
            {'role': 'user',
             'content': question}
        ]

        prompt = self.pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        max_new_tokens = generate_max_tokens(prompt)
        outputs = self.pipe(prompt, max_new_tokens=max_new_tokens, do_sample=False, top_k=50)
        parts = outputs[0]["generated_text"].split("</s>")
        if len(parts) >= 3:
            parts = parts[2].strip()
            parts = re.sub(r"```\s?|\s?```", "", parts).replace("<|assistant|>", "").replace('\n', ' ')
            parther = r"(SELECT.*?;)"
            result = re.search(parther, parts, re.IGNORECASE | re.DOTALL)
            return result.group(1).replace("  ", " ")
        else:
            return ""
