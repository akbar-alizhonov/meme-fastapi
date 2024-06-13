# Meme-FastAPI

## Локальный запуск

### Установите все зависимости

```shell
pip3 install -r requirements.txt
```

### Скопируйте и измените значения переменных окружений под себя
```shell
cp .env.template .env
```

### Запустите Базу Данных
```shell
docker run --name db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres 
```

### Выполните команды
```shell
cd src/
fastapi dev meme/main.py
```

## Запуск с Docker
```shell
docker-compose up -d --build
```

## Запуск Тестов
### Выполните команды
```shell
cd tests
pytest
```