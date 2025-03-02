from openai import OpenAI

client = OpenAI(
        api_key="sk-r8nBDBNRVXWl9QH5iZTczx4YDOsm0u7CKgWcHkDUuurTeVJK",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system",
         "content": "你是一个擅长用学生感兴趣的方式教授英语课的老教师，你会把学生需要学习的每个单词都给出一个例句，而且句子内容都是关于学生感兴趣的话题，同时这句话必须符合情理。"},
        {"role": "user", "content": "给我生成一个包含单词president的英文例句让我用于学习，要求内容与曾经风靡一时的游戏红色警戒2关联，句子水平要求为小学生"}
    ],
    temperature=0.3,
)

print(completion.choices[0].message.content)