import json
import os
import sys
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


def plural_days(number: int) -> str:
    last_two = number % 100
    last = number % 10
    if 11 <= last_two <= 14:
        return "дней"
    if last == 1:
        return "день"
    if 2 <= last <= 4:
        return "дня"
    return "дней"


def today_in_timezone() -> date:
    timezone_name = os.getenv("TIMEZONE", "Europe/Moscow").strip()
    try:
        return date.today() if not timezone_name else __import__("datetime").datetime.now(ZoneInfo(timezone_name)).date()
    except Exception as exc:
        raise RuntimeError(f"Некорректный TIMEZONE={timezone_name!r}: {exc}") from exc


def days_since_start() -> int:
    start_date_text = required_env("START_DATE")
    try:
        start_date = date.fromisoformat(start_date_text)
    except ValueError as exc:
        raise RuntimeError("START_DATE должна быть в формате YYYY-MM-DD, например 2026-08-31") from exc

    current_date = today_in_timezone()
    result = (current_date - start_date).days + 1
    if result < 1:
        raise RuntimeError(
            f"Сегодня {current_date.isoformat()}, а START_DATE={start_date.isoformat()} находится в будущем"
        )
    return result


def telegram_request(token: str, method: str, data: dict) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    body = urlencode(data).encode("utf-8")
    request = Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram API вернул HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise RuntimeError(f"Не удалось подключиться к Telegram API: {exc.reason}") from exc

    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API вернул ошибку: {payload}")
    return payload


def main() -> int:
    token = required_env("TELEGRAM_BOT_TOKEN")
    chat_id = required_env("TELEGRAM_CHAT_ID")
    days = days_since_start()
    message = f"С уезда пацанов прошел {days} {plural_days(days)}"
    telegram_request(token, "sendMessage", {"chat_id": chat_id, "text": message})
    print(f"Отправлено: {message}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        raise SystemExit(1)
