#  Запуск проекта 🚀

<h4>
1. Создайте файл .env в корневой директории 
проекта и установите переменные согласно .env.example:
</h4>

```requirements
PROJECT_NAME=
BASE_URL='http://127.0.0.1'

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

<h4>
2. Запустите docker compose:
</h4>

```commandline
docker compose up --build -d
```

<b>Готово!</b>
<b>Документация API:</b> <em>http://127.0.0.1/docs</em><br>

<br>

<h3>
Для запуска тестов выполните команду:
</h3>

```commandline
docker exec -it {PROJECT_NAME из .env}_app pytest -v
```