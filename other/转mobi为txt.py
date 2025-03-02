import subprocess

def mobi_to_txt(input_file, output_file):
    command = ["ebook-convert", input_file, output_file]
    subprocess.run(command)

# 示例调用
mobi_to_txt("/Users/C5389057/Downloads/新時代日漢辭典.mobi", "../dict/词典.txt")
