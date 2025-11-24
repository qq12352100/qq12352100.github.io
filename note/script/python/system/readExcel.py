#!/usr/bin/python
# encoding:utf-8

import pandas as pd
import os
import re

def mask_digits(text):
    """
    将输入文本中的所有数字替换为 '*'
    
    参数:
        text: 输入的字符串（或可转为字符串的值，如数字、NaN 等）
    
    返回:
        str: 数字被替换为 '*' 的字符串
    
    示例:
        mask_digits("张三12345") -> "张三*****"
        mask_digits("电话：13812345678") -> "电话：***********"
        mask_digits(20251231) -> "********"
    """
    s = str(text).strip()
    if s == 'nan':
        return s  # 或返回 '' 或 '****'，根据需求
    return re.sub(r'\d', '*', s)
    
# 将输入值转换为字符串，并将其最后一个字符替换为 '$'
def replace_last_char_with_dollar(s):
    s = str(s)
    if s == 'nan':
        return '$'
    return s[:-1] + '$' if len(s) > 0 else '$'
    
"""
对姓名进行脱敏：
- 2个字：张三 -> 张*
- 3个字：李小四 -> 李*四
- >=4个字：欧阳小北 -> 欧阳*北（中间全替为一个 *)
"""
def mask_name(s, mask_char='某'):
    name = str(s).strip()
    if name == 'nan' or not name:
        return mask_char  # 或返回空、原值等

    length = len(name)
    if length == 1:
        return name  # 单字不处理，或可返回 *
    elif length == 2:
        return name[0] + mask_char + name[1]
    elif length == 3:
        return name[0] + mask_char + name[2]
    else:  # length >= 4
        return name[0] + name[1] + mask_char + name[-1]  # 保留前两字首、末字，中间一个 *
        # 或更彻底：name[0] + mask_char * (length - 2) + name[-1]
        
#脱敏身份证号码（支持18位或15位）
def mask_id_card(s, method='middle'):
    """
    脱敏身份证号码（支持18位或15位）
    
    参数:
    - s: 身份证号（字符串或数字）
    - method: 
        'middle' -> 保留前6后4，中间替换为 *
        'date'   -> 保留出生年月日，隐藏地区和顺序码（常用展示方式）

    示例:
        method='middle':   110105199003078654 -> 110105********8654
        method='date':     110105199003078654 -> 110105****0307****
    """
    id_str = str(s).strip()
    
    # 处理空值或 NaN
    if id_str == 'nan' or not id_str:
        return id_str

    # 只处理 15 位或 18 位身份证
    if len(id_str) not in [18]:
        if len(id_str) > 18 :
            return id_str[:6] + '*' * 8 + id_str[14:]
        else:
            return id_str + '****' # 非法格式返回 **** 处理

    if method == 'middle':
        # 保留前6位和地区码 + 后4位
        return id_str[:6] + '*' * (len(id_str) - 10) + id_str[-4:]

    elif method == 'date':
        if len(id_str) == 18:
            # 格式：XXXXXXXXXXXXXXX***
            #       地区(6) + **** + 月日(4) + ****
            return id_str[:6] + '****' + id_str[10:14] + '****'
        elif len(id_str) == 15:
            # 15位身份证：无X，出生年为2位
            return id_str[:6] + '****' + id_str[8:12] + '****'

    else:
        return id_str  # 默认不处理
        
def pro_cb_btran_bankcheck():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'pro_cb_btran_bankcheck.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)
    df.iloc[1:, 34] = df.iloc[1:, 34].astype(str).apply(replace_last_char_with_dollar)
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    # df.iloc[1:, 28] = df.iloc[1:, 28].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    df.iloc[1:, 10] = df.iloc[1:, 10].astype(str).apply(mask_digits)
    df.iloc[1:, 11] = df.iloc[1:, 11].astype(str).apply(mask_digits)
    
    df.iloc[1:, 29] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)

        
def sub_ps_cloudsearch():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'sub_ps_cloudsearch.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    df.iloc[1:, 30] = df.iloc[1:, 30].astype(str).apply(replace_last_char_with_dollar)# apply_id
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    df.iloc[1:, 28] = df.iloc[1:, 28].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 4] = df.iloc[1:, 4] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 10] = df.iloc[1:, 10].astype(str).apply(mask_digits)
    # df.iloc[1:, 11] = df.iloc[1:, 11].astype(str).apply(mask_digits)
    
    df.iloc[1:, 23] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
        
def sub_ps_driver():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'sub_ps_driver.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    df.iloc[1:, 27] = df.iloc[1:, 30].astype(str).apply(replace_last_char_with_dollar)# apply_id
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    df.iloc[1:, 28] = df.iloc[1:, 28].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 4] = df.iloc[1:, 4] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 10] = df.iloc[1:, 10].astype(str).apply(mask_digits)
    # df.iloc[1:, 11] = df.iloc[1:, 11].astype(str).apply(mask_digits)
    
    df.iloc[1:, 23] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def sub_ps_simplecotenant():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'sub_ps_simplecotenant.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    df.iloc[1:, 5] = df.iloc[1:, 5].astype(str).apply(mask_digits)
    
    df.iloc[1:, 17] = df.iloc[1:, 17].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 10] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def trk_pt_cabooking():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_pt_cabooking.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 5] = df.iloc[1:, 5].astype(str).apply(mask_digits)
    
    df.iloc[1:, 44] = df.iloc[1:, 44].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 39] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def trk_pt_caleaving():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_pt_caleaving.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 5] = df.iloc[1:, 5].astype(str).apply(mask_digits)
    
    df.iloc[1:, 48] = df.iloc[1:, 48].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 43] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def trk_pt_hotel():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_pt_hotel.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    df.iloc[1:, 20] = df.iloc[1:, 20].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    df.iloc[1:, 18] = df.iloc[1:, 18].astype(str).apply(mask_digits)
    
    df.iloc[1:, 41] = df.iloc[1:, 41].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 36] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def trk_pt_immigration():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_pt_immigration.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 4] = df.iloc[1:, 4] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 18] = df.iloc[1:, 18].astype(str).apply(mask_digits)
    
    df.iloc[1:, 35] = df.iloc[1:, 35].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 30] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
    
def trk_pt_trainbooking():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_pt_trainbooking.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 18] = df.iloc[1:, 18].astype(str).apply(mask_digits)
    
    df.iloc[1:, 31] = df.iloc[1:, 31].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 26] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
def trk_vt_alltrack():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'trk_vt_alltrack.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 2] = df.iloc[1:, 2].astype(str).apply(mask_name)
    df.iloc[1:, 10] = df.iloc[1:, 10].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 3] = df.iloc[1:, 3] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    df.iloc[1:, 11] = df.iloc[1:, 11] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 18] = df.iloc[1:, 18].astype(str).apply(mask_digits)
    
    df.iloc[1:, 12] = df.iloc[1:, 12].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 5] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
def sub_ps_immigcert():
    folder = r'E:\A\langchao_kuake\推广演示数据\standard标准库-推广演示数据\未脱敏'
    file = 'sub_ps_immigcert.xlsx'
    df = pd.read_excel(os.path.join(folder, file),sheet_name=0,header=None)

    # 获取第一列从第二行开始的数据，加$
    df.iloc[1:, 0] = df.iloc[1:, 0].astype(str).apply(replace_last_char_with_dollar)# pid
    
    # 第二列 --名字
    df.iloc[1:, 1] = df.iloc[1:, 1].astype(str).apply(mask_name)
    
    # 第3列 --身份证
    df.iloc[1:, 2] = df.iloc[1:, 2] .astype(str).apply(lambda x: mask_id_card(x, method='middle'))
    
    # 地址
    # df.iloc[1:, 18] = df.iloc[1:, 18].astype(str).apply(mask_digits)
    
    df.iloc[1:, 24] = df.iloc[1:, 24].astype(str).apply(replace_last_char_with_dollar)# apply_id
    df.iloc[1:, 19] = "9a0a6252faf742e59f5124c417c7e803"  # 替换整列case_id
    
    # 保存脱敏后的文件
    df.to_excel(os.path.join(folder, '脱敏_' + file), index=False, header=False)
# ================= 调用函数 =================
if __name__ == "__main__":
    # pro_cb_btran_bankcheck()
    # sub_ps_cloudsearch()
    # sub_ps_driver()
    # sub_ps_simplecotenant()
    # trk_pt_cabooking()
    # trk_pt_caleaving()
    # trk_pt_hotel()
    # trk_pt_immigration()
    # trk_pt_trainbooking()
    # trk_vt_alltrack()
    sub_ps_immigcert()
    print(f"脱敏完成!")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    