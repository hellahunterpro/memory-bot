import hmac
import hashlib
import json
from urllib.parse import unquote, parse_qsl
from fastapi import Header, HTTPException
from config import TELEGRAM_BOT_TOKEN


def validate_telegram_init_data(init_data: str) -> dict:
    """
    Проверяет подпись Telegram initData и возвращает данные пользователя.
    
    Алгоритм описан в документации Telegram:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        # Разбираем строку в словарь: "key1=value1&key2=value2..." -> {"key1": "value1", ...}
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid initData format")
    
    # Достаём hash отдельно (он не участвует в проверке)
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=401, detail="Missing hash in initData")
    
    # Собираем data_check_string: ключи отсортированы алфавитно, значения через \n
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )
    
    # Генерируем secret_key из bot token
    secret_key = hmac.new(
        b"WebAppData",
        TELEGRAM_BOT_TOKEN.encode(),
        hashlib.sha256
    ).digest()
    
    # Вычисляем ожидаемый hash
    expected_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Сравниваем
    if not hmac.compare_digest(expected_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid initData signature")
    
    # Парсим user данные из JSON-строки
    user_data = parsed.get("user")
    if not user_data:
        raise HTTPException(status_code=401, detail="No user data in initData")
    
    try:
        user = json.loads(unquote(user_data))
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid user data format")
    
    return user


def get_current_user(authorization: str = Header(None)) -> dict:
    """
    FastAPI dependency для извлечения пользователя из заголовка Authorization.
    
    Frontend будет слать: Authorization: tma <init_data_string>
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Ожидаем формат "tma <init_data>"
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0] != "tma":
        raise HTTPException(status_code=401, detail="Invalid authorization format. Expected: tma <init_data>")
    
    init_data = parts[1]
    return validate_telegram_init_data(init_data)
