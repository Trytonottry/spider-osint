# ai/assistant.py
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class OSINTAssistant:
    def __init__(self, model="Grossmend/rudialogpt3-large"):
        try:
            self.generator = pipeline("text-generation", model=model, device=0 if torch.cuda.is_available() else -1)
        except:
            logger.warning("GPU not available, using CPU for assistant.")
            self.generator = pipeline("text-generation", model=model, device=-1)

    def ask(self, query: str, context: str, max_tokens: int = 200) -> str:
        prompt = f"""
        Ты — ИИ-аналитик OSINT-системы SPIDER. Отвечай кратко, по делу, на русском.

        Контекст:
        {context[:2000]}

        Вопрос: {query}
        Ответ:
        """
        try:
            output = self.generator(prompt, max_length=max_tokens, num_return_sequences=1, temperature=0.7)
            text = output[0]['generated_text']
            return text.split("Ответ:")[-1].strip()
        except Exception as e:
            return f"Ошибка ИИ: {str(e)}"