# -------------------------------
# Этап 1: сборка Vue-приложения
# -------------------------------
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем манифест и устанавливаем зависимости
COPY package.json package-lock.json ./

# Устанавливаем зависимости
RUN npm ci --silent --no-audit --no-fund

# Копируем весь код и собираем production-бандл
COPY . .
RUN npm run build

# -------------------------------
# Этап 2: копирование в volume
# -------------------------------
FROM alpine:latest

# Создаем папку для копирования
RUN mkdir -p /static

# Копируем результат сборки
COPY --from=builder /app/dist /static

# Команда для копирования в volume
CMD ["sh", "-c", "cp -r /static/* /app/static/ && echo 'Frontend files copied successfully'"]