import subprocess

# 启动 CMD 并执行命令
process = subprocess.Popen(
    ["cmd.exe", "/c", "echo Hello World && dir"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate()

print("标准输出：\n", stdout)
print("错误输出：\n", stderr)