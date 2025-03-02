from typing import List, Tuple

import MeCab

from use.呈现实体类 import Element
from dict.字典实体类 import WordEntry
from dict.数据库工具 import connect_db
# 创建 MeCab 解析器
mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic -r /opt/homebrew/etc/mecabrc')

def parse_sentence(sentence: str) -> Tuple[List[Element], List[str]]:
    sentence = sentence.replace("\n", "abc")
    # 解析句子
    common_result = mecab.parse(sentence)

    lines = common_result.splitlines()
    elements = []
    original_text_list = []
    base_form_set = set()
    # 输出分词结果并提取每个词的原形
    for line in lines:
        if line == 'EOS':
            break
        # 解析每一行，获取词的基本信息
        surface, feature = line.split('\t')
        features = feature.split(',')
        if surface == "abc":
            original_text_list.append("\t");
            continue;
        original_text_list.append(surface)
        # print(features)
        # 获取词的原形（基本形式）
        base_form = features[6]  # 第7个字段是原形（如果有的话）
        if base_form not in base_form_set:
            # 输出词表面形式和原形
            # print(f"词：{surface} -> 原形：{base_form}")
            elements.append(Element(surface, base_form, None, None, None))
            base_form_set.add(base_form)

    # 获取所有 element 的 base_form
    base_forms = [element.base_form for element in elements]
    connection = connect_db()
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(base_forms))  # 用于 SQL 查询的占位符
    common_query = f"SELECT common, kana, hanzi, explanation, structure FROM word_entry WHERE common IN ({placeholders})"
    # 执行查询，获取匹配的 hanzi 和 explanation
    cursor.execute(common_query, tuple(base_forms))
    common_result = cursor.fetchall()

    kana_query = f"SELECT common, kana, hanzi, explanation, structure FROM word_entry WHERE kana IN ({placeholders})"
    # 执行查询，获取匹配的 hanzi 和 explanation
    cursor.execute(kana_query, tuple(base_forms))
    kana_result = cursor.fetchall()

    # 创建一个字典，以 hanzi 为键，explanation 为值
    common_word_map = dict()
    for row in common_result:
        word_entry = WordEntry(id = None, common=row[0], kana=row[1], hanzi=row[2], explanation=row[3], structure=row[4])
        common_word_map[word_entry.common] = word_entry

    kana_word_map = dict()
    for row in kana_result:
        word_entry = WordEntry(id = None, common=row[0], kana=row[1], hanzi=row[2], explanation=row[3], structure=row[4])
        kana_word_map[word_entry.kana] = word_entry

    result_list = []
    for element in elements:
        word_entry = common_word_map.get(element.base_form)
        print("\n")
        if word_entry:
            element.explanation = word_entry.explanation
            element.structure = word_entry.structure
            element.kana = word_entry.kana
            print(element)
            result_list.append(element)
        else:
            word_entry = kana_word_map.get(element.base_form)
            if word_entry:
                element.explanation = word_entry.explanation
                element.structure = word_entry.structure
                element.kana = word_entry.kana
                print(element)
                result_list.append(element)

    cursor.close()
    connection.close()
    return result_list, original_text_list

def test():
    # 创建 MeCab 解析器
    mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic -r /opt/homebrew/etc/mecabrc')
    # 输入日语句子
    sentence = "今は底にゴミが積もって—"

    # 解析句子
    common_result = mecab.parse(sentence)

    lines = common_result.splitlines()
    elements = []

    # 输出分词结果并提取每个词的原形
    for line in lines:
        if line == 'EOS':
            break
        # 解析每一行，获取词的基本信息
        surface, feature = line.split('\t')
        features = feature.split(',')

        # print(features)
        # 获取词的原形（基本形式）
        base_form = features[6]  # 第7个字段是原形（如果有的话）

        # 输出词表面形式和原形
        # print(f"词：{surface} -> 原形：{base_form}")
        elements.append(Element(surface, base_form, None, None))

    # 获取所有 element 的 base_form
    base_forms = [element.base_form for element in elements]
    connection = connect_db()
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(base_forms))  # 用于 SQL 查询的占位符
    common_query = f"SELECT common, kana, hanzi, explanation FROM word_entry WHERE common IN ({placeholders})"
    # 执行查询，获取匹配的 hanzi 和 explanation
    cursor.execute(common_query, tuple(base_forms))
    common_result = cursor.fetchall()

    kana_query = f"SELECT common, kana, hanzi, explanation FROM word_entry WHERE kana IN ({placeholders})"
    # 执行查询，获取匹配的 hanzi 和 explanation
    cursor.execute(kana_query, tuple(base_forms))
    kana_result = cursor.fetchall()

    # 创建一个字典，以 hanzi 为键，explanation 为值
    common_word_map = dict()
    for row in common_result:
        word_entry = WordEntry(id = None, common=row[0], kana=row[1], hanzi=row[2], explanation=row[3])
        common_word_map[word_entry.common] = word_entry

    kana_word_map = dict()
    for row in kana_result:
        word_entry = WordEntry(id = None, common=row[0], kana=row[1], hanzi=row[2], explanation=row[3])
        kana_word_map[word_entry.kana] = word_entry

    for element in elements:
        word_entry = common_word_map.get(element.base_form)
        print("\n")
        if word_entry:
            element.explanation = word_entry.explanation
            element.kana = word_entry.kana
            print(element)
        else:
            word_entry = kana_word_map.get(element.base_form)
            if word_entry:
                element.explanation = word_entry.explanation
                element.kana = word_entry.kana
                print(element)

    cursor.close()
    connection.close()

# test()