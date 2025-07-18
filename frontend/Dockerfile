# -------------------------------
# Этап 1: сборка Vue-приложения
# -------------------------------
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем манифест и устанавливаем зависимости
COPY package.json package-lock.json ./

# Очищаем кэш npm и переустанавливаем зависимости
RUN npm cache clean --force && \
    rm -rf node_modules package-lock.json && \
    npm install

# Копируем весь код и собираем production-бандл
COPY . .
RUN npm run build

# -------------------------------
# Этап 2: отдача статики через Nginx
# -------------------------------
FROM nginx:stable-alpine

# Очищаем дефолтную статику
RUN rm -rf /usr/share/nginx/html/*

# Копируем результат сборки
COPY --from=builder /app/dist /usr/share/nginx/html

# (Опционально) свой конфиг nginx:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]