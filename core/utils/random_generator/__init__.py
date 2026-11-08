"""随机变量生成工具包：日期、时间戳、身份证、中英文姓名、手机号、整数、字符串。"""

from __future__ import annotations

from core.utils.random_generator.date_generator import generate_date, generate_today
from core.utils.random_generator.id_card_generator import generate_id_card
from core.utils.random_generator.integer_generator import generate_integer
from core.utils.random_generator.name_generator import (
    generate_chinese_name,
    generate_english_name,
)
from core.utils.random_generator.phone_generator import generate_phone
from core.utils.random_generator.string_generator import generate_string
from core.utils.random_generator.timestamp_generator import generate_timestamp

__all__ = [
    "generate_date",
    "generate_today",
    "generate_timestamp",
    "generate_id_card",
    "generate_chinese_name",
    "generate_english_name",
    "generate_phone",
    "generate_integer",
    "generate_string",
]
