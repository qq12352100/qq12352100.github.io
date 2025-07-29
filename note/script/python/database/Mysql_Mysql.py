import pymysql
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from DBUtils.PooledDB import PooledDB

# 配置日志
LOG_FILENAME = 'data_migration.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 进度记录文件
PROGRESS_FILE = 'progress.txt'

# 源数据库配置
source_db_config = {
    'host': '172.20.127.102',
    'port': 3306,
    'user': 'bzjw',
    'password': 'bzjw@bzjw',
    'database': 'psn_insu_d_jm',
    'charset': 'utf8mb4'
}

# 目标数据库配置
target_db_config = {
    'host': '172.20.127.102',
    'port': 3306,
    'user': 'bzjw',
    'password': 'bzjw@bzjw',
    'database': 'psn_insu_d_jm_test',
    'charset': 'utf8mb4'
}

# 创建数据库连接池
source_pool = PooledDB(pymysql, 10, **source_db_config)
target_pool = PooledDB(pymysql, 10, **target_db_config)

# 清洗函数
def clean_value(value):
    if isinstance(value, str):
        return value.replace('\n', '').replace('\t', '')
    return value

# 获取上次处理的 offset
def get_last_offset():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

# 保存当前 offset
def save_offset(offset):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(offset))

# 单个线程处理一个 offset 范围的数据
def process_chunk(offset, batch_size, columns_info, varchar_types, insert_sql):
    try:
        # 从连接池获取连接
        source_conn = source_pool.connection()
        source_cursor = source_conn.cursor()

        target_conn = target_pool.connection()
        target_cursor = target_conn.cursor()

        # 查询数据
        source_cursor.execute(f"SELECT * FROM psn_insu_d_jm LIMIT {offset}, {batch_size}")
        rows = source_cursor.fetchall()

        if not rows:
            source_cursor.close()
            source_conn.close()
            target_cursor.close()
            target_conn.close()
            return 0

        # 清洗 VARCHAR 类型字段，其他字段保留原值
        cleaned_rows = []
        for row in rows:
            cleaned_row = [
                clean_value(val) if any(t in str(col[1]).lower() for t in varchar_types) else val
                for val, col in zip(row, columns_info)
            ]
            cleaned_rows.append(cleaned_row)

        # 批量插入
        target_cursor.executemany(insert_sql, cleaned_rows)
        target_conn.commit()

        # 关闭连接
        source_cursor.close()
        source_conn.close()
        target_cursor.close()
        target_conn.close()

        return len(rows)

    except Exception as e:
        logging.error(f"线程处理 offset={offset} 出错: {e}", exc_info=True)
        return -1

# 主函数
def main():
    # 连接源数据库获取字段信息
    source_conn = source_pool.connection()
    source_cursor = source_conn.cursor()

    # 获取字段信息
    source_cursor.execute("DESCRIBE psn_insu_d_jm")
    columns_info = source_cursor.fetchall()

    # 获取字段名用于插入语句
    columns = [col[0] for col in columns_info]

    if not columns:
        logging.error("表中没有字段，无法继续插入。")
        print("表中没有字段，无法继续插入。")
        return

    print(f"所有字段: {', '.join(columns)}")
    logging.info(f"所有字段: {', '.join(columns)}")

    # 构建插入语句
    insert_sql = f"INSERT INTO psn_insu_d_jm ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

    # 只清洗 VARCHAR 类型字段
    varchar_types = ['char', 'varchar', 'text', 'tinytext', 'mediumtext', 'longtext']

    # 分页参数
    batch_size = 50000  # 增大批处理大小
    num_threads = 8  # 增加线程数
    offset = get_last_offset()
    total_processed = 0

    print(f"开始处理数据，每次处理 {batch_size} 条（从 offset={offset} 开始）...")
    logging.info(f"开始处理数据，每次处理 {batch_size} 条（从 offset={offset} 开始）...")

    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        while True:
            # 预查当前 offset 是否有数据
            source_cursor.execute(f"SELECT 1 FROM psn_insu_d_jm LIMIT {offset}, 1")
            if not source_cursor.fetchone():
                break  # 没有更多数据

            # 提交线程任务
            futures.append(executor.submit(
                process_chunk, offset, batch_size, columns_info, varchar_types, insert_sql
            ))
            offset += batch_size

        # 等待所有线程完成
        for future in as_completed(futures):
            result = future.result()
            if result > 0:
                total_processed += result
                print(f"已处理 {total_processed} 条数据")
                logging.info(f"已处理 {total_processed} 条数据")
            elif result == 0:
                logging.info("该批次无数据")
            else:
                logging.warning("该批次处理失败")

    # 更新最终 offset（即最后一个处理的 offset + batch_size）
    save_offset(offset)

    source_cursor.close()
    source_conn.close()

    print("✅ 数据清洗并插入完成。")
    logging.info("✅ 数据清洗并插入完成。")

if __name__ == "__main__":
    main()