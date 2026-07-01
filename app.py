import streamlit as st
from datetime import date, datetime
from lunardate import LunarDate

st.set_page_config(page_title="易学助手")

st.title("易学助手 - 八字排盘")

# ========== 基础数据 ==========

TIAN_GAN_PY = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
TIAN_GAN_CN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
GAN_WU_XING = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
GAN_YIN_YANG = ["阳", "阴", "阳", "阴", "阳", "阴", "阳", "阴", "阳", "阴"]

DI_ZHI_PY = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
DI_ZHI_CN = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ZHI_WU_XING = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]

CANG_GAN = {
    "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"], "卯": ["乙"],
    "辰": ["戊", "乙", "癸"], "巳": ["丙", "戊", "庚"], "午": ["丁", "己"],
    "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"], "酉": ["辛"],
    "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"],
}

KONG_WANG = {
    "甲子": ["戌", "亥"], "乙丑": ["戌", "亥"], "丙寅": ["戌", "亥"],
    "丁卯": ["戌", "亥"], "戊辰": ["戌", "亥"], "己巳": ["戌", "亥"],
    "庚午": ["戌", "亥"], "辛未": ["戌", "亥"], "壬申": ["戌", "亥"],
    "癸酉": ["戌", "亥"],
    "甲戌": ["申", "酉"], "乙亥": ["申", "酉"], "丙子": ["申", "酉"],
    "丁丑": ["申", "酉"], "戊寅": ["申", "酉"], "己卯": ["申", "酉"],
    "庚辰": ["申", "酉"], "辛巳": ["申", "酉"], "壬午": ["申", "酉"],
    "癸未": ["申", "酉"],
    "甲申": ["午", "未"], "乙酉": ["午", "未"], "丙戌": ["午", "未"],
    "丁亥": ["午", "未"], "戊子": ["午", "未"], "己丑": ["午", "未"],
    "庚寅": ["午", "未"], "辛卯": ["午", "未"], "壬辰": ["午", "未"],
    "癸巳": ["午", "未"],
    "甲午": ["辰", "巳"], "乙未": ["辰", "巳"], "丙申": ["辰", "巳"],
    "丁酉": ["辰", "巳"], "戊戌": ["辰", "巳"], "己亥": ["辰", "巳"],
    "庚子": ["辰", "巳"], "辛丑": ["辰", "巳"], "壬寅": ["辰", "巳"],
    "癸卯": ["辰", "巳"],
    "甲辰": ["寅", "卯"], "乙巳": ["寅", "卯"], "丙午": ["寅", "卯"],
    "丁未": ["寅", "卯"], "戊申": ["寅", "卯"], "己酉": ["寅", "卯"],
    "庚戌": ["寅", "卯"], "辛亥": ["寅", "卯"], "壬子": ["寅", "卯"],
    "癸丑": ["寅", "卯"],
    "甲寅": ["子", "丑"], "乙卯": ["子", "丑"], "丙辰": ["子", "丑"],
    "丁巳": ["子", "丑"], "戊午": ["子", "丑"], "己未": ["子", "丑"],
    "庚申": ["子", "丑"], "辛酉": ["子", "丑"], "壬戌": ["子", "丑"],
    "癸亥": ["子", "丑"],
}

ZHI_KU = {
    "辰": "水库", "戌": "火库", "丑": "金库", "未": "木库",
}

WU_XING_INDEX = {"木": 0, "火": 1, "土": 2, "金": 3, "水": 4}

SHI_SHEN_NAMES = {
    "同+阳+阳": "比肩", "同+阴+阴": "比肩", "同+阳+阴": "劫财", "同+阴+阳": "劫财",
    "生+阳+阳": "偏印", "生+阴+阴": "偏印", "生+阳+阴": "正印", "生+阴+阳": "正印",
    "我生+阳+阳": "食神", "我生+阴+阴": "食神", "我生+阳+阴": "伤官", "我生+阴+阳": "伤官",
    "克+阳+阳": "偏官", "克+阴+阴": "偏官", "克+阳+阴": "正官", "克+阴+阳": "正官",
    "我克+阳+阳": "偏财", "我克+阴+阴": "偏财", "我克+阳+阴": "正财", "我克+阴+阳": "正财",
}

WU_HU = {
    "Jia": 2, "Ji": 2, "Yi": 4, "Geng": 4,
    "Bing": 6, "Xin": 6, "Ding": 8, "Ren": 8,
    "Wu": 0, "Gui": 0,
}

WU_SHU = {
    "Jia": 0, "Ji": 0, "Yi": 2, "Geng": 2,
    "Bing": 4, "Xin": 4, "Ding": 6, "Ren": 6,
    "Wu": 8, "Gui": 8,
}

ALL_GAN = TIAN_GAN_CN * 6
ALL_ZHI = DI_ZHI_CN * 5
SIXTY_JIAZI = [ALL_GAN[i] + ALL_ZHI[i] for i in range(60)]


# ========== 计算函数 ==========

def get_shi_shen(ri_gan_idx, target_gan_idx):
    if ri_gan_idx == target_gan_idx:
        return "日主"
    ri_wx = WU_XING_INDEX[GAN_WU_XING[ri_gan_idx]]
    t_wx = WU_XING_INDEX[GAN_WU_XING[target_gan_idx]]
    ri_yy = GAN_YIN_YANG[ri_gan_idx]
    t_yy = GAN_YIN_YANG[target_gan_idx]
    diff = (t_wx - ri_wx) % 5
    if diff == 0:
        key = "同"
    elif diff == 1:
        key = "我生"
    elif diff == 2:
        key = "我克"
    elif diff == 3:
        key = "克"
    else:
        key = "生"
    key += "+" + ri_yy + "+" + t_yy
    return SHI_SHEN_NAMES.get(key, "?")


def get_sheng_ke(A, B, tiangan):
    if tiangan == "天干":
        a_wx = GAN_WU_XING[A]
        b_wx = GAN_WU_XING[B]
    else:
        a_wx = ZHI_WU_XING[A]
        b_wx = ZHI_WU_XING[B]
    a_num = WU_XING_INDEX[a_wx]
    b_num = WU_XING_INDEX[b_wx]
    diff = (b_num - a_num) % 5
    if diff == 0:
        return "同"
    elif diff == 1:
        return "生"
    elif diff == 2:
        return "泄"
    elif diff == 3:
        return "耗"
    else:
        return "克"


def get_dayun(yue_zhu_cn, shun_pai, start_age=1, count=8):
    yue_idx = SIXTY_JIAZI.index(yue_zhu_cn)
    dayun = []
    for i in range(count):
        if shun_pai:
            idx = (yue_idx + 1 + i) % 60
        else:
            idx = (yue_idx - 1 - i) % 60
        age = start_age + i * 10
        dayun.append((age, SIXTY_JIAZI[idx]))
    return dayun


def get_liunian(year):
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIAN_GAN_CN[gan_idx] + DI_ZHI_CN[zhi_idx], gan_idx, zhi_idx


def calc_start_age(year, month, day, shun_pai):
    birth = datetime(year, month, day)
    jie_qi = {
        "小寒": (1, 5), "立春": (2, 4), "惊蛰": (3, 6),
        "清明": (4, 5), "立夏": (5, 6), "芒种": (6, 6),
        "小暑": (7, 7), "立秋": (8, 8), "白露": (9, 8),
        "寒露": (10, 8), "立冬": (11, 7), "大雪": (12, 7),
    }
    if shun_pai:
        for i in range(12):
            m = (month - 1 + i) % 12 + 1
            y = year if m >= month else year + 1
            for name, (jm, jd) in jie_qi.items():
                if jm == m:
                    jq_date = datetime(y, jm, jd)
                    if jq_date > birth:
                        days = (jq_date - birth).days
                        if days <= 31:
                            return max(1, round(days / 3))
        return 8
    else:
        for i in range(12):
            m = (month - 1 - i) % 12 + 1
            if m <= 0:
                m += 12
            y = year if m <= month else year - 1
            for name, (jm, jd) in jie_qi.items():
                if jm == m:
                    jq_date = datetime(y, jm, jd)
                    if jq_date < birth:
                        days = (birth - jq_date).days
                        if days <= 31:
                            return max(1, round(days / 3))
        return 8


# ========== 格局函数 ==========

def get_guan_qi(ri_gan, zhi):
    table = {
        "甲": [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3],
        "乙": [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3],
        "丙": [1, 1, 3, 3, 1, 3, 3, 1.3, 1, 1, 0, 1],
        "丁": [1, 1, 3, 3, 1, 3, 3, 1.3, 1, 1, 0.3, 1],
        "戊": [1, 1, 1, 1, 1, 3, 3, 3, 1, 1, 0, 1],
        "己": [1, 1, 1, 1, 1, 3, 3, 3, 1, 1, 3, 1],
        "庚": [1, 0, 1, 1, 3, 1, 1, 1, 3, 3, 1, 1],
        "辛": [1, 3, 1, 1, 3, 1, 1, 1, 3, 3, 1, 1],
        "壬": [3, 1.3, 1, 0, 1, 1, 1, 1, 3, 3, 1, 3],
        "癸": [3, 1.3, 1, 0.3, 1, 1, 1, 1, 3, 3, 1, 3],
    }
    zhi_idx = DI_ZHI_CN.index(zhi)
    return table[ri_gan][zhi_idx]


def is_zao_tu(zhi):
    return zhi in ["戌", "未"]


def is_shi_tu(zhi):
    return zhi in ["辰", "丑"]


def is_tu(zhi):
    return zhi in ["辰", "戌", "丑", "未"]


def check_tu_special(gan, zhi, same_column_gan=None):
    if gan in ["戊", "己"] and is_zao_tu(zhi):
        return "生助"
    if gan in ["戊", "己"] and is_shi_tu(zhi):
        return "克泄耗"
    if is_tu(zhi) and gan in ["戊", "己"]:
        return "克泄耗"
    if gan in ["丙", "丁"] and is_zao_tu(zhi) and same_column_gan == gan:
        return "生助"
    if gan in ["丙", "丁"] and is_shi_tu(zhi):
        return "克泄耗"
    if gan in ["庚", "辛"] and is_zao_tu(zhi):
        return "克泄耗"
    if gan in ["庚", "辛"] and is_shi_tu(zhi):
        return "生助"
    if gan in ["壬", "癸"] and is_shi_tu(zhi) and same_column_gan == gan:
        return "生助"
    if gan in ["壬", "癸"] and is_shi_tu(zhi) and same_column_gan != gan:
        return "克泄耗"
    if is_shi_tu(zhi) and is_zao_tu(gan):
        return "克泄耗"
    if is_zao_tu(zhi) and is_shi_tu(gan):
        return "克泄耗"
    return None


def get_sheng_zhu_or_ke_xie(ri_gan_idx, target_gan_idx, target_zhi, same_column_gan=None):
    target_gan = TIAN_GAN_CN[target_gan_idx]
    ri_gan = TIAN_GAN_CN[ri_gan_idx]
    tu_result = check_tu_special(ri_gan, target_zhi, same_column_gan)
    if tu_result:
        return tu_result
    zhi_idx = DI_ZHI_CN.index(target_zhi)
    zhi_wx = ZHI_WU_XING[zhi_idx]
    ri_wx = GAN_WU_XING[ri_gan_idx]
    zhi_num = WU_XING_INDEX[zhi_wx]
    ri_num = WU_XING_INDEX[ri_wx]
    diff = (zhi_num - ri_num) % 5
    if diff == 0 or diff == 1 or diff == 4:
        return "生助"
    else:
        return "克泄耗"


def check_you_li(gan_idx, zhi_idx, all_gans, all_zhis):
    target_gan = TIAN_GAN_CN[gan_idx]
    target_zhi = DI_ZHI_CN[zhi_idx]
    zhi_wx = ZHI_WU_XING[zhi_idx]
    gan_wx = GAN_WU_XING[gan_idx]
    zhi_num = WU_XING_INDEX[zhi_wx]
    gan_num = WU_XING_INDEX[gan_wx]
    diff = (gan_num - zhi_num) % 5
    if diff == 1 or diff == 0 or diff == 4:
        tu_special = check_tu_special(target_gan, target_zhi, target_gan)
        if tu_special == "生助" or tu_special is None:
            return True
    else:
        tu_special = check_tu_special(target_gan, target_zhi, target_gan)
        if tu_special != "生助":
            return False
    return True


def check_fan_duan(ri_gan, ri_zhi, yue_zhi, nian_zhi, yue_gan_idx, nian_gan_idx, ri_gan_idx, yue_zhi_kong):
    ri_zhi_guan_qi = get_guan_qi(ri_gan, ri_zhi)
    if ri_zhi_guan_qi == 0:
        ri_zhi_effect = get_sheng_zhu_or_ke_xie(ri_gan_idx, ri_gan_idx, ri_zhi)
        ri_zhi_direction = "旺" if ri_zhi_effect == "生助" else "弱"
    elif ri_zhi_guan_qi == 3 or ri_zhi_guan_qi == 1.3 or ri_zhi_guan_qi == 0.3:
        ri_zhi_direction = "旺"
    else:
        ri_zhi_direction = "弱"

    if not yue_zhi_kong:
        used_zhi = yue_zhi
    else:
        used_zhi = nian_zhi
    used_zhi_guan_qi = get_guan_qi(ri_gan, used_zhi)

    if used_zhi_guan_qi == 0:
        used_zhi_effect = get_sheng_zhu_or_ke_xie(ri_gan_idx, ri_gan_idx, used_zhi)
        used_zhi_direction = "旺" if used_zhi_effect == "生助" else "弱"
    elif used_zhi_guan_qi == 3 or used_zhi_guan_qi == 1.3 or used_zhi_guan_qi == 0.3:
        used_zhi_direction = "旺"
    else:
        used_zhi_direction = "弱"

    if ri_zhi_direction == used_zhi_direction:
        return False

    if not yue_zhi_kong:
        ke_count = 0
        nian_zhi_wx = ZHI_WU_XING[DI_ZHI_CN.index(nian_zhi)]
        yue_zhi_wx = ZHI_WU_XING[DI_ZHI_CN.index(yue_zhi)]
        if (nian_zhi_wx == "金" and yue_zhi_wx == "木") or \
           (nian_zhi_wx == "木" and yue_zhi_wx == "土") or \
           (nian_zhi_wx == "土" and yue_zhi_wx == "水") or \
           (nian_zhi_wx == "水" and yue_zhi_wx == "火") or \
           (nian_zhi_wx == "火" and yue_zhi_wx == "金"):
            ke_count += 1
        yue_gan_wx = GAN_WU_XING[yue_gan_idx]
        if (yue_gan_wx == "金" and yue_zhi_wx == "木") or \
           (yue_gan_wx == "木" and yue_zhi_wx == "土") or \
           (yue_gan_wx == "土" and yue_zhi_wx == "水") or \
           (yue_gan_wx == "水" and yue_zhi_wx == "火") or \
           (yue_gan_wx == "火" and yue_zhi_wx == "金"):
            ke_count += 1
        ri_zhi_wx = ZHI_WU_XING[DI_ZHI_CN.index(ri_zhi)]
        if (ri_zhi_wx == "金" and yue_zhi_wx == "木") or \
           (ri_zhi_wx == "木" and yue_zhi_wx == "土") or \
           (ri_zhi_wx == "土" and yue_zhi_wx == "水") or \
           (ri_zhi_wx == "水" and yue_zhi_wx == "火") or \
           (ri_zhi_wx == "火" and yue_zhi_wx == "金"):
            ke_count += 1
        return ke_count >= 2
    else:
        ke_count = 0
        nian_gan_wx = GAN_WU_XING[nian_gan_idx]
        nian_zhi_wx = ZHI_WU_XING[DI_ZHI_CN.index(nian_zhi)]
        if (nian_gan_wx == "金" and nian_zhi_wx == "木") or \
           (nian_gan_wx == "木" and nian_zhi_wx == "土") or \
           (nian_gan_wx == "土" and nian_zhi_wx == "水") or \
           (nian_gan_wx == "水" and nian_zhi_wx == "火") or \
           (nian_gan_wx == "火" and nian_zhi_wx == "金"):
            ke_count += 1
        yue_zhi_wx = ZHI_WU_XING[DI_ZHI_CN.index(yue_zhi)]
        if (yue_zhi_wx == "金" and nian_zhi_wx == "木") or \
           (yue_zhi_wx == "木" and nian_zhi_wx == "土") or \
           (yue_zhi_wx == "土" and nian_zhi_wx == "水") or \
           (yue_zhi_wx == "水" and nian_zhi_wx == "火") or \
           (yue_zhi_wx == "火" and nian_zhi_wx == "金"):
            ke_count += 1
        return ke_count >= 2


def check_shizhi_cheng_ge(geju, shi_zhi, shi_gan, ri_zhi, ri_gan_idx):
    if geju != "从弱格":
        return geju
    ke_shi_gan = get_sheng_zhu_or_ke_xie(ri_gan_idx, TIAN_GAN_CN.index(shi_gan), shi_zhi) == "克泄耗"
    ke_ri_zhi = get_sheng_zhu_or_ke_xie(ri_gan_idx, ri_gan_idx, shi_zhi) == "克泄耗"
    if not (ke_shi_gan or ke_ri_zhi):
        return geju
    if get_sheng_zhu_or_ke_xie(ri_gan_idx, ri_gan_idx, shi_zhi) == "生助":
        return "身弱格"
    return geju


def get_ge_ju(ri_gan_idx, ri_zhi, yue_gan_idx, yue_zhi, shi_gan_idx, shi_zhi, nian_zhi, nian_gan_idx, all_gans, all_zhis):
    ri_gan = TIAN_GAN_CN[ri_gan_idx]
    ri_zhu = ri_gan + ri_zhi
    ri_kong = KONG_WANG.get(ri_zhu, ["", ""])
    yue_zhi_kong = yue_zhi in ri_kong
    if yue_zhi_kong:
        used_zhi = nian_zhi
    else:
        used_zhi = yue_zhi
    guan_qi = get_guan_qi(ri_gan, used_zhi)

    ri_zhi_effect = get_sheng_zhu_or_ke_xie(ri_gan_idx, ri_gan_idx, ri_zhi)
    yue_effect = get_sheng_zhu_or_ke_xie(ri_gan_idx, yue_gan_idx, yue_zhi)
    shi_effect = get_sheng_zhu_or_ke_xie(ri_gan_idx, shi_gan_idx, shi_zhi)

    yue_you_li = check_you_li(yue_gan_idx, DI_ZHI_CN.index(yue_zhi), all_gans, all_zhis)
    shi_you_li = check_you_li(shi_gan_idx, DI_ZHI_CN.index(shi_zhi), all_gans, all_zhis)
    ri_you_li = True

    sheng_zhu_count = 0
    wu_li_count = 0

    if ri_zhi_effect == "生助":
        sheng_zhu_count += 1
    else:
        if not ri_you_li:
            wu_li_count += 1

    if yue_effect == "生助":
        sheng_zhu_count += 1
    else:
        if not yue_you_li:
            wu_li_count += 1

    if shi_effect == "生助":
        sheng_zhu_count += 1
    else:
        if not shi_you_li:
            wu_li_count += 1

    if guan_qi == 3:
        if wu_li_count == 3:
            geju = "从旺格"
        else:
            geju = "身旺格"
    elif guan_qi == 1:
        if sheng_zhu_count == 0 and wu_li_count == 3:
            geju = "从弱格"
        else:
            geju = "身弱格"
    elif guan_qi == 0:
        if ri_zhi_effect == "生助":
            if yue_you_li or shi_you_li:
                geju = "身旺格"
            else:
                geju = "从旺格"
        else:
            if yue_you_li or shi_you_li:
                geju = "身弱格"
            else:
                geju = "从弱格"
    else:
        if sheng_zhu_count == 3:
            geju = "从旺格"
        elif sheng_zhu_count >= 2:
            geju = "身旺格"
        else:
            geju = "身弱格"

    geju = check_shizhi_cheng_ge(geju, shi_zhi, TIAN_GAN_CN[shi_gan_idx], ri_zhi, ri_gan_idx)

    if check_fan_duan(ri_gan, ri_zhi, yue_zhi, nian_zhi, yue_gan_idx, nian_gan_idx, ri_gan_idx, yue_zhi_kong):
        if geju == "身旺格":
            geju = "身弱格"
        elif geju == "身弱格":
            geju = "身旺格"

    return geju


# ========== 界面 ==========

st.subheader("请输入出生信息")

input_mode = st.radio("输入方式", ["公历", "农历", "四柱直输"], horizontal=True)

if input_mode == "公历":
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("年", min_value=1900, max_value=2100, value=2006, step=1)
    with col2:
        month = st.number_input("月", min_value=1, max_value=12, value=10, step=1)
    with col3:
        day = st.number_input("日", min_value=1, max_value=31, value=9, step=1)
    solar_year, solar_month, solar_day = year, month, day
    use_direct = False

elif input_mode == "农历":
    st.caption("输入农历日期，自动转换为公历排盘")
    col1, col2, col3 = st.columns(3)
    with col1:
        lunar_year = st.number_input("农历年", min_value=1900, max_value=2100, value=2006, step=1)
    with col2:
        lunar_month = st.number_input("农历月", min_value=1, max_value=12, value=8, step=1)
    with col3:
        lunar_day = st.number_input("农历日", min_value=1, max_value=30, value=18, step=1)
    is_leap = st.checkbox("闰月")
    try:
        lunar_date = LunarDate(lunar_year, lunar_month, lunar_day, is_leap)
        solar_date = lunar_date.toSolarDate()
        solar_year, solar_month, solar_day = solar_date.year, solar_date.month, solar_date.day
        st.caption(f"对应公历：{solar_year}年{solar_month}月{solar_day}日")
    except Exception as e:
        st.error(f"农历日期无效：{e}")
        solar_year, solar_month, solar_day = 2006, 10, 9
    use_direct = False

else:
    st.caption("直接输入已知的四柱，无需出生日期")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nian_gan = st.selectbox("年干", TIAN_GAN_CN, index=2)
        nian_zhi = st.selectbox("年支", DI_ZHI_CN, index=10)
    with col2:
        yue_gan = st.selectbox("月干", TIAN_GAN_CN, index=4)
        yue_zhi = st.selectbox("月支", DI_ZHI_CN, index=10)
    with col3:
        ri_gan = st.selectbox("日干", TIAN_GAN_CN, index=7)
        ri_zhi = st.selectbox("日支", DI_ZHI_CN, index=7)
    with col4:
        shi_gan = st.selectbox("时干", TIAN_GAN_CN, index=9)
        shi_zhi = st.selectbox("时支", DI_ZHI_CN, index=5)
    use_direct = True

if not use_direct:
    col1, col2 = st.columns(2)
    with col1:
        hour_input = st.number_input("出生时", min_value=0, max_value=23, value=9, step=1)
    with col2:
        minute_input = st.number_input("出生分", min_value=0, max_value=59, value=0, step=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        province = st.text_input("省/直辖市", value="广东")
    with col2:
        city_name = st.text_input("城市", value="佛山")
    with col3:
        district = st.text_input("区/县", value="顺德")

    col1, col2 = st.columns(2)
    with col1:
        lng_input = st.number_input("当地经度（°）", min_value=70.0, max_value=140.0, value=113.3, step=0.1, format="%.1f")
    with col2:
        gender = st.selectbox("性别", ["男", "女"])

    with st.expander("📌 常用城市经度参考"):
        st.caption("北京116.4 | 上海121.5 | 广州113.3 | 深圳114.1 | 成都104.1 | 重庆106.5 | 西安108.9 | 武汉114.3 | 南京118.8 | 杭州120.2 | 哈尔滨126.6 | 沈阳123.4 | 天津117.2 | 昆明102.7 | 贵阳106.7 | 南宁108.3 | 福州119.3 | 郑州113.7 | 济南117.0 | 长沙113.0 | 南昌115.9 | 兰州103.8 | 乌鲁木齐87.6 | 拉萨91.1 | 海口110.3 | 香港114.2 | 台北121.5")

    time_diff = round((lng_input - 120) * 4)
    true_hour = hour_input + time_diff // 60
    true_minute = minute_input + time_diff % 60
    if true_minute >= 60:
        true_hour += 1
        true_minute -= 60
    elif true_minute < 0:
        true_hour -= 1
        true_minute += 60
    if true_hour >= 24:
        true_hour -= 24
    elif true_hour < 0:
        true_hour += 24

    location_str = f"{province} {city_name} {district}" if province else "未知地点"
    st.caption(f"出生地点：{location_str}（经度 {lng_input}°）| 北京时间 {hour_input:02d}:{minute_input:02d} → 真太阳时 {true_hour:02d}:{true_minute:02d}")
else:
    gender = st.selectbox("性别", ["男", "女"])

current_year = st.number_input("查看流年", min_value=1900, max_value=2100, value=2026, step=1)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    btn_paipan = st.button("排盘", use_container_width=True)
with col_btn2:
    btn_jishi = st.button("⚡ 即时起盘（当前时间）", use_container_width=True)

if btn_jishi:
    now = datetime.now()
    solar_year, solar_month, solar_day = now.year, now.month, now.day
    hour_input = now.hour
    minute_input = now.minute
    lng_input = 120.0
    province = ""
    city_name = ""
    district = ""
    location_str = "即时起盘"
    time_diff = 0
    true_hour = hour_input
    true_minute = minute_input
    use_direct = False
    gender = "男"
    current_year = now.year
    st.info(f"即时起盘：{now.strftime('%Y年%m月%d日 %H:%M')}（北京时间）")
    btn_paipan = True

if btn_paipan:
    if use_direct:
        nian_gan_idx = TIAN_GAN_CN.index(nian_gan)
        nian_zhi_idx = DI_ZHI_CN.index(nian_zhi)
        yue_gan_idx = TIAN_GAN_CN.index(yue_gan)
        yue_zhi_idx = DI_ZHI_CN.index(yue_zhi)
        ri_gan_idx = TIAN_GAN_CN.index(ri_gan)
        ri_zhi_idx = DI_ZHI_CN.index(ri_zhi)
        shi_gan_idx = TIAN_GAN_CN.index(shi_gan)
        shi_zhi_idx = DI_ZHI_CN.index(shi_zhi)
        nian_yy = GAN_YIN_YANG[nian_gan_idx]
        yue_zhu_cn = yue_gan + yue_zhi
        start_age = 1
        solar_year = 2000
    else:
        year_val = solar_year
        month_val = solar_month
        day_val = solar_day

        year_g = (year_val - 4) % 10
        year_z = (year_val - 4) % 12
        if month_val < 2 or (month_val == 2 and day_val < 4):
            year_g = (year_val - 5) % 10
            year_z = (year_val - 5) % 12

        nian_gan_idx = year_g
        nian_zhi_idx = year_z
        nian_yy = GAN_YIN_YANG[nian_gan_idx]

        yue_zhi_idx = 11
        for jm, jd, zhi_idx in [
            (1,6,1),(2,4,2),(3,6,3),(4,5,4),
            (5,6,5),(6,6,6),(7,7,7),(8,8,8),
            (9,8,9),(10,8,10),(11,7,11),(12,7,0),
        ]:
            if month_val < jm or (month_val == jm and day_val < jd):
                break
            yue_zhi_idx = zhi_idx
        yin_gan = WU_HU[TIAN_GAN_PY[nian_gan_idx]]
        yue_gan_idx = (yin_gan + (yue_zhi_idx - 2) % 12) % 10
        yue_zhu_cn = TIAN_GAN_CN[yue_gan_idx] + DI_ZHI_CN[yue_zhi_idx]

        target = date(year_val, month_val, day_val)
        ref = date(2006, 10, 9)
        days = (target - ref).days
        ri_gan_idx = (7 + days) % 10
        ri_zhi_idx = (7 + days) % 12

        shi_zhi_idx = (true_hour + 1) // 2 % 12
        zi_gan = WU_SHU[TIAN_GAN_PY[ri_gan_idx]]
        shi_gan_idx = (zi_gan + shi_zhi_idx) % 10

        solar_year = year_val
        shun_pai = (nian_yy == "阳" and gender == "男") or (nian_yy == "阴" and gender == "女")
        start_age = calc_start_age(year_val, month_val, day_val, shun_pai)

    gans = [TIAN_GAN_CN[nian_gan_idx], TIAN_GAN_CN[yue_gan_idx], TIAN_GAN_CN[ri_gan_idx], TIAN_GAN_CN[shi_gan_idx]]
    zhis = [DI_ZHI_CN[nian_zhi_idx], DI_ZHI_CN[yue_zhi_idx], DI_ZHI_CN[ri_zhi_idx], DI_ZHI_CN[shi_zhi_idx]]
    gan_idx = [nian_gan_idx, yue_gan_idx, ri_gan_idx, shi_gan_idx]
    zhi_idx = [nian_zhi_idx, yue_zhi_idx, ri_zhi_idx, shi_zhi_idx]
    shishen = [get_shi_shen(ri_gan_idx, g) for g in gan_idx]

    geju = get_ge_ju(ri_gan_idx, zhis[2], yue_gan_idx, zhis[1], shi_gan_idx, zhis[3], zhis[0], nian_gan_idx, gans, zhis)

    shun_pai = (nian_yy == "阳" and gender == "男") or (nian_yy == "阴" and gender == "女")
    dayun = get_dayun(yue_zhu_cn, shun_pai, start_age)

    ln_name, ln_gan_idx, ln_zhi_idx = get_liunian(current_year)
    ln_shi_shen = get_shi_shen(ri_gan_idx, ln_gan_idx)
    ln_wx = GAN_WU_XING[ln_gan_idx] + ZHI_WU_XING[ln_zhi_idx]

    current_dayun = None
    for age, yun in dayun:
        if current_year >= solar_year + age and current_year < solar_year + age + 10:
            current_dayun = yun
            break

    st.divider()
    st.subheader("排盘结果")

    st.markdown(f"""
    <div style="text-align:center; font-size:28px; line-height:2;">
        <p><b>年柱</b>　　{gans[0]}{zhis[0]}</p>
        <p><b>月柱</b>　　{gans[1]}{zhis[1]}</p>
        <p><b>日柱</b>　　{gans[2]}{zhis[2]}</p>
        <p><b>时柱</b>　　{gans[3]}{zhis[3]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='text-align:center; font-size:22px;'><b>格局：{geju}</b></p>", unsafe_allow_html=True)

    st.divider()
    st.subheader("详细信息")

    html_table = """
    <style>
    .detail-table { width:100%; border-collapse:collapse; font-size:14px; }
    .detail-table th, .detail-table td { text-align:center; padding:6px 4px; border:1px solid #ddd; }
    .detail-table th { background-color:#f5f5f5; }
    .label-col { background-color:#fafafa; font-weight:bold; }
    </style>
    <table class="detail-table">
    <tr><th class="label-col"></th><th>年柱</th><th>月柱</th><th>日柱</th><th>时柱</th></tr>
    """

    labels = ["天干", "地支", "藏干", "十神", "五行", "库", "空亡"]
    for label in labels:
        html_table += f"<tr><td class='label-col'>{label}</td>"
        for i in range(4):
            if label == "天干":
                val = gans[i]
            elif label == "地支":
                val = zhis[i]
            elif label == "藏干":
                val = "/".join(CANG_GAN[zhis[i]])
            elif label == "十神":
                val = shishen[i]
            elif label == "五行":
                val = GAN_WU_XING[gan_idx[i]] + ZHI_WU_XING[zhi_idx[i]]
            elif label == "库":
                val = ZHI_KU.get(zhis[i], "")
            elif label == "空亡":
                kong = KONG_WANG.get(gans[i] + zhis[i], ["", ""])
                val = "/".join(kong) if kong[0] else ""
            html_table += f"<td>{val}</td>"
        html_table += "</tr>"

    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

    st.divider()
    st.subheader("大运排盘")
    direction = "顺排" if shun_pai else "逆排"
    st.caption(f"年柱{nian_yy}年，{gender}命，{direction}，{start_age}岁起运，每柱十年")

    cols = st.columns(8)
    for i, (age, yun) in enumerate(dayun):
        with cols[i]:
            st.metric(f"{age}岁", yun)

    st.divider()
    st.subheader(f"流年 {current_year} 年")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("流年干支", f"{ln_name}（{ln_wx}）")
    with col2:
        st.metric("流年十神", ln_shi_shen)
    with col3:
        st.metric("当前大运", current_dayun if current_dayun else "未排到")

    st.info(f"**四柱**：{gans[0]}{zhis[0]} {gans[1]}{zhis[1]} {gans[2]}{zhis[2]} {gans[3]}{zhis[3]}　|　"
            f"**日主**：{gans[2]}　|　"
            f"**格局**：{geju}　|　"
            f"**流年**：{ln_name}（{ln_shi_shen}）")