# ai/nlp.py
from transformers import pipeline
import spacy

# Загрузка моделей
sentiment_pipeline = pipeline("sentiment-analysis", model="blanchefort/russian-sentiment")
nlp_spacy = spacy.load("ru_core_news_sm")

def analyze(text: str) -> dict:
    return {
        "sentiment": sentiment(text),
        "entities": extract_entities(text),
        "summary": summarize(text)
    }

def sentiment(text: str) -> str:
    try:
        result = sentiment_pipeline(text[:512])
        return result[0]["label"]
    except:
        return "neutral"

def extract_entities(text: str) -> list:
    doc = nlp_spacy(text)
    return [{"text": ent.text, "type": ent.label_} for ent in doc.ents]

def summarize(text: str) -> str:
    # Упрощённо: обрезка
    return text[:200] + "..." if len(text) > 200 else text