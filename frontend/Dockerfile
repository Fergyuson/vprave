FROM node:18-alpine

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm ci --silent --no-audit --no-fund

# Копируем код и собираем
COPY . .
RUN npm run build

# Создаем volume для копирования результата
VOLUME /app/dist

# Команда для копирования в volume
CMD ["sh", "-c", "cp -r /app/dist/* /static/ && echo 'Frontend built successfully'"]