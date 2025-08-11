# SPIDER API (FastAPI)

## Авторизация
`POST /token` → получаете JWT

## Маршруты
- `POST /scan` — запуск OSINT
- `POST /ask` — вопрос ИИ-ассистенту
- `GET /reports` — список отчётов
- `GET /audit` — журнал действий (только админ)

## Пример
```bash
curl -X POST http://localhost:8000/scan \
  -H "Authorization: Bearer <token>" \
  -d '{"target": "test@example.com"}'
  ```