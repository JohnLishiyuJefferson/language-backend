from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
import os

# 配置 OpenAI API 相关参数
openai_api_key = "sk-r8nBDBNRVXWl9QH5iZTczx4YDOsm0u7CKgWcHkDUuurTeVJK"
openai_api_base = "https://api.moonshot.cn/v1"

# 初始化 LangChain 的 OpenAI LLM
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    openai_api_base=openai_api_base,
    model_name="moonshot-v1-8k",  # 确保这个模型在 moonshot.cn 也适用
    temperature=0.5
)

# 创建 LangChain 的 Prompt 模板
prompt_template = ChatPromptTemplate.from_messages([("system", "你是一个语言学习助手，擅长解释外语句子和解答相关疑问。"), ("user", "用户需要学习的外语句子：{sentence}\n\n用户的疑问：{question}")])

def ai_reply(sentence: str, question: str) -> str:
    """
    使用 OpenAI API 解释用户提供的外语句子，并回答用户的疑问。
    """
    messages = prompt_template.invoke({"sentence": sentence, "question": question})
    response = llm.invoke(messages)
    print(response)
    return response.content

# 示例输入
# user_sentence = "Je suis étudiant en informatique."
# user_question = "'étudiant' 这个词可以用来形容女生吗？"

# 获取 AI 生成的解释
# explanation = explain_sentence(user_sentence, user_question)
# print("AI 解释：", explanation)
