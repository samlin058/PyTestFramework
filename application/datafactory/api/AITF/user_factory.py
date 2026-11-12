from domain.assets.api.AITF.function import LoginView
from domain.business.api.AITF.user_biz import create_user as biz_create_user
from service.utils.random_generator.email_generator import generate_email
from service.utils.random_generator.string_generator import generate_string
from service.utils.random_generator.name_generator import generate_chinese_name

# 获取管理员token
def get_admin_token() -> str:
    response = LoginView().post(account="admin", password="123456")
    return response["token"]

# 随机生成一个用户，密码为123456
def create_user() -> str:
    return biz_create_user(
        account=generate_string(prefix='user_'),
        username=generate_chinese_name(),
        email=generate_email(),
        password='123456',
    ).body


if __name__ == "__main__":
    print(get_admin_token())
