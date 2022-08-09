# Проект «Продуктовый помощник»
На сайте вы можете публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит вам создать список продуктов, которые нужно купить для приготовления выбранных блюд.

Доступен по адресу:

# Документация к API
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке: http://127.0.0.1/api/docs/

Так же документация доступна на сервере: http://foodgram.ddns.net/api/docs/

# Установка
На сервер переместите в корень папку nginx, docker-compose.yaml. Создайте .env с настройками для подключения к БД и с ключом джанго проекта.

DEBUG=on
SECRET_KEY=ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgre
POSTGRES_USER=postgre
POSTGRES_PASSWORD=postgre
DB_HOST=db
DB_PORT=5432
Запуск проекта выполняется командой docker-compose up --build -d

Далее необходимо выполнить следующий шаги

открываем терминал в контейнере web docker exec -it <container_id> bash
миграция python manage.py migrate
создаем необходимые таблицы python3 manage.py migrate --run-syncdb
заходим в оболочку джанго python3 manage.py shell
импортируем ContentType from django.contrib.contenttypes.models import ContentType
удаляем ContentType.objects.all().delete()
выходим из оболочки quit()
загружаем данные в базу данных python3 manage.py loaddata dump.json
создаем администратора python manage.py createsuperuser
заходим по адресу pretty-food.tk/admin/ и создаем flatpages
Built With
Python v:
Django v:
Django REST Framework v:
PostgreSQL v:
nginx v:

