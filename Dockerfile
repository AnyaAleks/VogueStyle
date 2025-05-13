# Используем официальный образ Python 3.11 с "slim" версией (минимальный размер)
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /bot

# Копируем файлы зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости с оптимизацией кэша
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта (исключая то, что в .dockerignore)
COPY ./bot .

ENV BOT_TOKEN="7715107679:AAFzZ7xjYsxbQwBzCkuHJ5lG2I96vO0PckY"

# Команда запуска сервера
# CMD ["python", "main.py"]