# Руководство пользователя SPIDER

## 1. Установка
```bash
git clone https://github.com/spider-osint/spider
cd spider
cp .env.example .env
docker-compose up --build
```

## 2. Использование 

    CLI: python spider.py --target "test@example.com" --report
    Web: http://localhost:3000
    API: POST /scan → http://localhost:8000/docs
     