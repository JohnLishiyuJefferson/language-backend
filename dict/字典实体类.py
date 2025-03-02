class WordEntry:
    def __init__(self, id: int, common: str, kana: str, hanzi: str, explanation: str, structure: str):
        self.id = id              # 数字类型的 id
        self.common = common
        self.kana = kana          # 假名字符串
        self.hanzi = hanzi        # 汉字字符串
        self.explanation = explanation  # 解释字符串
        self.structure = structure

    def __str__(self):
        return f"ID: {self.id}, 最常见形态: {self.common}, 假名: {self.kana}, 汉字: {self.hanzi}, 解释: {self.explanation}, , 结构化解释: {self.structure}"