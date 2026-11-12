"""随机数据生成器。"""

from service.utils.random_generator.date_generator import generate_date, generate_today
from service.utils.random_generator.email_generator import generate_email
from service.utils.random_generator.id_card_generator import generate_id_card
from service.utils.random_generator.integer_generator import generate_integer
from service.utils.random_generator.name_generator import generate_chinese_name, generate_english_name
from service.utils.random_generator.phone_generator import generate_phone
from service.utils.random_generator.string_generator import generate_string
from service.utils.random_generator.timestamp_generator import generate_timestamp

__all__ = [
    "generate_chinese_name",
    "generate_date",
    "generate_email",
    "generate_english_name",
    "generate_id_card",
    "generate_integer",
    "generate_phone",
    "generate_string",
    "generate_timestamp",
    "generate_today",
]
