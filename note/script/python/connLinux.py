import paramiko
import time

def ssh_connect(host, port, username, password):
    """建立SSH连接"""
    ssh = paramiko.SSHClient()
    # 自动接受未知的主机密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 连接服务器
        ssh.connect(host, port, username, password, timeout=10)
        print(f"成功连接到 {host}:{port}")
        return ssh
    except Exception as e:
        print(f"连接失败: {str(e)}")
        return None

def execute_command(ssh, command, timeout=30):
    """执行命令并返回结果"""
    if not ssh:
        print("未建立SSH连接")
        return None
    
    try:
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
        
        # 等待命令执行完成
        time.sleep(1)
        
        # 读取输出
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error:
            print(f"命令执行错误: {error}")
            return None
        
        return output
    except Exception as e:
        print(f"执行命令出错: {str(e)}")
        return None

def main():
    # 配置连接信息
    host = "81.70.203.208"  # Linux服务器IP
    port = 22               # SSH默认端口
    username = "ubuntu"  # 用户名
    password = "lL2#oOk-Ec^%+!mY"  # 密码
    
    # 建立连接
    ssh = ssh_connect(host, port, username, password)
    if not ssh:
        return
    
    try:
        # 示例：执行多个命令
        commands = [
            "uname -a",          # 查看系统信息
            "ls -l /home",       # 查看home目录
            "df -h",             # 查看磁盘空间
            "cat /etc/os-release" # 查看操作系统版本
        ]
        
        for cmd in commands:
            print(f"\n执行命令: {cmd}")
            print("=" * 50)
            result = execute_command(ssh, cmd)
            if result:
                print(result)
            print("=" * 50)
            
    finally:
        # 关闭连接
        ssh.close()
        print("\nSSH连接已关闭")

if __name__ == "__main__":
    main()
