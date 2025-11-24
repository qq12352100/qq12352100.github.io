'''
pip install python-docx
'''
import subprocess
from docx import Document
from datetime import datetime
import os
from docx.shared import Pt  # 用于设置字体大小
from docx.oxml.ns import qn


kecheng='大数据集群搭建维护与数据处理'
cankaoziliao='《Hadoop系统搭建及项目实践》北京邮电大学出版社'

kecheng='大数据数据库NoSQL数据库原理'
cankaoziliao='《NoSQL数据库原理与应用案例教程》 航空工业出版社'

file_path = 'E:\A\滨科教务\教学资料/4.教案/'+kecheng+'-（第12周 4课时）.docx'

# subprocess.run(["explorer", "E:\A\滨科教务\教学资料/4.教案"], shell=True)                           # 使用 explorer 命令打开文件夹


#课题
keti = 'HBase基础与HDFS原理'

# 授课时间
shoukeshijian = '2025.11.26 5-8节'

#学情分析
xueqingfenxi='学生已经学习了MongoDB、Redis、Neo4j等多种NoSQL数据库，对非关系型数据库有了较为全面的认识。但在面对HBase这样的列式数据库时，需要重新建立数据模型认知。同时学生对Hadoop生态系统仅有概念性了解，对HDFS的具体工作机制理解不深，需要从原理层面进行系统讲解。'

#教学内容
jiaoxueneirong = '''
HBase发展历程与技术特性
HBase与Hadoop生态系统关系
HDFS基本架构与核心组件
HDFS分块机制与多副本策略
HDFS读写流程详细解析
HDFS高可用性与容错机制
'''

#知识目标
zhishimubiao='''
了解HBase的发展历程和主要特性
掌握HBase在Hadoop生态系统中的定位
理解HDFS的基本架构和工作原理
熟悉HDFS的分块和多副本机制
掌握HDFS的读写流程和数据一致性保证
'''

#能力目标
nenglimubiao='''
能够分析HBase与传统数据库的差异
具备理解分布式文件系统架构的能力
能够描述HDFS读写数据的完整流程
具备初步的HDFS故障分析能力
能够根据业务需求选择合适的数据存储方案
'''

# 素质目标
suzhimubiao='''
培养分布式系统思维模式
增强对大数据底层架构的理解深度
树立数据安全与可靠存储的意识
培养技术发展的历史观和前瞻性
'''

# 教学重点
jiaoxuezhongdian='''
HBase的列式存储特性与数据模型
HDFS的主从架构与组件功能
HDFS分块存储的原理与优势
数据副本的分布策略与一致性保证
HDFS读写流程的核心步骤
'''

# 教学难点
jiaoxuenandian='''
HBase列族设计与存储结构的理解
HDFS元数据管理机制
数据分块大小设置的权衡考量
多副本一致性维护机制
读写过程中的故障处理机制
'''

# 教学策略
jiaoxuecelv='采用"架构图解-流程分解-对比分析"的教学方法。通过HDFS架构图直观展示各组件关系，使用流程图详细分解数据读写过程，结合HBase与关系型数据库的对比突出技术特点。设置HDFS数据存储模拟任务，让学生在实操中理解分布式存储原理。'

# 思政案例
sizhenganli='以"自主可控的分布式存储技术"为主题，通过介绍HDFS在国内外大型互联网企业的广泛应用，以及其在数据安全、容灾备份方面的重要价值，引导学生认识核心技术自主可控的重要性，培养学生对国家信息基础设施建设的责任感和使命感。'

# 教学反思
jiaoxuefansi='HDFS架构讲解需要更多可视化支持，后续应准备更丰富的动画演示材料。学生对分布式存储概念接受程度不一，需要设计分层练习任务。HBase数据模型的理解是难点，需要增加实际案例帮助学生建立直观认识。技术原理与实操环节的时间分配需要进一步优化。'


#----------------------------------------------------------------------------------------
doc = Document('E:\A\滨科教务\教学资料/4.教案\教案模版.docx')

doc.paragraphs[1].text = '课程：'+kecheng+' 2025-2026学年第一学期 教师：卜凯凯'
paragraph = doc.paragraphs[1]
for run in paragraph.runs:
    run.bold = True

# 设置文档默认字体
style = doc.styles['Normal']
font = style.font

# 设置字体为仿宋_GB2312
font.name = '仿宋_GB2312'
font._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')

# 设置字体大小为小四号（12磅）
font.size = Pt(12)  # 小四号对应12磅

cell_content = doc.tables[0].rows[0].cells[1]
cell_content.text = keti.strip()  # 课题

cell_content = doc.tables[0].rows[1].cells[4]
cell_content.text = shoukeshijian.strip()  # 授课时间

cell_content = doc.tables[0].rows[2].cells[1]
cell_content.text = xueqingfenxi.strip()  # 学情分析
cell_content = doc.tables[0].rows[3].cells[1]
cell_content.text = jiaoxueneirong.strip()  # 教学内容

cell_content = doc.tables[0].rows[4].cells[2]
cell_content.text = zhishimubiao.strip()  # 知识目标
cell_content = doc.tables[0].rows[5].cells[2]
cell_content.text = nenglimubiao.strip()  # 能力目标
cell_content = doc.tables[0].rows[6].cells[2]
cell_content.text = suzhimubiao.strip()  # 素质目标

cell_content = doc.tables[0].rows[7].cells[1]
cell_content.text = jiaoxuezhongdian.strip()  # 教学重点
cell_content = doc.tables[0].rows[8].cells[1]
cell_content.text = jiaoxuenandian.strip()  # 教学难点
cell_content = doc.tables[0].rows[9].cells[1]
cell_content.text = jiaoxuecelv.strip()  # 教学策略
cell_content = doc.tables[0].rows[10].cells[1]
cell_content.text = sizhenganli.strip()  # 思政案例
cell_content = doc.tables[0].rows[11].cells[1]
cell_content.text = cankaoziliao.strip()  # 参考资料
cell_content = doc.tables[0].rows[12].cells[1]
cell_content.text = jiaoxuefansi.strip()  # 教学反思


        
# 保存修改
if os.path.exists(file_path):
    os.remove(file_path)
doc.save(file_path)











