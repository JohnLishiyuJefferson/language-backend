import mysql.connector
from typing import List

from dict.字典实体类 import WordEntry


# 连接 MySQL 数据库
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # 例如: "localhost" 或 "127.0.0.1"
        user="root",  # 例如: "root"
        password="1234",  # 例如: "password"
        database="dict"  # 例如: "dictionary"
    )


# 分批插入数据
def insert_word_entries(entries: List[WordEntry], batch_size=1000):
    conn = connect_db()
    cursor = conn.cursor()

    sql = "INSERT INTO word_entry (common, kana, hanzi, explanation) VALUES (%s, %s, %s, %s)"

    try:
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]  # 切分当前批次
            values = [(entry.common, entry.kana, entry.hanzi, entry.explanation) for entry in batch]

            cursor.executemany(sql, values)  # 批量执行当前批次
            conn.commit()
            print(f"成功插入 {len(values)} 条数据，共 {i + len(values)}/{len(entries)}")

    except mysql.connector.Error as err:
        print("插入失败:", err)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_all():
    # 连接数据库
    conn = connect_db()
    cursor = conn.cursor()

    # 替换倒三角
    cursor.execute("delete from word_entry where 1 = 1")
    conn.commit()