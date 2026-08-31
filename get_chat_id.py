import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("Сначала задай TELEGRAM_BOT_TOKEN", file=sys.stderr)
        return 1

    request = Request(
        f"https://api.telegram.org/bot{token}/getUpdates",
        data=urlencode({"limit": 100}).encode("utf-8"),
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        print(f"Ошибка Telegram API: {exc}", file=sys.stderr)
        return 1

    if not payload.get("ok"):
        print(payload, file=sys.stderr)
        return 1

    chats = {}
    for update in payload.get("result", []):
        message = update.get("message") or update.get("channel_post") or update.get("edited_message")
        if not message or not message.get("chat"):
            continue
        chat = message["chat"]
        chats[str(chat["id"])] = {
            "title": chat.get("title") or chat.get("first_name") or "без названия",
            "type": chat.get("type"),
        }

    if not chats:
        print("Чаты не найдены. Напиши боту /start или отправь сообщение в группу, затем повтори команду.")
        return 0

    print("Найденные чаты:")
    for chat_id, info in chats.items():
        print(f"TELEGRAM_CHAT_ID={chat_id}  ({info['type']}, {info['title']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
