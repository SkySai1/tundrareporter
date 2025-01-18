# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для Flask
EXPOSE ${CONTAINER_PORT:-5000}

# Указываем команду для запуска приложения с параметрами
CMD ["python", "run.py", "--host=0.0.0.0", "--port=${CONTAINER_PORT:-5000}"]