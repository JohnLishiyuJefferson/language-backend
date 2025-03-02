import mysql.connector
import re

from dict.数据库工具 import connect_db

def process_bracket():
    # 连接数据库
    conn = connect_db()
    cursor = conn.cursor()

    # 查找包含 '（' 和 '）' 的数据
    cursor.execute("SELECT id, hanzi, kana, explanation FROM word_entry2 WHERE hanzi LIKE '%（%' AND hanzi LIKE '%）%'")
    rows = cursor.fetchall()

    # 处理数据
    new_entries = []
    for row in rows:
        id, hanzi, kana, explanation = row

        # 去掉括号和括号中的内容，保留括号外的内容
        hanzi_no_parentheses = re.sub(r'（.*?）', '', hanzi)  # 去掉括号及其内容
        hanzi_with_empty_parentheses = re.sub(r'（.*?）', '()', hanzi)  # 去掉内容，但保留括号

        # 新增两条记录
        new_entries.append((hanzi_no_parentheses, kana, explanation))  # 一行：去掉括号和内容
        new_entries.append((hanzi_with_empty_parentheses, kana, explanation))  # 一行：只去掉括号中的内容

    # 批量插入新数据
    if new_entries:
        cursor.executemany("INSERT INTO word_entry2 (hanzi, kana, explanation) VALUES (%s, %s, %s)", new_entries)

    # 删除原始包含括号的记录
    cursor.execute("DELETE FROM word_entry2 WHERE hanzi LIKE '%（%' AND hanzi LIKE '%）%'")

    # 提交更改
    conn.commit()

    print(f"已处理 {len(rows)} 条数据，新增 {len(new_entries)} 条数据")

    # 关闭连接
    cursor.close()
    conn.close()
