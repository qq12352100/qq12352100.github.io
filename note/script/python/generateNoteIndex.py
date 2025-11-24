#!/usr/bin/python
# encoding:utf-8
import os
'''
运行qq12352100项目下note中的generateNoteIndex.py，更新本文件在note中更新，把整个note拷贝到qq12352100项目中
'''
def getfiles():
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 获取上3层目录的路径
    for _ in range(2):
        current_directory = os.path.dirname(current_directory)
    html_tree =list_files(current_directory, url_prefix="note")
    print(html_tree)
    
    # 再往上找一层
    index_html_path = os.path.dirname(current_directory)+"\\index.html"
    print(current_directory)
    html_content = ""
    with open(index_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
    from bs4 import BeautifulSoup
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', class_='left_div')
    if div:
        div.clear()  # 清空原有内容
        # 插入新内容（假设 new_content 是字符串 HTML）
        div.append(BeautifulSoup(html_tree, 'html.parser'))
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    
    
def list_files(directory, url_prefix=''):
    """
    递归生成目录的HTML文件树，文件排在前面，文件夹排在后面，均按名称排序。
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"目录不存在: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"路径不是目录: {directory}")

    items = []  # 存放生成的HTML片段
    try:
        # 获取所有子项并分类
        files = []
        dirs = []
        skip_dirs = ["script"]  # 指定要跳过的目录
        
        for item_name in os.listdir(directory):
            # 跳过指定目录
            if item_name in skip_dirs:
                continue
            item_path = os.path.join(directory, item_name)
            if os.path.isdir(item_path):
                dirs.append(item_name)
            elif item_name.endswith(".txt"):
                files.append(item_name)

        # 文件夹和文件都按字母顺序排序
        dirs.sort()
        files.sort()

        # 添加文件
        for file_name in files:
            item_url = f"{url_prefix}/{file_name}".lstrip('/')
            items.append(f'  <li><a href="{item_url}" target="myFrame">{file_name}</a></li>')
            
        # 添加文件夹
        for dir_name in dirs:
            item_url = f"{url_prefix}/{dir_name}".lstrip('/')
            subtree = list_files(os.path.join(directory, dir_name), item_url)
            items.append(f'  <li class="folder" onclick="toggle_ul(this)">{dir_name}</li>{subtree}')


    except PermissionError:
        items.append('  <li class="error">[权限不足]</li>')

    # 生成最终HTML
    if items:
        return '<ul>\n' + '\n'.join(items) + '\n</ul>'
    else:
        return '<ul></ul>'
        
        
if __name__=="__main__":
    getfiles()