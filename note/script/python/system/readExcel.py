#!/usr/bin/python
# encoding:utf-8

import pandas as pd

# 读取 Excel 文件（假设文件名为 data.xlsx，sheet 名为 Sheet1）
file_path = 'E:\\xwechat_files\\qq-12352100_27af\\msg\\file\\2025-06\\2025年教材选用目录(2).xlsx'

# 读取 Excel 文件，不识别表头
df = pd.read_excel(file_path, sheet_name='Sheet1', header=None)

# 筛选 A 列中包含 "软件" 的行（不区分大小写）
# filtered_df = df[df['A'].str.contains('软件', na=False)]
# 使用第0列（即 A 列）进行筛选
filtered_df = df[df[0].str.contains('软件', na=False)]

# 打印匹配的整行数据
# print(filtered_df)

# 将结果写入文本文件
output_file = 'output.txt'
filtered_df.to_string(output_file, index=False, header=True)