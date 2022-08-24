![example workflow](https://github.com/margoloko/foodgram-project-react-1/actions/workflows/foodgram-workflow.yml/badge.svg)
# Проект «Продуктовый помощник»
Проект «Продуктовый помощник» создан для публикции рецептов.
Это сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
-- -
## Сайт доступен по адресу: foodgram.myddns.me
-- -
### Для запуска приложения в контейнерах:
- Установите Docker
- Клонируйте репозиторий
``` git clone https://github.com/margoloko/foodgram-project-react-1.git ```
- Создайте и заполните файл .env в папке infra
-- -
### Заполнение .env файла:
- SECRET_KEY
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
-- -
- Запустите docker-compose в директории infra_sp2/infra командой
``` docker-compose up -d --build ```
- Выполните миграции
``` docker-compose exec backend python manage.py migrate ```
- Создайте суперпользователя
``` docker-compose exec backend python manage.py createsuperuser ```
- Для сбора статики воспользуйтесь командой
``` docker-compose exec backend python manage.py collectstatic --no-input ```
- Для загрузки базы данных ингрединтов
``` docker-compose exec backend python manage.py load_data ```
-- -
### Для доступа в админ-зону:
http://localhost/admin
- Логин: adminadmin
- Пароль: 123admin345
-- -
### Технологии:
- Python
- Django Rest Framework
- Docker
- Nginx
- Postgres
-- -
### Автор:
Балахонова Марина
