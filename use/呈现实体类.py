class Element:
    def __init__(self, word: str, base_form: str, explanation: str, kana: str, structure: str):
        self.word = word  # 词
        self.base_form = base_form  # 原形
        self.explanation = explanation  # 解释
        self.kana = kana
        self.structure = structure

    def __repr__(self):
        return f"Element(word={self.word}, base_form={self.base_form}, kana={self.kana}, explanation={self.explanation}, structure={self.structure})"

    def to_dict(self):
        return {
            "word": self.word,
            "base_form": self.base_form,
            "explanation": self.explanation,
            "kana": self.kana,
            "structure": self.structure,
        }