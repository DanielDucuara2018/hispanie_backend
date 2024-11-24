import random
from typing import Any

import bcrypt


def idv2(prefix: str, *, version: int = 0, code: int = 1022) -> str:  # fix calculation
    random_bytes = (version << 127) + (code << 127) + random.getrandbits(117)
    return f"{prefix}-{random_bytes:032x}"


def generate_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password_hash(hashed_password: bytes, input_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]
