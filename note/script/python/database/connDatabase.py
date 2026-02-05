''' 连接Mysql'''        
# pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error
def mysql():
    try:
        # 创建连接
        connection = mysql.connector.connect(
            host='106.52.70.220',  # 数据库主机地址，例如 'localhost' 或 '127.0.0.1'
            user='root',  # 数据库用户名
            password='123456',  # 用户密码
            database='bkk'  # 要连接的数据库名称
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_Info}")
            cursor = connection.cursor()
            # 执行SQL查询
            cursor.execute("SELECT * from youtube;")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
            # 示例：插入数据
            query = "INSERT INTO youtube (hostname,videoId,title) VALUES (%s, %s, %s)"
            cursor.execute(query, ("value1", "value2", "value2"))
            connection.commit()  # 提交，以保存更改
            print("Record inserted successfully into your_table")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        # 关闭连接，释放资源
        if (connection.is_connected()):
            cursor.close()
            connection.close()
        print("MySQL connection is closed")
''' 连接Oracle'''        
# pip install cx_Oracle
import cx_Oracle
def oracle():
    # 指定Oracle客户端库目录
    cx_Oracle.init_oracle_client(lib_dir=r"D:\AAA\installAll\instantclient_12_2")
    # 定义数据库连接信息
    dsn = cx_Oracle.makedsn('172.20.123.219', '1521', 'ORCL')  # 构建DSN
    try:
        # 创建连接
        connection = cx_Oracle.connect('zfpt', 'zfpt1', dsn)
        if connection:
            print("Successfully connected to Oracle Database")
            # 创建游标
            cursor = connection.cursor()
            # 执行SQL查询
            cursor.execute("SELECT * FROM AA01 WHERE ROWNUM <= 5")
            # 获取查询结果
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            # 关闭游标
            cursor.close()
    except cx_Oracle.Error as error:
        print(f"Error occurred: {error}")
    finally:
        # 关闭连接
        if connection:
            connection.close()
            print("Oracle connection is closed.")

# mysql()
oracle()