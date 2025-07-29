FROM python:3.11-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard]

# Копируем код бэкенда
COPY . .

# Создаем папки для статики
RUN mkdir -p static/assets static/docs

# Пробрасываем порт
EXPOSE 4014

# PYTHONPATH для модулей
ENV PYTHONPATH=/app

# Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4014"]
