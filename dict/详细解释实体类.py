class Structure:
    def __init__(self, sentence: str, antonym: str, synonym: str, idiom: str, explanation: str, derivative: str):
        self.sentence = sentence
        self.antonym = antonym
        self.synonym = synonym
        self.idiom = idiom
        self.explanation = explanation
        self.derivative = derivative

    def __repr__(self):
        return f"WordEntry(explanation={self.explanation}, sentence={self.sentence}, antonym={self.antonym}, synonym={self.synonym}, idiom={self.idiom}, derivative={self.derivative})"

    def to_dict(self):
        """将对象转换为字典，以便 JSON 序列化"""
        return {
            "sentence": self.sentence,
            "antonym": self.antonym,
            "synonym": self.synonym,
            "idiom": self.idiom,
            "explanation": self.explanation,
            "derivative": self.derivative
        }