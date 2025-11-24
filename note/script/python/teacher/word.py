'''
pip install python-docx
'''
import subprocess
from docx import Document
from datetime import datetime
import os
from docx.shared import Pt  # 用于设置字体大小
from docx.oxml.ns import qn


# 获取当前日期（本地时间）
today = datetime.today()
# 格式化为 "年-月-日" 中文格式
formatted_date = today.strftime("%Y年%m月%d日")

file_path = 'E:\A\管控项目资料\日报周报\工程日报-'+formatted_date+'.docx'

subprocess.run(["explorer", "E:\A\管控项目资料\日报周报"], shell=True)                           # 使用 explorer 命令打开文件夹

doc = Document('E:\A\管控项目资料\日报周报\日报.docx')

# 今日日报 - 设置内容及格式
today_content = '''
1、完成重点人群组装文本预处理。
2、实现12345热线与网格数据的脱敏展示功能。
3、大数据向量模型代码适配解决，为后续“人找事”业务功能提供依据。
4、实现12345热线数据与网格数据增量抽取。
5、组装12345热线数据摸排文本向量，初步实现12345数据摸排。
6、根据建设方案梳理智能转办中心、分析预警中心、指挥调度中心展示数据。
7、继续整理并完善系统业务流程图及数据治理流程图。
8、实现情况摸排功能代码进度90%。
9、现项目总体进度45%。
'''
# 明日计划 - 设置内容及格式
tomorrow_content = '''
1、继续完善数据治理功能模块中文本预处理流程。
2、切换大数据提供的大数据的向量模型，并测试。
3、根据重点人群匹配检索12345向量库生成风险隐患。
'''


# 读取所有段落
# print("=== 段落内容 ===")
# for para in doc.paragraphs:
    # print(para.text)

# 读取所有表格
# print("\n=== 表格内容 ===")
# for table in doc.tables:
    # for row in table.rows:
        # row_data = [cell.text for cell in row.cells]
        # print(row_data)
        
        
doc.paragraphs[1].text = '编制时间：'+formatted_date
# 设置字体为宋体，大小为小四（12磅）
for run in doc.paragraphs[1].runs:
    run.font.name = '宋体'
    run.font.size = Pt(12)
    # 解决中文显示问题的额外设置
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 设置今日日报内容
cell_today = doc.tables[0].rows[2].cells[1]
cell_today.text = today_content.strip()  # 先设置文本内容

# 格式化今日日报单元格（宋体小四）
for para in cell_today.paragraphs:
    for run in para.runs:
        run.font.name = '宋体'  # 西文字体
        run.font.size = Pt(12)  # 小四对应12磅
        # 设置中文字体（解决宋体显示问题）
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 设置明日计划内容
cell_tomorrow = doc.tables[0].rows[4].cells[1]
cell_tomorrow.text = tomorrow_content.strip()  # 先设置文本内容

# 格式化明日计划单元格（宋体小四）
for para in cell_tomorrow.paragraphs:
    for run in para.runs:
        run.font.name = '宋体'
        run.font.size = Pt(12)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        
        
# 保存修改
if os.path.exists(file_path):
    os.remove(file_path)
doc.save(file_path)











