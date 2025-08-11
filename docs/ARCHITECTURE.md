# Архитектура SPIDER v6.0

## Обзор
SPIDER — модульная, многоуровневая OSINT-платформа с ИИ, поддержкой командной работы и автоматизацией.

## Компоненты
- **Backend**: FastAPI + Celery + PostgreSQL + Neo4j
- **Frontend**: React (Web), React Native (Mobile)
- **Browser Extension**: Chrome Manifest V3
- **Security**: JWT, Fernet, Audit Log
- **Automation**: Celery Beat, Telegram Bot
- **AI**: Hugging Face, DeepFace, rudialogpt3

## Поток данных
1. Пользователь запускает сканирование (CLI/Web/Mobile/Chrome)
2. Запрос проходит аутентификацию (JWT)
3. Ядро определяет тип цели → выбирает модули
4. Модули собирают данные (с прокси/Tor)
5. ИИ анализирует: NLP, Vision, IOCs
6. Результаты сохраняются, генерируется отчёт
7. Уведомление через Telegram
8. Ежедневный мониторинг (Celery Beat)