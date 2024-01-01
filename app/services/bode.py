from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
import torch
from numba import cuda
import gc


def generate_prompt(instruction, input=None):
    if input:
        return f"""Abaixo está uma instrução que descreve uma tarefa, juntamente com uma entrada que fornece mais contexto. Escreva uma resposta que complete adequadamente o pedido.

### Instrução:
{instruction}

### Entrada:
{input}

### Resposta:"""
    else:
        return f"""Abaixo está uma instrução que descreve uma tarefa. Escreva uma resposta que complete adequadamente o pedido.

### Instrução:
{instruction}

### Resposta:"""


class BodeService:
    def __init__(self):
        llm_model = 'recogna-nlp/bode-7b-alpaca-pt-br'
        hf_auth = ''
        config = PeftConfig.from_pretrained(llm_model)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            trust_remote_code=True,
            return_dict=True,
            load_in_8bit=True,
            device_map='auto',
            token=hf_auth
        )

        self.tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path, token=hf_auth)
        self.model = PeftModel.from_pretrained(model, llm_model)
        self.model.to("cuda")
        self.generation_config = GenerationConfig(
            temperature=0.2,
            top_p=0.75,
            num_beams=1,
            do_sample=True
        )

    def ask(self, question: str) -> str:
        with torch.no_grad():
            prompt = generate_prompt(question, input)
            inputs = self.tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].cuda()
            generation_output = self.model.generate(
                input_ids=input_ids,
                generation_config=self.generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=100
            )

        outputs = [self.tokenizer.decode(s) for s in generation_output.sequences]
        del self.model
        del self.tokenizer
        gc.collect()
        torch.cuda.empty_cache()
        cuda.select_device(0)
        cuda.close()
        return outputs[0].split("### Resposta:")[1].strip().replace("</s>","") if outputs else ""
