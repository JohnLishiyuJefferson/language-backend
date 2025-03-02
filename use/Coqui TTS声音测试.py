import pykakasi
from TTS.api import TTS

# 原始文本
text = "CCTVによると、探査車のレーダーが探知したのは、中・低緯度地域の地表から10～35メートルの深さにある多層の堆積（たいせき）物。層の傾斜などが地球上で海岸線が形成される際の地質学的な特徴と似ているという。abcabc　「祝融」は2021年5月に火星に着陸。過去の研究成果が高緯度地域に集中していたのに対して、人間の活動に適した低・中緯度地域を探査した。今回の研究により、火星にかつて居住可能な環境があったことが裏付けられたと報じている。abcabc　中国は昨年発表した2050年までの宇宙計画で「人類が居住可能な星を探す」という目標を掲げる。CCTVは「大量の水が地下に氷として閉じ込められている可能性があり、将来の火星基地の建設費も大幅に削減されるだろう」としている。"

# 将汉字转换为假名
kks = pykakasi.kakasi()
result = kks.convert(text)
converted_text = "".join([item['hira'] for item in result])
print("转换后的文本：", converted_text)
# 输出可能为全假名的字符串，比如： "こんにちは、これはにほんごのてすとです。"

# 初始化 TTS 模型（确保选择支持日语的模型）
tts = TTS(model_name="tts_models/ja/kokoro/tacotron2-DDC").to("cpu")
# 生成语音文件（或直接播放）
tts.tts_to_file(text=converted_text, file_path="output.wav")
print("语音已生成，文件名：output.wav")
