# JSON Document Processing Application

## Описание

Это приложение предназначено для обработки JSON документов пользователя. Схема этих документов и их структура задаются пользователем и предоставляются разработчикам заранее.

### Основные компоненты

1. **CLI Приложение**
   - Генерация Pydantic моделей на основе описания JSON Schema.
   - Генерация кода контроллеров REST приложения для обработки JSON документов.

2. **REST Приложение**
   - Обработка JSON документов.
   - Интеграция с базой данных и обработка запросов.

3. **База данных**
   - Схема реляционной базы данных (одна таблица).

### ОПЦИОНАЛЬНО

- Приложение для применения миграций базы данных.
- Отправка сообщений в брокеры сообщений (например, Kafka).
- Файлы спецификаций для запуска в Kubernetes.
- Схемы архитектуры приложения.
- Генерация и обновление Swagger документации.

## Системные Требования

- **Язык программирования**: Python
- **База данных**: MariaDB или PostgreSQL
- **Pydantic**: Версия 1.10
- **FastAPI**: Версия 0.110.0
- **SQLAlchemy**: Версия 2.0.30
- **Alembic**: Версия 1.13.0

## Сценарий использования

1. **Создание схемы базы данных**

   ```sql
   CREATE TABLE apps (
     uuid UUID PRIMARY KEY,
     kind VARCHAR(32),
     name VARCHAR(128),
     version VARCHAR(64),
     description TEXT,
     state ENUM('NEW', 'INSTALLING', 'RUNNING') DEFAULT 'NEW',
     json JSONB
   );
В rest/models/base_db есть .sql файл для создание таблицы

2. **Генерация кода по заранее созданному документу JSON**
   Пример генерации pydantic моделей из файла engine.json в папку rest\models\engine\
   Все модели необходимо загружать в директорию models, в уже существующую или просто указать название папки, создается автоматически.

   ```bash
   python cli_gen_code/main.py gen-models -json-schema-dir="G:\Programms\PyCharmProjects\VKinternProjectfastapi\engine.json" -out-dir="G:\Programms\PyCharmProjects\VKinternProjectfastapi\rest\models\engine\" 
   
   
Пример генерации эндпоинтов для REST приложения, CLI создает эндпоинты всех файлов указанной папки, в примере \rest\models\engine\
Все роуты необходимо загружать в папку routes, в отдельню папку kind документа, в уже существующую или просто указать название папки, создается автоматически.
   
   ```bash
   python cli_gen_code/main.py gen-rest -models="G:\Programms\PyCharmProjects\VKinternProjectfastapi\rest\models\engine\" -rest-routes="G:\Programms\PyCharmProjects\VKinternProjectfastapi\rest\routes\engine\"
   
   
В корневой папке проекта есть файл generate_and_commit.sh для генерации моделей. Но его нужно отредактировать на нужный файл.
Также этот файл сделает создает новую версию программу на git под новым тегом.

3. **Миграция базы данных**
   
   alembic revision --autogenerate -m "Ваша описание"     
   alembic upgrade head

В корневой папке проекта есть файл migration_alembic.sh для миграций базы данных

4. **Запуск проекта**
   Приложение можно запустить через Dockerfile.
   docker-compose с запуском БД, kafka и тд, работает не очень корректно. Его стоит подправить

5. **REST API**
   Основные Эндпоинты:
      POST /{kind}/ - Создание нового документа типа {kind}.
      PUT /{kind}/{uuid}/configuration/ - Обновление словаря configuration.
      PUT /{kind}/{uuid}/settings/ - Обновление словаря settings.
      PUT /{kind}/{uuid}/state - Обновление состояния объекта.
      DELETE /{kind}/{uuid}/ - Удаление объекта.
      GET /{kind}/{uuid} - Получение объекта.
      GET /{kind}/{uuid}/state - Получение состояния объекта.
                                                

