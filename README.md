## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/ViktorovGO/aezakmi_test.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd aezakmi_test
    ```
3. Настройка переменных окружения

    Для запуска проекта на вашей локальной машине вам нужно будет настроить переменные окружения. Для этого следуйте этим шагам:

    - Скопируйте файл `.env.template` в `.env`:
    ```bash
    cp .env.template .env
    ```
    - Откройте файл .env и укажите нужные значения для переменных окружения. Пример:
    ```
    DB_NAME=my_database_name
    DB_USER=my_database_user
    DB_PASS=my_secure_password
    DB_HOST=localhost
    DB_PORT=5432
    APP_PORT=8000
    DEBUG=True
    ```

4. Запустите docker-compose
    ```bash
    docker-compose up -d
    ```
## Тесты
```bash
docker exec -it fastapi_container poetry run pytest
```

## Использование

1. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/docs, чтобы получить доступ к Swagger UI.

