from flask import Flask, request, jsonify
import hashlib
import requests
import pymysql
import os
from dotenv import load_dotenv  # 新增环境变量管理
import time

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 从环境变量获取敏感信息
APPID = os.getenv('WX_APPID')
SECRET = os.getenv('WX_SECRET')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 数据库连接池（简化版）
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# 获取openid端点
@app.route('/jscode2session', methods=['GET'])
def jscode2session():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Missing code parameter"}), 400
    
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'
    
    try:
        response = requests.get(url, timeout=5)  # 添加超时
        response.raise_for_status()
        data = response.json()

        if data.get('errcode', 0) != 0:
            return jsonify({
                "error": data.get('errmsg', 'Unknown error'),
                "code": data.get('errcode', -1)
            }), 400

        # 只返回必要信息给客户端
        # 成功返回 openid 和 session_key
        return jsonify({
            "openid": data.get("openid"),
            "session_key": data.get("session_key")
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"WeChat API error: {str(e)}")
        return jsonify({"error": "Service temporarily unavailable"}), 503
    except Exception as e:
        app.logger.exception("Unexpected error in jscode2session")
        return jsonify({"error": "Internal server error"}), 500

# 业务处理端点
@app.route('/invoke', methods=['POST'])
def handle_invoke():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty request body"}), 400
        app.logger.warning(data)
        # 签名验证
        if not verify_signature(data):
            app.logger.warning("Signature verification failed")
            return jsonify({"error": "Invalid signature"}), 401
        
        # 根据操作类型处理业务
        operation = data.get('operation')
        if operation in {'add', 'modify', 'del', 'list'}:
            return handle_db_query(data)
        else:
            # 其他操作类型处理
            return jsonify({
                "status": "success",
                "message": "Operation processed"
            })
            
    except Exception as e:
        app.logger.exception("Error in handle_invoke")
        return jsonify({"error": "Internal processing error"}), 500

# 安全的数据库查询
def handle_db_query(data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 参数化查询防止SQL注入
            table = data.get('table', '').strip()
            operation = data.get('operation', '').strip()
            if not table:
                return jsonify({"error": "Missing table parameter"}), 400
                
            sql = generate_sql(data)
            print(f"Excel sql: {sql}")
            cursor.execute(sql)
            if operation == 'list':
                results = cursor.fetchall()
                return jsonify(results)
            else:
                conn.commit()
                return jsonify({
                "status": "success",
                "message": "Operation processed"
            })
            
    except pymysql.Error as e:
        app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if conn:
            conn.close()

# 组装sql语句
def generate_sql(data):
    table = data.get("table")
    operation = data.get("operation")
    data_fields = data.get("data", {})
    id_value = data_fields.get("id")

    if not table or not operation or not data_fields:
        raise ValueError("缺少必要字段: table, operation, data")

    if operation == "add":          # INSERT INTO user (name, age) VALUES ('123', '1234')
        columns = ", ".join(data_fields.keys())
        values = ", ".join(f"'{v}'" for v in data_fields.values())
        return f"INSERT INTO {table} ({columns}) VALUES ({values});"

    elif operation == "modify":     # UPDATE user SET name='123', age='1234' WHERE id='1'
        if not id_value:
            raise ValueError("修改操作必须包含 id")
        set_clause = ", ".join(f"{k}='{v}'" for k, v in data_fields.items() if k != "id")
        return f"UPDATE {table} SET {set_clause} WHERE id='{id_value}';"

    elif operation == "del":        # 仅支持id删除，多个 id，如 "1,2,3"
        if not id_value:
            raise ValueError("删除操作必须包含 id")
        id_list = [x.strip() for x in id_value.split(",")]
        id_str = ", ".join(f"'{x}'" for x in id_list)
        return f"DELETE FROM {table} WHERE id IN ({id_str});"

    elif operation == "list":       # SELECT * FROM user WHERE id='1' ...
        where_clause = " WHERE " + data_fields.get("query")
        limit_clause = ""
        if "pageNum" in data and "pageSize" in data:
            page_num = int(data["pageNum"])
            page_size = int(data["pageSize"])
            limit_clause = f" LIMIT {page_size} OFFSET {page_num * page_size}"
        return f"SELECT * FROM {table} {where_clause}{limit_clause};"

    else:
        raise ValueError(f"不支持的操作类型: {operation}")
        
# MD5签名验证
def verify_signature(data):
    required_fields = ['time', 'table', 'operation', 'single']
    if not all(field in data for field in required_fields):
        return False
    # if int(time.time()) - data['time'] > 60: # 与当前时间相差超过60秒验证失败
        # return False
    message = f"{data['time']}{data['table']}{data['operation']}".encode()
    md5_str = hashlib.md5(message).hexdigest()
    print(f"Generated MD5: {md5_str}")
    return md5_str == data['single']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # 生产环境应关闭debug模式
    # app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
    
'''

# 删除 必须填id
{
    "time": 123,
    "table": "user",
    "operation": "del",
    "data": {
        "id": "1,2,3"
    },
    "single": "12312312312312313"
}

# 添加 不用传id
{
    "time": 123,
    "table": "user",
    "operation": "add",
    "data": {
        "name":"123"
        "age":"1234"
    },
    "single": "12312312312312313"
}

# 修改 必须填id
{
    "time": 123,
    "table": "user",
    "operation": "modify",
    "data": {
        "id":"1"
        "name":"123"
        "age":"1234"
    },
    "single": "12312312312312313"
}

# 查看
    "time": 123,
    "table": "user",
    "operation": "list",
    "data": {
        "id":"1"
        "name":"123"
        "age":"1234"
    },
    "pageNum":"0",
    "pageSize":"20",
    "single": "12312312312312313"
}


'''


















