import re

from dict.数据库工具 import connect_db

# 连接 MySQL 数据库
conn = connect_db()
cursor = conn.cursor()

# **1. 检查 parsed_explanation 字段是否存在**
cursor.execute("SHOW COLUMNS FROM word_entry LIKE 'parsed_explanation'")
result = cursor.fetchone()

# **2. 如果字段不存在，则新增该字段**
if not result:
    cursor.execute("ALTER TABLE word_entry ADD COLUMN parsed_explanation TEXT")
    conn.commit()
    print("已添加字段 parsed_explanation")

# **3. 处理 explanation 字段内容**
circle_number_pattern = re.compile(r"[\u2460-\u2473\u24EA-\u24FF]")  # 匹配 ①-⑳ 和 ⓪-⑩

# 查询需要处理的数据
cursor.execute("SELECT id, explanation FROM word_entry")
rows = cursor.fetchall()

# **4. 生成批量更新的数据**
update_data = [(circle_number_pattern.sub("", explanation), id)
               for id, explanation in rows]

# **5. 批量更新 parsed_explanation 字段**
if update_data:
    cursor.executemany("UPDATE word_entry SET parsed_explanation = %s WHERE id = %s", update_data)
    conn.commit()
    print(f"更新了 {len(update_data)} 条数据")

# 关闭连接
cursor.close()
conn.close()
