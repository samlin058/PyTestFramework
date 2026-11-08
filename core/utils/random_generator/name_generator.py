"""随机中英文姓名生成。"""

from __future__ import annotations

import random

# 约 300 个常用姓：前 100 按公安部户籍人口频率；其后按现代常见程度扩展。
# 非《百家姓》顺序。末尾含 10 个常见复姓。
_SURNAMES = [
    "王", "李", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周",
    "徐", "孙", "马", "朱", "胡", "郭", "何", "林", "高", "罗",
    "郑", "梁", "谢", "宋", "唐", "许", "韩", "冯", "邓", "曹",
    "彭", "曾", "肖", "田", "董", "袁", "潘", "于", "蒋", "蔡",
    "余", "杜", "叶", "程", "苏", "魏", "吕", "丁", "任", "沈",
    "姚", "卢", "姜", "崔", "钟", "谭", "陆", "汪", "范", "金",
    "石", "廖", "贾", "夏", "韦", "付", "方", "白", "邹", "孟",
    "熊", "秦", "邱", "江", "尹", "薛", "闫", "段", "雷", "侯",
    "龙", "史", "陶", "黎", "贺", "顾", "毛", "郝", "龚", "邵",
    "万", "钱", "严", "覃", "武", "戴", "莫", "孔", "向", "汤",
    "易", "常", "温", "康", "施", "文", "牛", "樊", "葛", "邢",
    "安", "齐", "伍", "庞", "颜", "倪", "庄", "聂", "章", "鲁",
    "岳", "梅", "欧", "皮", "卞", "曲", "赖", "季", "裴", "翁",
    "舒", "辛", "乔", "翟", "兰", "骆", "甘", "景", "凌", "霍",
    "虞", "柯", "管", "洪", "包", "诸", "左", "涂", "单", "禹",
    "吉", "钮", "荣", "俞", "柳", "鲍", "费", "廉", "岑", "毕",
    "邬", "乐", "时", "傅", "元", "卜", "和", "穆", "萧", "湛",
    "祁", "狄", "米", "贝", "明", "计", "成", "谈", "茅", "阮",
    "蓝", "闵", "席", "麻", "强", "路", "娄", "危", "童", "盛",
    "刁", "经", "房", "裘", "解", "应", "宗", "宣", "郁", "杭",
    "纪", "屈", "项", "祝", "华", "戚", "喻", "柏", "窦", "云",
    "郎", "昌", "苗", "凤", "花", "滕", "殷", "平", "甄", "焦",
    "山", "谷", "车", "全", "班", "仲", "伊", "宫", "宁", "仇",
    "栾", "厉", "符", "詹", "束", "印", "卓", "蔺", "屠", "蒙",
    "池", "阴", "胥", "党", "姬", "申", "冉", "桑", "桂", "阎",
    "连", "茹", "习", "艾", "容", "古", "戈", "都", "耿", "满",
    "匡", "国", "寇", "东", "冷", "阚", "简", "饶", "沙", "关",
    "相", "查", "荆", "红", "游", "权", "盖", "益", "桓", "公",
    "阳", "楚", "卫", "水", "井", "富", "巫", "乌", "巴", "弓",
    "欧阳", "上官", "司马", "诸葛", "司徒", "夏侯", "令狐", "慕容", "皇甫", "宇文",
]

# 约 300 个常用名用字/双字名（以单字为主，末尾保留少量常见双字名）。
_GIVEN_CHARS = [
    "伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
    "勇", "艳", "杰", "娟", "涛", "明", "超", "华", "慧", "巧",
    "美", "霞", "平", "刚", "丹", "萍", "鑫", "亮", "飞", "鹏",
    "波", "斌", "宇", "浩", "凯", "健", "俊", "帆", "宁", "欣",
    "婷", "琳", "雪", "梅", "兰", "竹", "松", "柏", "峰", "岩",
    "川", "海", "河", "山", "云", "风", "晨", "阳", "月", "星",
    "雨", "露", "秋", "春", "夏", "冬", "文", "武", "德", "志",
    "成", "安", "康", "福", "祥", "瑞", "博", "泽", "轩", "涵",
    "睿", "哲", "恒", "昊", "辰", "一", "凡", "天", "翔", "旭",
    "辉", "龙", "虎", "坤", "乾", "钧", "锋", "锐", "威", "雄",
    "豪", "毅", "诚", "信", "义", "礼", "智", "忠", "孝", "仁",
    "善", "正", "东", "南", "北", "中", "国", "建", "卫", "永",
    "远", "长", "久", "兴", "旺", "发", "达", "昌", "盛", "雅",
    "怡", "悦", "心", "思", "梦", "瑶", "琪", "倩", "颖", "洁",
    "莉", "蓉", "菲", "薇", "蕾", "茜", "妍", "嫣", "婉", "柔",
    "淑", "娴", "玲", "珑", "珠", "玉", "珍", "宝", "翠", "碧",
    "青", "蓝", "紫", "红", "彤", "虹", "彩", "锦", "绣", "丝",
    "林", "森", "木", "叶", "花", "草", "苗", "禾", "泉", "溪",
    "湖", "江", "浪", "潮", "冰", "霜", "雾", "晖", "光", "影",
    "晴", "朗", "爽", "清", "澈", "石", "金", "银", "子", "墨",
    "然", "诺", "言", "语", "诗", "书", "画", "琴", "棋", "歌",
    "舞", "乐", "音", "韵", "律", "调", "和", "鸣", "逸", "闲",
    "淡", "泊", "深", "新", "初", "始", "终", "元", "亨", "利",
    "贞", "嘉", "吉", "庆", "喜", "欢", "笑", "咏", "吟", "航",
    "舟", "路", "道", "英", "秀", "俏", "好", "佳", "优", "卓",
    "越", "生", "运", "祺", "淳", "钰", "璇", "瑾", "瑜", "琦",
    "琬", "琰", "璟", "璐", "璧", "珂", "珉", "琛", "琼", "岚",
    "霓", "雯", "霖", "霄", "霆", "桐", "梓", "楠", "槿", "棠",
    "枫", "榆", "柳", "杏", "桃", "梨", "橘", "橙", "莲", "荷",
    "秀英", "秀兰", "桂英", "玉兰", "建华", "志强", "国强", "秀珍", "凤英", "桂兰",
]


_EN_MALE_FIRST = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan", "Jacob",
    "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
    "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Frank",
    "Raymond", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam",
    "Nathan", "Henry", "Douglas", "Zachary", "Peter", "Kyle", "Noah", "Ethan",
    "Jeremy", "Walter", "Christian", "Keith", "Roger", "Terry", "Austin", "Sean",
    "Gerald", "Carl", "Dylan", "Harold", "Jordan", "Jesse", "Bryan", "Billy",
    "Bruce", "Gabriel", "Joe", "Logan", "Alan", "Juan", "Wayne", "Roy",
    "Ralph", "Randy", "Eugene", "Vincent", "Russell", "Louis", "Philip", "Bobby",
]

_EN_FEMALE_FIRST = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela",
    "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra",
    "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather", "Diane",
    "Ruth", "Julie", "Olivia", "Joyce", "Virginia", "Victoria", "Kelly", "Lauren",
    "Christina", "Joan", "Evelyn", "Judith", "Megan", "Andrea", "Cheryl", "Hannah",
    "Jacqueline", "Martha", "Gloria", "Teresa", "Ann", "Sara", "Madison", "Frances",
    "Kathryn", "Janice", "Jean", "Abigail", "Alice", "Judy", "Sophia", "Grace",
    "Denise", "Amber", "Doris", "Marilyn", "Danielle", "Beverly", "Isabella", "Theresa",
]

_EN_LAST = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
    "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray",
    "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel",
]


def _normalize_gender(gender: str | None) -> str | None:
    if gender is None:
        return None
    g = gender.strip().lower()
    if g in {"male", "m", "男"}:
        return "male"
    if g in {"female", "f", "女"}:
        return "female"
    raise ValueError("gender 仅支持 male/female/M/F/男/女")


def generate_chinese_name(
    gender: str | None = None,
    *,
    surname: str | None = None,
    given_length: int | None = None,
) -> str:
    """随机生成中文姓名。

    Args:
        gender: 预留参数（当前中文名库不区分性别，传入不影响结果）。
        surname: 指定姓氏；默认随机。
        given_length: 名字字数，1 或 2；默认随机。

    Returns:
        如 ``张伟``、``李小明``。
    """
    _ = gender  # 预留扩展
    family = surname or random.choice(_SURNAMES)
    length = given_length if given_length is not None else random.choice([1, 2])
    if length not in {1, 2}:
        raise ValueError("given_length 仅支持 1 或 2")

    # 优先从单字库拼名字；多字项只在需要时整体使用
    single_chars = [c for c in _GIVEN_CHARS if len(c) == 1]
    if length == 1:
        given = random.choice(single_chars)
    else:
        # 两字：两个单字 或 一个双字名
        if random.random() < 0.85:
            given = "".join(random.choices(single_chars, k=2))
        else:
            double_chars = [c for c in _GIVEN_CHARS if len(c) == 2]
            given = random.choice(double_chars) if double_chars else "".join(
                random.choices(single_chars, k=2)
            )
    return f"{family}{given}"


def generate_english_name(
    gender: str | None = None,
    *,
    first_name: str | None = None,
    last_name: str | None = None,
) -> str:
    """随机生成英文姓名（First Last）。

    Args:
        gender: ``male`` / ``female`` / ``M`` / ``F`` / ``男`` / ``女``；默认随机。
        first_name: 指定名；默认按性别从常用名库随机。
        last_name: 指定姓；默认随机。

    Returns:
        如 ``James Smith``、``Emily Johnson``。
    """
    normalized = _normalize_gender(gender)
    if first_name is None:
        if normalized is None:
            normalized = random.choice(["male", "female"])
        pool = _EN_MALE_FIRST if normalized == "male" else _EN_FEMALE_FIRST
        first_name = random.choice(pool)
    family = last_name or random.choice(_EN_LAST)
    return f"{first_name} {family}"
