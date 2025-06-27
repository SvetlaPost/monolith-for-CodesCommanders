FROM python:3.10-slim

LABEL maintainer="svetlanapostel"

# Уменьшает размер образа
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы (если нужно psycopg2 или другие бинарные пакеты)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем библиотеки
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Команда запуска через gunicorn
CMD ["gunicorn", "proj.wsgi:application", "--bind", "0.0.0.0:8000"]
