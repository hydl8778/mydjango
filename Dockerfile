# 使用 Python 3.12 作为基础镜像（和你的本地版本一致）
FROM python:3.12-slim

# 设置环境变量，防止 Python 输出缓冲，并设置时区
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /app

# 先拷贝依赖文件并安装（利用 Docker 缓存，加快后续构建）
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

# 拷贝项目的所有代码到容器中
COPY . /app/

# 暴露 8080 端口（腾讯云云托管默认监听这个端口）
EXPOSE 8080

# 启动命令：收集静态文件 -> 执行数据库迁移 -> 使用 gunicorn 启动 Django
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn thedjango.wsgi:application --bind 0.0.0.0:8080"]