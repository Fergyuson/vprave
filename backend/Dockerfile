FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Системные зависимости
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard]

# Копируем весь код бэкенда (main.py, src/, etc)
COPY . .

# Пробрасываем порт из билд-арга
ARG BACKEND_PORT=4014
ENV BACKEND_PORT=${BACKEND_PORT}
EXPOSE ${BACKEND_PORT}

# PYTHONPATH, чтобы модули src.* импортировались
ENV PYTHONPATH=/app

# Запуск Uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT
