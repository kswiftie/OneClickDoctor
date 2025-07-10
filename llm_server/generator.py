import torch
from dbmanagers.vectordbmanagers.weaviate_manager import WManager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


class GenerationRequest(BaseModel):
    prompt: str
    max_length: int = 128
    temperature: float = 1.0
    top_p: float = 0.9


class ModelService:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.device = device
        self.model_name = model_name
        self.dbmanager = WManager()

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        ).to(self.device)
        self.model.eval()

    def classify_request(self, query: str) -> int:
        """Классифицирует запрос пользователя и возвращает номер категории"""
        prompt = f"""Определи, к какой категории относится запрос. Ответь ТОЛЬКО цифрой от 1 до 5:
1. Хочу выбрать дату
2. Хочу выбрать время
3. Хочу записаться к врачу
4. Помоги мне выбрать врача
5. Другое

Запрос: "{query}"
Ответ:"""

        messages = [
            {"role": "system", "content": "Отвечай только цифрой от 1 до 5."},
            {"role": "user", "content": prompt},
        ]

        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(self.device)

        try:
            out = self.model.generate(
                input_ids,
                max_new_tokens=2,
                temperature=0.0,
                do_sample=False,
            )

            response = self.tokenizer.decode(
                out[0][input_ids.shape[-1] :], skip_special_tokens=True
            ).strip()

            for char in response:
                if char.isdigit() and 1 <= int(char) <= 5:
                    return int(char)
            return 5

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Classification error: {str(e)}"
            )

    def generate_text(
        self,
        prompt: str,
        max_length: int = 128,
        temperature: float = 1.0,
        top_p: float = 0.9,
    ) -> str:
        """Generates text based on prompt"""
        try:
            helpful_data = self.dbmanager.search_near_data("SymptomDisease", prompt, 1)[
                0
            ]
            new_prompt = f"""Использую следующию информацию:
Симптомы: {helpful_data["symptoms"]}
Специалисты, которые могут помочь: {helpful_data["Doctors"]}
Возможное заболевание: {helpful_data["Diagnosis"]}
Ты собрать эту информацию в удобный для пользователя вид и выдать как качественный осмысленный текст. Ничего больше.
"""
            # prompt += new_prompt
            inputs = self.tokenizer(prompt + new_prompt, return_tensors="pt").to(
                self.device
            )

            out = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

            return self.tokenizer.decode(out[0], skip_special_tokens=True)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")


model_service = ModelService(
    # model_name="C:/Dev/OneClickDoctorEnv/OneClickDoctor/models/TinyLlama-1.1B-Chat-v1.0",
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device="cpu",
)

app = FastAPI(title="TinyLlama API")


@app.post("/generate/")
async def generate(req: GenerationRequest):
    return {
        "generated_text": model_service.generate_text(
            req.prompt, req.max_length, req.temperature, req.top_p
        )
    }


@app.get("/classify/{query}")
async def classify(query: str):
    return {"category": model_service.classify_request(query)}
