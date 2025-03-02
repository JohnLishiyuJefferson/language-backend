import MeCab

# 创建 MeCab 解析器
mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic -r /opt/homebrew/etc/mecabrc')
# 输入日语句子
sentence = "帰る時間よ"

# 解析句子
result = mecab.parse(sentence)

lines = result.splitlines()
# 输出分词结果并提取每个词的原形
for line in lines:
    if line == 'EOS':
        break
    # 解析每一行，获取词的基本信息
    surface, feature = line.split('\t')
    features = feature.split(',')

    print(features)
    # 获取词的原形（基本形式）
    # base_form = features[6]  # 第7个字段是原形（如果有的话）

    # 输出词表面形式和原形
    # print(f"词：{surface} -> 原形：{base_form}")
