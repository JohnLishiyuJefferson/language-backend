import mysql.connector

from dict.数据库工具 import connect_db

def split_dot():
    # 连接数据库
    conn = connect_db()
    cursor = conn.cursor()

    # 查找包含 `·` 的数据
    cursor.execute("SELECT id, hanzi, kana, explanation FROM word_entry WHERE hanzi LIKE '%·%'")
    rows = cursor.fetchall()

    # 处理数据
    new_entries = []
    for row in rows:
        id, hanzi, kana, explanation = row
        hanzi_parts = hanzi.split("·")  # 按 `·` 拆分
        for part in hanzi_parts:
            new_entries.append((part.strip(), kana, explanation))

    # 批量插入新数据
    if new_entries:
        cursor.executemany("INSERT INTO word_entry (hanzi, kana, explanation) VALUES (%s, %s, %s)", new_entries)

    # 删除原始数据
    cursor.execute("DELETE FROM word_entry WHERE hanzi LIKE '%·%'")

    # 提交更改
    conn.commit()

    print(f"已拆分 {len(rows)} 条数据，新增 {len(new_entries)} 条数据")

    # 关闭连接
    cursor.close()
    conn.close()
