# 🕷️ SPIDER v7.1 — OSINT Framework with AI & Multiplatform Support

> **S**ocial **P**enetration, **I**ntelligence, **D**ata **E**xtraction & **R**eporting

**SPIDER** — это модульная, enterprise-уровня OSINT-платформа с ИИ, поддержкой PostgreSQL, веб-интерфейсом, мобильным приложением, Telegram-ботом и нативными сборками.

---

## ✨ Функции

- 🌐 Сбор данных: соцсети, WHOIS, DNS, файлы, изображения
- 🤖 ИИ-анализ: NLP, распознавание лиц, суммаризация
- 💾 Хранение в PostgreSQL + резервное копирование
- 📊 Веб-интерфейс (React) + Мобильное приложение (React Native)
- 📱 Telegram-бот для уведомлений и команд
- 🔐 JWT-аутентификация, аудит, шифрование
- 📦 Нативные сборки: `.exe`, `.AppImage`, `.apk`
- 🔄 Автомониторинг, сравнение изменений, экспорт в CSV/JSON

---

## 🚀 Запуск

```bash
git clone https://github.com/spider-osint/spider
cd spider
cp .env.example .env
# Настройте .env (API-ключи, Telegram и т.д.)
docker-compose up --build
```
- Web UI: http://localhost:3000
- API: http://localhost:8000/docs
- Telegram: @SpiderOsintBot
     
## 📱 Мобильное приложение 
```bash
cd mobile
npm install
npx react-native run-android
```
 
## 🧩 Chrome Extension 

- Перейдите в chrome://extensions
- Включите "Режим разработчика"
- Загрузите папку extension/
     
## 📦 Нативные сборки 

При теге v* GitHub Actions автоматически собирает: 

- spider.exe (Windows)
- spider.AppImage (Linux)
- app-release.apk (Android)
     
Скачайте из GitHub Releases. 
 
## 🛡️ Безопасность 

- Только для легального использования
- Поддержка GDPR/SOC2
- Аудит-логи, шифрование
     
📄 Документация 

    docs/CHANGELOG.md
    docs/SECURITY.md
    Swagger: http://localhost:8000/docs
     
