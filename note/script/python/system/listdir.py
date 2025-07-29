import os
import sys

# 列出目录下所有文件名字
def list_directory(path, indent='--'):
    """
    递归遍历目录，打印文件和文件夹结构
    :param path: 要遍历的目录路径
    :param indent: 缩进字符串，用于显示层级关系
    """
    print(f"{indent}-- {os.path.basename(path)}/")

    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                list_directory(full_path, indent + '--')
            else:
                print(f"{indent}---- {item}")
        print(f"")
    except PermissionError:
        print(f"{indent}  [无权限访问]")

# 删除包含keyword的文件 simulate=False 是真删除
def delete_files_with_keyword(directory, keyword="王欣欣", simulate=False):
    """
    遍历目录，删除文件名中包含关键字的文件
    :param directory: 要扫描的根目录
    :param keyword: 要匹配的关键字
    :param simulate: 如果为 True，只显示将要删除的文件；否则真正删除
    """
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword in file:
                file_path = os.path.join(root, file)
                print(f"{'[模拟删除]' if simulate else '[正在删除]'} {file_path}")
                if not simulate:
                    try:
                        os.remove(file_path)
                        count += 1
                    except Exception as e:
                        print(f"❌ 删除失败: {file_path} - {e}")
    if not simulate:
        print(f"\n 已删除 {count} 个包含 '{keyword}' 的文件。")

# 创建文件目录
def create_dir(directory, cdir):
    for folder_name in cdir:
        folder_path = os.path.join(root_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"已创建文件夹：{folder_path}")
        else:
            print(f"文件夹已存在，跳过创建：{folder_path}")
            
            
if __name__ == "__main__":

    root_path = r"D:\logs"

    cdir = [
    "2024级大数据4班/二级目录",
    "2024级大数据5班",
    "2024级大数据6班",
    "2024级大数据7班"
    ]

    create_dir(root_path, cdir)
    # list_directory(root_path)
    # delete_files_with_keyword(root_path)


























