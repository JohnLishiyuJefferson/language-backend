# 选择基础镜像（使用 Python 3.11 的轻量 Linux 版本）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . .

# 安装 Python 依赖（最好带版本号）
RUN pip install --no-cache-dir -r requirements.txt

# 指定启动命令（假设你的主程序是 app.py）
CMD ["python", "server.py"]
