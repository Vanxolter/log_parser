Nginx logs parser
========


About
-----


Author: Maksim Laurou <Lavrov.python@gmail.com>

Source link: git@github.com:Vanxolter/log_parser.git

------------------

**ЗАПУСК ПРОЕКТА ВРУЧНУЮ**

1) Клонируем репозиторий: ``` git@github.com:Vanxolter/log_parser.git ```

2) Создаем виртуальное окружение: ``` virtualenv -p python3 --prompt=logs- venv/ ```

3) Устанавливаем необходимые библиотеки: ``` pip install -r requirements.txt ```

4) Создаем базу данных:
	*  ``` sudo su postgres ```
	* ``` psql ```
	* ``` CREATE USER nginxparser WITH PASSWORD 'nginxparser' CREATEDB; ```
	* ``` CREATE DATABASE nginxparser OWNER nginxparser; ```
	* ``` GRANT ALL PRIVILEGES ON DATABASE nginxparser TO nginxparser; ```

5) Поднимаем миграции: ``` python manage.py migrate ```<br/>

6) ЗАМЕНИТЬ в docker/env/.env.dev ПЕРЕМЕННУЮ POSTGRES_HOST с postgres на localhost 

7) Запускаем проект: ``` python manage.py runserver ```

------------------

**ЗАПУСК DEV КОНТЕЙНЕРА**

1) Сборка билда``` sudo docker compose -f docker-compose.dev.yml build ```
2) Запуск контейнера ``` sudo docker compose -f docker-compose.dev.yml up ```
3) Вход в консоль контейнера ``` docker exec -it django sh ```
4) Создаем юзера ```python manage.py createsuperuser```

------------------

**ПАРСИНГ ДАННЫХ ИЗ ФАЙЛА**
1) ``` python manage.py import_log <путь к файлу> ```
   (_путь указывать относительно рута приложения например_ - ```python manage.py import_log ../logs_for_parsing/nginx_json_logs.txt```)
------------------


**ПРОЕГОНКА ТЕСТОВ**

``` pytest ```


------------------