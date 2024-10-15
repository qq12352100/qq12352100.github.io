#!/usr/bin/python
# encoding:utf-8
import os
import chardet

#标记递归文件深度
i=0

def getfiles():
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 获取上两层目录的路径
    parent_directory = os.path.dirname(os.path.dirname(current_directory))
    # 遍历当前文件夹中的所有文件和子文件夹
    recursive_files(parent_directory,i)

#递归文件夹
def recursive_files(file_directory, i):
    for filename in os.listdir(file_directory):
        filepath = os.path.join(file_directory, filename)
        # 判断文件类型
        if os.path.isdir(filepath):
            print("文件夹"+str(i)+":", filename)
            recursive_files(filepath,i+1)
        elif os.path.isfile(filepath):
            print("文件"+str(i)+":", filename)
            operation_file(filepath, filename, i)#操作单个文件
        else:
            print("未知类型:", filename)

#操作单个文件
def operation_file(filepath, filename, i):
    if filename.endswith(".txt") :#如果文件是txt结尾
        # modify_content(filepath, i)
        convert_to_utf8(filepath,filepath)
        # 读取文件内容，并检测编码
        # with open(filepath, "rb") as file:
            # content = file.read()
            # result = chardet.detect(content)
        # print("未知类型:", result['encoding'])
    elif filename.endswith(".html") :#如果文件是html结尾
        if os.path.exists(filepath):
            os.remove(filepath)
            print(filepath+"文件删除成功")

#修改文件内容
# "r"：只读模式。文件必须存在，否则会引发异常。
# "w"：写入模式。如果文件存在，则会被覆盖；如果文件不存在，则会创建新文件。
# "a"：追加模式。如果文件存在，则新内容将被追加到文件末尾；如果文件不存在，则会创建新文件。
# "b"：二进制模式。在文本模式下，Python会将文件内容解释为文本；而在二进制模式下，文件内容会以字节的形式读取或写入。
# "t"：文本模式（默认）。如果省略了此参数，则文件将以文本模式打开。
# 此外，还可以结合使用这些模式。例如，"rb" 表示以只读的二进制模式打开文件，"w+" 表示以读写模式打开文件，如果文件不存在则创建，如果文件存在则覆盖
def modify_content(file_path, i):
    # 读取文件
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    strend = ""
    for k in range(i):strend = strend+"../"
    # 在头部增加内容
    additional_content = "<!DOCTYPE html><html><head><script>fetch('"+strend+"common_head.html').then(response=>response.text()).then(html=>{document.head.innerHTML+=html;});</script></head><body><p>\n"
    content = additional_content + content +"\n</p></body></html>"
    # 写回到文件并修改后缀---源文件保留
    with open(file_path.replace(".txt", ".html"), "w", encoding="utf-8") as file:
        file.write(content)
#将其他编码的文本文件转换为UTF-8格式
def convert_to_utf8(input_file, output_file):
    # 检测原始文件的编码
    with open(input_file, 'rb') as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
    # 读取原始文件并以原始编码解码
    with open(input_file, 'r', encoding=detected_encoding) as f:
        content = f.read()
    # 将内容以UTF-8编码写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__=="__main__":
    getfiles()
