import psycopg2
from psycopg2 import OperationalError, ProgrammingError
'''
pip install psycopg2-binary
'''
def create_connection(db_name, db_user, db_password, db_host, db_port):
    """创建与瀚高数据库的连接"""
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("数据库连接成功")
    except OperationalError as e:
        print(f"连接错误: {e}")
    return connection

def execute_query(connection, query, params=None):
    """执行SQL查询（INSERT, UPDATE, DELETE等）"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        print("查询执行成功")
    except ProgrammingError as e:
        print(f"查询错误: {e}")
        connection.rollback()
    finally:
        cursor.close()

def execute_read_query(connection, query, params=None):
    """执行查询并返回结果（SELECT等）"""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except ProgrammingError as e:
        print(f"查询错误: {e}")
        return None
    finally:
        cursor.close()

if __name__ == "__main__":
    # 数据库连接参数
    db_params = {
        "db_name": "你的数据库名",
        "db_user": "你的用户名",
        "db_password": "你的密码",
        "db_host": "数据库主机地址",
        "db_port": "5866"  # 瀚高数据库默认端口
    }
    
    # 创建连接
    conn = create_connection(**db_params)
    
    if conn:
        try:
            # 示例：创建表
            create_table_query = """
            CREATE TABLE IF NOT EXISTS example_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                value INT
            );
            """
            execute_query(conn, create_table_query)
            
            # 示例：插入数据
            insert_query = "INSERT INTO example_table (name, value) VALUES (%s, %s);"
            execute_query(conn, insert_query, ("测试数据", 100))
            
            # 示例：查询数据
            select_query = "SELECT * FROM example_table;"
            results = execute_read_query(conn, select_query)
            
            if results:
                print("查询结果:")
                for row in results:
                    print(row)
                    
        finally:
            # 关闭连接
            conn.close()
            print("数据库连接已关闭")
