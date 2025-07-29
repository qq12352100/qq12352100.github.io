import os
import datetime
file_path = 'D://a.py'
# 自定义时间
custom_time = datetime.datetime(2022, 1, 1, 12, 0, 0)
# 转换为时间戳
timestamp = custom_time.timestamp()
# 修改文件时间
os.utime(file_path, (timestamp, timestamp))
print(f"文件时间已修改为：{custom_time}")

