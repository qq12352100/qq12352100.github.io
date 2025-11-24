from kazoo.client import KazooClient
import time

# 创建客户端实例（连接到本地 ZooKeeper，默认端口 2181）
zk = KazooClient(hosts='127.0.0.1:2181')

# 启动连接
zk.start()

# 确保根路径存在（可选）
if zk.exists("/my_app"):
    print("Path /my_app exists")
else:
    zk.create("/my_app", b"initial data")

# 读取数据
data, stat = zk.get("/my_app")
print("Data:", data.decode("utf-8"))
print("Version:", stat.version)

# 写入数据
zk.set("/my_app", b"updated data")

# 创建子节点（临时/持久）
zk.create("/my_app/child1", b"child data", ephemeral=False)

# 列出子节点
children = zk.get_children("/my_app")
print("Children:", children)


def my_listener(event):
    print(f"Event: {event}")

# 设置监听
zk.get("/my_app", watch=my_listener)

# 或使用装饰器方式（推荐）
@zk.DataWatch("/my_app")
def watch_app_node(data, stat):
    if data:
        print(f"App node updated: {data.decode('utf-8')}, version: {stat.version}")
    else:
        print("App node deleted!")
        
        
time.sleep(20)
# 关闭连接
zk.stop()
zk.close()