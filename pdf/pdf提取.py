import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    # 打开 PDF 文件
    doc = fitz.open(pdf_path)

    # 存储提取的文本
    text = ''

    # 遍历所有页面并提取文本
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # 加载页面
        text += page.get_text()  # 提取页面的文本

    return text


# 测试代码
pdf_path = 'example.pdf'  # 替换为你自己的 PDF 文件路径
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)
