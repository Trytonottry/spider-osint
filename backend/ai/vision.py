# ai/vision.py
import cv2
from deepface import DeepFace

def detect_faces(image_urls: list) -> list:
    faces = []
    for url in image_urls:
        try:
            # Загрузка изображения (реализовать через requests)
            # faces = DeepFace.extract_faces(url)  # Пример
            # Упрощённо:
            faces.append({"url": url, "detected": True})
        except:
            continue
    return faces