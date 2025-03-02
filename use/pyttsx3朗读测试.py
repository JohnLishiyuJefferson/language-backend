import pyttsx3

engine = pyttsx3.init()  # 初始化引擎
text = "探査車" #     によると、探査車のレーダーが探知したのは、中・低緯度地域の地表から10～35メートルの深さにある多層の堆積（たいせき）物。層の傾斜などが地球上で海岸線が形成される際の地質学的な特徴と似ているという。abcabc　「祝融」は2021年5月に火星に着陸。過去の研究成果が高緯度地域に集中していたのに対して、人間の活動に適した低・中緯度地域を探査した。今回の研究により、火星にかつて居住可能な環境があったことが裏付けられたと報じている。abcabc　中国は昨年発表した2050年までの宇宙計画で「人類が居住可能な星を探す」という目標を掲げる。CCTVは「大量の水が地下に氷として閉じ込められている可能性があり、将来の火星基地の建設費も大幅に削減されるだろう」としている。"
engine = pyttsx3.init(driverName='nsss')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[127].id)  # 选择第一个语音
rate = engine.getProperty('rate')
print(f"当前语速: {rate}")

# 降低语速，例如设置为 150
engine.setProperty('rate', 150)
engine.say(text)         # 加入要朗读的文本
engine.runAndWait()      # 播放语音
print(engine.getProperty('volume'))

for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} ({voice.id})")