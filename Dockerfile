FROM python:alpine

# Установим директорию для работы
WORKDIR /bot

# Копируем зависимости
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

# Копируем проект

COPY ./bot .
RUN chmod -R 777 ./main.py

# run app
CMD ["python", "main.py"]