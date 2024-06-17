# Запуск локального сервера

❗Все команды выполняются из директории `./server`

## Заполните значения переменных

Создайте `.env` файл и наполните его своими данными, используя `env.example`.

По умолчанию в `env.example` указаны стандартные наcтройки для запуска.

Для отправки писем используется `smtp.gmail.com`.
В `SMTP_EMAIL` указывается почта с которой будет осуществляться отправка.
> [Политика безопасности Google](https://support.google.com/accounts/answer/6010255). С 30 мая 2022 г. компания Google больше не будет поддерживать использование сторонних приложений и устройств, требующих входа в учетную запись Google , используя только имя пользователя и пароль.

Для предоставления «разрешения» на отправку email с google необходимо:

1. Включить двухэтапную аутентификацию
    * Откройте страницу Аккаунт Google.
    * На панели навигации выберите **Безопасность**.
    * В разделе "Вход в Google" нажмите **Двухэтапная аутентификация** затем **Начать**.
    * Следуйте инструкциям на экране.

2. Создать пароль для приложения
    * Откройте страницу Аккаунт Google.
    * Нажмите **Безопасность**.
    * В разделе "Вход в Google" выберите пункт **Двухэтапная аутентификация**.
    * Внизу страницы нажмите **Пароли приложений**.
    * Укажите название, которое поможет вам запомнить, где будет использоваться пароль приложения.
    * Выберите **Создать**.
    * Введите пароль приложения, следуя инструкциям на экране. Пароль приложения – это 16-значный код, который генерируется на вашем устройстве.
    * Нажмите **Готово**.

Готовый пароль без пробелов укажите в `SMTP_PASSWORD`

### Запустите контейнеры Docker

* база данных (PostgreSQL)
* база данных для тестов (PostgreSQL)
* Redis
  
```bash
docker-compose -f ./backend-docker-compose.yaml --env-file ./.env up -d
```

### Настройте виртуальное окружение

> Убедитесь, что у вас [установлен Poetry](https://python-poetry.org/docs/#installation)

Для того чтобы чтобы виртуальное окружение находилось внутри проекта, используйте команду ниже перед загрузкой зависимостей.

```bash
poetry config virtualenvs.in-project true
```

Загрузите зависимости.

```bash
poetry install 
```

Запустите оболочку с активированным виртуальным окружением.

```bash
poetry shell
```

### Примените миграции

Примените миграции командой:

```bash
alembic upgrade head
```

### Запустите сервер

```bash
uvicorn src.main:app --reload
```

### Celery

Для запуска Celery воспользуйтесь командой:

```bash
celery -A src.celery_tasks worker --loglevel=info -B
```

### Тесты

Для запуска тестов воспользуйтесь командой:

```bash
pytest tests/
```