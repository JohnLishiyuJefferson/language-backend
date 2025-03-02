import re
import json
from dict.数据库工具 import connect_db
from dict.详细解释实体类 import Structure

# 按行分割字符串
def split_text_by_newline_number(text):
    return re.split(r"\n(?=\d)", text)

# 从一个用法的文本中构建出一个Structure
def get_single_use(text: str) -> Structure:
    # 1. 用换行符分割字符串，得到列表
    lines = text.split("\n")

    # 2. 新建 WordEntry 实例，并初始化所有属性为空字符串
    entry = Structure("", "", "", "", "", "")

    # 3. 如果列表不为空，第一个元素作为解释
    if lines:
        entry.explanation = lines[0].strip()  # 去除首尾空格

    # 4. 遍历列表，从第二个元素开始判断
    for line in lines[1:]:
        line = line.strip()  # 去除首尾空格
        if not line:
            continue  # 跳过空行

        # 根据开头的特殊字符，追加到对应的属性
        if line.startswith("▸"):
            entry.sentence += (line[1:].strip() + " ")
        elif line.startswith("⇎"):
            entry.antonym += (line[1:].strip() + " ")
        elif line.startswith("⇒"):
            entry.synonym += (line[1:].strip() + " ")
        elif line.startswith("●"):
            entry.idiom += (line[1:].strip() + " ")
        elif line.startswith("衍："):
            entry.derivative += (line[2:].strip() + " ")

    # 去除每个属性末尾可能的多余空格
    entry.sentence = entry.sentence.strip()
    entry.antonym = entry.antonym.strip()
    entry.synonym = entry.synonym.strip()
    entry.idiom = entry.idiom.strip()

    return entry

# 从一个完整的explanation中解析出structure_list
def get_structure_list(parsed_explanation: str):
    structure_list = []
    split_result = split_text_by_newline_number(parsed_explanation)
    for text in split_result:
        item: Structure = get_single_use(text)
        structure_list.append(item)
    return structure_list

def save_structure():
    # 连接 MySQL 数据库
    # 连接数据库
    conn = connect_db()
    cursor = conn.cursor()

    # 1. 检查 structure 字段是否存在，如果不存在则新增
    cursor.execute("SHOW COLUMNS FROM word_entry LIKE 'structure'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("ALTER TABLE word_entry ADD COLUMN structure TEXT")
        conn.commit()

    # 2. 查询所有数据
    cursor.execute("SELECT id, parsed_explanation FROM word_entry")
    rows = cursor.fetchall()

    # 3. 处理数据
    update_data = []
    for row in rows:
        word_id, parsed_explanation = row
        if not parsed_explanation:
            continue  # 如果 parsed_explanation 为空，则跳过

        try:
            # 将 JSON 转换为字符串数组
            structure_list = get_structure_list(parsed_explanation)
            # 序列化 Structure 对象数组
            structure_json = json.dumps([s.to_dict() for s in structure_list], ensure_ascii=False)
            # 记录更新数据
            update_data.append((structure_json, word_id))

        except json.JSONDecodeError:
            print(f"解析 JSON 失败，ID: {word_id}")

    # 4. 批量更新数据
    if update_data:
        cursor.executemany("UPDATE word_entry SET structure = %s WHERE id = %s", update_data)
        conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()




