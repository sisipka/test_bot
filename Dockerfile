FROM python:alpine

# Установим директорию для работы
WORKDIR /telegram_bot

# Копируем зависимости
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

# Копируем проект

COPY ./bot.py .
RUN chmod -R 777 ./bot.py

# run app
CMD ["python", "bot.py"]