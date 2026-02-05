import dmPython as dm
'''
连接达梦数据库DM Database Server 64 V8 8.4
https://pypi.org/project/dmpython/
pip install dmPython
'''

def getconn():
    try:
        # 建立连接
        conn = dm.connect(user='SYSDBA', password='Sysdba@123', server='172.30.162.149', port=5236)

        # 创建游标
        cursor = conn.cursor()

        # 执行 SQL 查询
        cursor.execute("SELECT * FROM rewcs.system_users ")  
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # 示例：创建表、插入数据、查询
        cursor.execute("CREATE TABLE test_table (id INT, name VARCHAR(50));")
        cursor.execute("INSERT INTO test_table VALUES (1, 'Alice');")
        cursor.execute("INSERT INTO test_table VALUES (2, 'Bob');")
        conn.commit()  # 提交事务

        cursor.execute("SELECT * FROM test_table;")
        results = cursor.fetchall()
        for r in results:
            print(r)

    except Exception as e:
        print("数据库操作出错:", e)

    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    getconn()









