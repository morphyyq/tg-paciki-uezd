# Telegram-бот ежедневного счётчика

Бот отправляет в Telegram сообщение один раз в день в 15:00 по Москве:

> С уезда пацанов прошел 1 день

На следующий день будет `2 дня`, затем `3 дня`, `4 дня`, `5 дней` и так далее. Первый день: **2026-08-31**.

## Важно про токен

Токен, который был отправлен в чате, считается скомпрометированным. Сначала открой `@BotFather`, выполни `/revoke`, выбери бота, затем создай новый токен через `/token`. Настоящий токен нельзя добавлять в файлы GitHub.

## 1. Подготовить чат

1. Открой своего бота в Telegram и нажми **Start**, если сообщения должны приходить лично тебе.
2. Если сообщение должно идти в группу, добавь туда бота и отправь в группе `/start`.
3. На компьютере задай новый токен и запусти:

```bash
TELEGRAM_BOT_TOKEN='НОВЫЙ_ТОКЕН' python get_chat_id.py
```

Команда покажет строки вида `TELEGRAM_CHAT_ID=123456789`. Для группы ID обычно отрицательный.

## 2. Загрузить проект на GitHub

Создай новый репозиторий, например `telegram-counter-bot`, и загрузи в него эти файлы:

- `bot.py`
- `get_chat_id.py`
- `requirements.txt`
- `render.yaml`
- `.gitignore`
- `.env.example`
- `README.md`

Не загружай `.env` и не вставляй токен в код.

Через Git в папке проекта:

```bash
git init
git add .
git commit -m "Create daily Telegram counter bot"
git branch -M main
git remote add origin https://github.com/ТВОЙ_ЛОГИН/telegram-counter-bot.git
git push -u origin main
```

## 3. Подключить GitHub к Render

1. Открой Render и выбери **New + → Cron Job**.
2. Подключи GitHub-репозиторий `telegram-counter-bot` и ветку `main`.
3. Если Render не подхватит `render.yaml` автоматически, укажи вручную:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Schedule:** `0 12 * * *`
4. В **Environment Variables** добавь:
   - `TELEGRAM_BOT_TOKEN` = новый токен от BotFather
   - `TELEGRAM_CHAT_ID` = ID нужного чата
   - `START_DATE` = `2026-08-31`
   - `TIMEZONE` = `Europe/Moscow`
5. Нажми **Create Cron Job**.

Расписание Render задаётся в UTC. Поэтому `0 12 * * *` означает 15:00 по Москве при московском времени UTC+3.

## 4. Проверка первого сообщения сегодня

После создания Cron Job запусти его вручную кнопкой **Run now**. Тогда бот отправит сегодняшнее сообщение с числом `1`. Затем Render будет запускать его каждый день по расписанию.

Если ручной запуск уже был выполнен сегодня, не запускай его повторно, иначе получишь дубликат.

## Локальная проверка без отправки

Для обычного запуска нужны только переменные окружения:

```bash
export TELEGRAM_BOT_TOKEN='НОВЫЙ_ТОКЕН'
export TELEGRAM_CHAT_ID='ID_ЧАТА'
export START_DATE='2026-08-31'
export TIMEZONE='Europe/Moscow'
python bot.py
```

## Стоимость Render

У Render для Cron Job есть минимальная месячная плата, поэтому этот вариант не является полностью бесплатным. Бесплатный Web Service для такого сценария ненадёжен: Render останавливает бесплатные web-сервисы после периода без входящего трафика.
