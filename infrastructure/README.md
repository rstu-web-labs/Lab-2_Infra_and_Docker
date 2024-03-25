# Что-то вроде отчета - документации.
~~Будет корректироваться, но пока что так :(~~

## Так,начнем сначала...

## 1. Клонируем репозиторий, Находящийся по данной ссылке:
<https://github.com/rstu-web-labs/Lab-2_Infra_and_Docker> - репозиторий 2 лабы

**Пояснение:**

Это делается так:
```
git clone https://github.com/rstu-web-labs/Lab-2_Infra_and_Docker.git
```

## 2. Создаем папку infrastructure, так чтобы структура вашего проекта была примерно такой: 
```
Lab-2_Infra_and_Docker
│   .env
│   .example.env
│   .flake8
│   .gitignore
│   LICENSE
│   lint
│   Makefile
│   poetry.lock
│   pyproject.toml
│   README.md
│   requirements.txt
│   Task.md
│
├───.github
│   └───workflows
│           cd.yaml
│
├───app
│   │   main.py
│   │   tasks.py
│   │   worker.py
│   │   __init__.py
│   │
│   ├───api
│   │   │   routers.py
│   │   │   __init__.py
│   │   │
│   │   ├───endpoints
│   │   │       cadastr.py
│   │   │       ping.py
│   │   │       __init__.py
│   │   │
│   │   └───schemas
│   │           cadastr.py
│   │           __init__.py
│   │
│   ├───core
│   │   │   db.py
│   │   │   settings.py
│   │   │   __init__.py
│   │   │
│   │   ├───constants
│   │   │       base.py
│   │   │       mime.py
│   │   │       regexes.py
│   │   │       __init__.py
│   │   │
│   │   └───schemas
│   │           cadastr.py
│   │           __init__.py
│   │
│   └───services
│       │   __init__.py
│       │
│       └───clients
│               base.py
│               cadastr_client.py
│               __init__.py
│
├───docs
│       service_part.md
│
└───infrastructure - Это папка которую вы создали
```

## 3. Теперь нам нужно создать файл с зависимостями *.env*

Для этого выполняем команду:

```
cp .env.example .env 
```

## 4. Теперь приступаем к созданию наших Dockerfile и docker-compose.local.yaml в дирректории infrastructure

Вот что хранится в нашем Dockerfile:

```
FROM python:latest
WORKDIR /
COPY ../app ./app
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```

* **FROM** - говорит,какой образ использовать для создания нашего собственного (В данном случае это **Python**), через двоеточие указывается версия, в данном случае это **latest**

* **WORKDIR** - указывает наш рабочий каталог, т.е. от куда будет выполняться наш проект (/ - означает, что выполнение с текущей дирректории)

* **COPY** - копирует первый аргумент, который находится на вашем компьютере, в контейнер. А вот второй аргумент указывает на его местонахождения в контейнере.

* **RUN pip install --no-cache-dir -r requirements.txt:** 

    Эта инструкция запускает команду pip install внутри контейнера для установки зависимостей Python, перечисленных в файле requirements.txt. Флаг --no-cache-dir указывает pip не использовать кэш, что полезно при создании образов Docker, чтобы уменьшить размер образа и убедиться в том, что зависимости устанавливаются с учетом текущих версий

Далее я вам просто покажу как выглядит мой docker-compose.local.yaml, если захотите разберетесь:

```
version: '3.8'

services:
  postgres:
    container_name: postgres
    image: postgres:latest
    ports:
     - "5432:${DB_POSTGRES_PORT}"
    restart: always
    env_file: ../.env
    environment:
      POSTGRES_PASSWORD: ${DB_POSTGRES_PASSWORD}
      POSTGRES_USER: ${DB_POSTGRES_USERNAME}
      POSTGRES_DB: ${DB_POSTGRES_NAME}
      ENVIRONMENT: ${ENVIRONMENT}
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis_db:
    container_name: redis_db
    image: redis:latest
    ports:
      - "${REDIS_PORT}:${REDIS_PORT}"
    restart: always
    env_file: ../.env
    environment:
      ENVIRONMENT: PROD
      REDIS_PASSWORD: ${REDIS_PASSWORD}
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/var/lib/redis/data

  celery:
    container_name: celery
    restart: always
    env_file: ../.env
    build:
      context: ..
      dockerfile: infrastructure/Dockerfile
    environment:
      DB_POSTGRES_HOST: ${DB_POSTGRES_HOST}
      REDIS_HOST: ${REDIS_HOST}
    command: celery -A app.worker.celery worker --loglevel=info
    depends_on:
      - postgres
      - redis_db
volumes:
  pg_data:
  redis-data:
```

Далее вы можете проверить работоспособность написанного вами кода.
Для этого в терминал нужно ввест следующее:
```
docker-compose --env-file .env -f infrastructure/docker-compose.local.yaml up --build
```

Чтобы проверить создались ли ваши контейннеры, пишем в терминал следующее

```
docker ps -a - так вы увидите все ваши созданные контейнеры
```

## 5. Теперь выгрузка нашего файла на Docker Hub

* Во первых, создайте аккаунт на Docker Hub
* Теперь для создания образа вам понадобиться написать в терминале следующую команду:
 ```
 docker build -t lastdaywithlesss/my_selary_image:latest -f ./infrastructure/Dockerfile .
 ``` 
 **lastdaywithlesss** - мой нейм на docker hub

 **my_selary_image** - как будет называться образ

 **-f** - насколько знаю, для указания полного пути до вайла с его названием (вот как раз и он **./infrastructure/Dockerfile**)

* Теперь вам нужно будет залогиниться через терминал, для этого пишем:
```
docker login
```
После чего вводим данные своего аккаунта

* Далее Пишем следующее:
```
docker tag lastdaywithlesss/my_selary_image:latest lastdaywithlesss/my_selary_image:latest
```
Это нужно для создания новой метки, но в данном случае я ее не меняю(оставляю latest)

* Загружаем образ на Docker Hub
```
docker push lastdaywithlesss/my_selary_image:latest
```

**lastdaywithlesss** - мой нейм на docker hub

###  Все вы выгрузили образ на Docker Hub!!!

## 6. Создание docker-compose.yaml

Лень обьяснять, да и сам не сказать что особо понял, но вот код(РАЗБЕРЕТЕСЬ).
Для запуска все та же команда, что и для docker-compose.local.yaml.
```
version: '3.8'

services:
  postgres:
    container_name: postgres
    image: postgres:latest
    restart: always
    env_file: ../.env
    environment:
      POSTGRES_PASSWORD: ${DB_POSTGRES_PASSWORD}
      POSTGRES_USER: ${DB_POSTGRES_USERNAME}
      POSTGRES_DB: ${DB_POSTGRES_NAME}
      ENVIRONMENT: ${ENVIRONMENT}
    volumes:
      - pg_data:/var/lib/postgresql/data
    expose:
      - ${DB_POSTGRES_HOST}

  redis_db:
    container_name: redis_db
    image: redis:latest
    restart: always
    env_file: ../.env
    environment:
      ENVIRONMENT: PROD
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/var/lib/redis/data
    expose:
      - ${REDIS_HOST}

  selery:
    container_name: selery
    restart: always
    command: celery -A app.worker.celery worker --loglevel=info
    env_file: ../.env
    image: lastdaywithlesss/my_selary_image:latest
    depends_on:
      - redis_db
      - postgres
      - application

  application:
    container_name: application
    restart: always
    command: sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4"
    image: lastdaywithlesss/my_selary_image:latest
    ports:
      - "80:8080"
    depends_on:
      - redis_db
      - postgres

volumes:
  pg_data:
  redis-data:

```

### Кстати да, подобную штуку ${REDIS_HOST} я беру из файла с зависимостям (.env). Можете заглянуть в него и тогда вам станет понятнее
