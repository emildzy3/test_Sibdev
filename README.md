Тестовое задание для SibDev
=====================

За основу взят шаблон проекта - [GitHub](https://github.com/SibdevPro/practice2021-django-stub)

Текст задания - [ТЕСТОВОЕ ЗАДАНИЕ на позицию Junior Python разработчик](https://github.com/emildzy3/test_Sibdev/blob/main/%5B%D0%A2%D0%97%5D%20Junior%20Python%20%E2%80%94%20Sibdev.pdf)

В результате выполнения тестового задания был реализован сервис по фиксированию и анализу сделок. Данные берутся из типового `.csv` файла. Дополнительно реализованы:
1. Документирование с использованием Swagger;
2. Unit-тестирование приложения;
3. Многопоточный `WSGI` сервер.


## Запуск сервера для разработки(`localhost:8000`):
```
docker-compose build &&

docker-compose up
```

или
```
docker-compose build &&

docker-compose run --rm --service-ports server
```
При первом запуске, необходимо применить миграции:
```
docker exec -it ... python manage.py migrate
```

## Запуск сервера на nginx (`localhost:80`)

```
docker-compose -f docker-compose.prod.yml build &&
docker-compose -f docker-compose.prod.yml up
```

## Документация доступна по адресу:
```
.../swagger/
```

### Примечания

* При разработке можно убрать или добавить зависимости

    `docker-compose run server poetry remove req_name`
    `docker-compose run server poetry add req_name`
* Запуск тестов внутри контейнера:

    `python manage.py test`
