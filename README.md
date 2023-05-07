Тестовое задание для SibDev
=====================

За основу взят шаблон проекта - [GitHub]()

Текст задания - [ТЕСТОВОЕ ЗАДАНИЕ на позицию Junior Python разработчик]()

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
* Запуск тестов:

    `python manage.py test`
