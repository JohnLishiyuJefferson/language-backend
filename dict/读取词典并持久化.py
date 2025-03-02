import re
from typing import List

from dict.字典实体类 import WordEntry
from dict.数据库工具 import insert_word_entries


def extract_and_remove(line: str):
    """
    从字符串中提取第一个被【】包裹的内容，然后将【】及其内容从字符串中删除。
    返回提取到的内容（不含括号）和处理后的字符串。
    """
    # 使用正则表达式匹配第一个被【】包裹的部分
    pattern = r'【(.*?)】'
    match = re.search(pattern, line)

    if match:
        # 完整匹配的内容，包括【】, 以及内部的内容
        full_match = match.group(0)  # 例如 "【需要移除】"
        inner_content = match.group(1)  # 例如 "需要移除"
        # 替换第一次出现的匹配项为空字符串
        new_line = line.replace(full_match, "", 1)
        return inner_content, new_line
    else:
        # 没有匹配到则返回None和原字符串
        return None, line

def contains_brackets_ordered(line: str) -> bool:
    """
    判断文本是否同时包含左括号【和右括号】，并确保左括号在右括号之前。
    """
    left_index = line.find("【")
    right_index = line.find("】")
    return left_index != -1 and right_index != -1 and left_index < right_index

def read_dictionary(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    words = []
    word_entry_list: List[WordEntry] = []
    entry = []
    empty_line_count = 0

    for line in lines:
        line = line.strip()  # 去除首尾空白字符
        if line == "":  # 发现空行
            empty_line_count += 1
            if empty_line_count == 3:  # 每三个空行表示一个新词的开始
                if entry:  # 确保上一个词条不为空
                    contents = "\n".join(entry)
                    words.append(contents)  # 存储完整的词条
                    entry = []  # 清空以存储下一个词条
                    word_entry_list.append(transform_to_word_entry(contents))
                empty_line_count = 0  # 重置计数
        else:
            empty_line_count = 0  # 只要不是空行，就重置计数
            entry.append(line)  # 记录当前词条的内容

    # 处理最后一个词条
    if entry:
        words.append("\n".join(entry))

    return words, word_entry_list

def read_and_save():
    # 读取词典文件
    dictionary_file = "词典.txt"  # 你的词典文件路径
    word_entries, word_entry_list = read_dictionary(dictionary_file)

    insert_word_entries(word_entry_list)


def transform_to_word_entry(s) -> WordEntry:
    s = s.strip()

    # 1. 截取第一个单词：从开头取到第一个空格
    parts = s.split(" ", 1)
    if len(parts) < 2:
        return s, "", "", ""
    token1 = parts[0]
    s = parts[1].strip()

    # 2. 截取第二个单词：遇到空格或【时停止
    # 查找空格和【的位置
    idx_bracket = s.find("【")
    idx_space = s.find(" ")
    if idx_bracket == -1 and idx_space == -1:
        token2 = s
        s = ""
    else:
        if idx_bracket == -1:
            pos = idx_space
        elif idx_space == -1:
            pos = idx_bracket
        else:
            pos = min(idx_bracket, idx_space)
        token2 = s[:pos]
        s = s[pos:].strip()
    token2 = token2.replace("·", "")
    # 3. 如果存在【，则提取第三个单词：从【开始，不包含【，遇到】停止
    token3 = ""
    idx_start = s.find("【")
    if idx_start != -1:
        # 如果【不在开头，则舍弃【之前的部分
        s = s[idx_start:]
        # 此时s以【开头，去掉它
        s = s[1:]
        idx_end = s.find("】")
        if idx_end != -1:
            token3 = s[:idx_end]
            s = s[idx_end + 1:].lstrip()
        else:
            # 如果没有找到】，则将剩余内容全部作为token3
            token3 = s
            s = ""
    token3 = token3.replace("▼", "").replace("▽", "")
    # 4. 剩下的作为第四个单词，不会包含 】
    token4 = s

    return WordEntry(None, token1, token2, token3 , token4)


