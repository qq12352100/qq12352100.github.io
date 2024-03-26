#!/usr/bin/python
# encoding:utf-8
import os
def getfiles():
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 获取上两层目录的路径
    parent_directory = os.path.dirname(os.path.dirname(current_directory))
    
    print(list_files(parent_directory))
    
def list_files(directory,indent='note'):
    # 初始化存储文件和文件夹的列表
    files = []
    directories = []
    # 遍历目录中的所有项目
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # 如果是文件，则添加到文件列表中
        if os.path.isfile(item_path):
            if item.endswith(".txt") :
                files.append(item)
        # 如果是文件夹，则递归调用本函数，并将结果添加到文件夹列表中
        elif os.path.isdir(item_path):
            directories.append(item)
    # 对文件和文件夹列表进行排序
    files.sort()
    directories.sort()
    html = '<ul>\n'
    # 输出文件和文件夹列表
    for file in files:
        print(os.path.join(directory, file))
        html += '<li><a href="{}" target="myFrame">{}</a></li>\n'.format(indent+"/"+file,file)
    for directory_name in directories:
        print(os.path.join(directory, directory_name))
        html += '<li>{}</li>\n'.format(directory_name)
        # 递归调用本函数，并将结果添加到当前层的HTML字符串中
        html += list_files(os.path.join(directory, directory_name),indent =indent+"/"+directory_name)
    html += '</ul>\n'
    return html
if __name__=="__main__":
    getfiles()