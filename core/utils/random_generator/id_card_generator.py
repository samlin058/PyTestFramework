"""随机中国大陆居民身份证号生成。"""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta

# 全国主要省市行政区划代码（省会/计划单列市等核心城区，满足测试造数）
_AREA_CODES = [
    # 直辖市
    "110101",  # 北京市东城区
    "110105",  # 北京市朝阳区
    "110108",  # 北京市海淀区
    "120101",  # 天津市和平区
    "120103",  # 天津市河西区
    "310101",  # 上海市黄浦区
    "310104",  # 上海市徐汇区
    "310115",  # 上海市浦东新区
    "500101",  # 重庆市万州区
    "500103",  # 重庆市渝中区
    "500105",  # 重庆市江北区
    "500112",  # 重庆市渝北区
    # 华北
    "130102",  # 河北省石家庄市长安区
    "130203",  # 河北省唐山市路北区
    "140105",  # 山西省太原市小店区
    "140106",  # 山西省太原市迎泽区
    "150102",  # 内蒙古呼和浩特市新城区
    "150202",  # 内蒙古包头市东河区
    # 东北
    "210102",  # 辽宁省沈阳市和平区
    "210204",  # 辽宁省大连市沙河口区
    "220102",  # 吉林省长春市南关区
    "220202",  # 吉林省吉林市昌邑区
    "230102",  # 黑龙江省哈尔滨市道里区
    "230103",  # 黑龙江省哈尔滨市南岗区
    # 华东
    "320102",  # 江苏省南京市玄武区
    "320105",  # 江苏省南京市建邺区
    "320205",  # 江苏省无锡市锡山区
    "320508",  # 江苏省苏州市姑苏区
    "330106",  # 浙江省杭州市西湖区
    "330110",  # 浙江省杭州市余杭区
    "330203",  # 浙江省宁波市海曙区
    "330302",  # 浙江省温州市鹿城区
    "340102",  # 安徽省合肥市瑶海区
    "340104",  # 安徽省合肥市蜀山区
    "350102",  # 福建省福州市鼓楼区
    "350203",  # 福建省厦门市思明区
    "360102",  # 江西省南昌市东湖区
    "360111",  # 江西省南昌市青山湖区
    "370102",  # 山东省济南市历下区
    "370202",  # 山东省青岛市市南区
    "370203",  # 山东省青岛市市北区
    # 华中
    "410102",  # 河南省郑州市中原区
    "410105",  # 河南省郑州市金水区
    "420102",  # 湖北省武汉市江岸区
    "420106",  # 湖北省武汉市武昌区
    "420111",  # 湖北省武汉市洪山区
    "430102",  # 湖南省长沙市芙蓉区
    "430104",  # 湖南省长沙市岳麓区
    # 华南
    "440103",  # 广东省广州市荔湾区
    "440106",  # 广东省广州市天河区
    "440304",  # 广东省深圳市福田区
    "440305",  # 广东省深圳市南山区
    "440402",  # 广东省珠海市香洲区
    "440604",  # 广东省佛山市禅城区
    "441900",  # 广东省东莞市
    "450102",  # 广西壮族自治区南宁市兴宁区
    "450103",  # 广西壮族自治区南宁市青秀区
    "460106",  # 海南省海口市龙华区
    "460108",  # 海南省海口市美兰区
    "460203",  # 海南省三亚市吉阳区
    # 西南
    "510104",  # 四川省成都市锦江区
    "510107",  # 四川省成都市武侯区
    "510108",  # 四川省成都市成华区
    "520102",  # 贵州省贵阳市南明区
    "520103",  # 贵州省贵阳市云岩区
    "530102",  # 云南省昆明市五华区
    "530103",  # 云南省昆明市盘龙区
    "540102",  # 西藏自治区拉萨市城关区
    # 西北
    "610102",  # 陕西省西安市新城区
    "610104",  # 陕西省西安市莲湖区
    "610113",  # 陕西省西安市雁塔区
    "620102",  # 甘肃省兰州市城关区
    "620103",  # 甘肃省兰州市七里河区
    "630102",  # 青海省西宁市城东区
    "630104",  # 青海省西宁市城西区
    "640104",  # 宁夏回族自治区银川市兴庆区
    "640105",  # 宁夏回族自治区银川市西夏区
    "650102",  # 新疆维吾尔自治区乌鲁木齐市天山区
    "650103",  # 新疆维吾尔自治区乌鲁木齐市沙依巴克区
]

_WEIGHTS = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
_CHECK_CODES = "10X98765432"


def generate_id_card(
    area_code: str | None = None,
    birth_date: str | date | None = None,
    gender: str | None = None,
) -> str:
    """生成符合校验规则的 18 位身份证号。

    Args:
        area_code: 6 位行政区划代码；默认从内置列表随机选取。
        birth_date: 出生日期，支持 ``YYYY-MM-DD`` / date；默认 18~60 岁随机。
        gender: ``male`` / ``female`` / ``M`` / ``F`` / ``男`` / ``女``；默认随机。

    Returns:
        18 位身份证号字符串。
    """
    code = area_code or random.choice(_AREA_CODES)
    if len(code) != 6 or not code.isdigit():
        raise ValueError("area_code 必须是 6 位数字")

    birthday = _resolve_birth_date(birth_date)
    birth_str = birthday.strftime("%Y%m%d")

    # 顺序码：奇数男，偶数女
    seq = random.randint(0, 999)
    want_odd = _is_male(gender) if gender is not None else None
    if want_odd is True and seq % 2 == 0:
        seq = (seq + 1) % 1000
    elif want_odd is False and seq % 2 == 1:
        seq = (seq + 1) % 1000
    seq_str = f"{seq:03d}"

    body = f"{code}{birth_str}{seq_str}"
    check = _CHECK_CODES[sum(int(n) * w for n, w in zip(body, _WEIGHTS)) % 11]
    return body + check


def _resolve_birth_date(value: str | date | None) -> date:
    if value is None:
        today = date.today()
        # 默认生成 18~60 岁
        end = today.replace(year=today.year - 18)
        start = today.replace(year=today.year - 60)
        delta = (end - start).days
        return start + timedelta(days=random.randint(0, max(delta, 0)))
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def _is_male(gender: str) -> bool:
    normalized = gender.strip().lower()
    if normalized in {"male", "m", "男", "1"}:
        return True
    if normalized in {"female", "f", "女", "0", "2"}:
        return False
    raise ValueError("gender 仅支持 male/female/M/F/男/女")
