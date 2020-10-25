# PWS-15_e7_mongo_redis

## API Доступен на виртуальном сервере в облаке Яндекс (до 2020.12.08) по адресам:
```
https://sf.rtru.tk/advs [GET, POST]
https://sf.rtru.tk/adv/<adv_id> [GET, PATCH, DELETE]
https://sf.rtru.tk/tags/<adv_id> [POST, DELETE]
https://sf.rtru.tk/comment/<adv_id> [POST]
https://sf.rtru.tk/stat/<adv_id> [GET]
```

### Реализовано
- flask-приложение для хренения объявлений
	- flask-mongoengine
	- Flask-RESTful
	- Flask-Caching
- Все GET запросы кешируются в Redis при первом обращении
- Если что-то поменяется в Mongodb, то соответствующая запись в Redis стирается
- Dockerfile и docker-compose.yml

### Установка
- скачать проект и перейти в директорию проекта
```
$ git clone https://github.com/LovingFox/PWS-15_e7_mongo_redis
$ cd PWS-15_e7_mongo_redis
```
- собрать контейнеры
```
$ docker-compose build
```
- запустить контейнеры
```
$ docker-compose up
```
## Использование
### На примере утилиты _http_
- /advs GET
```
$ http http://0.0.0.0:5001/advs
```
 - /advs POST
```
$ http http://0.0.0.0:5001/advs title="Title 1" body="Body Text Message1"
$ http http://0.0.0.0:5001/advs title="Title 2" body="Body Text Message2" tags:='["tag1", "tag2"]'
$ http http://0.0.0.0:5001/advs title="Title 3" body="Body Text Message3" comments:='["comment text 1", "comment text 2"]'
$ http http://0.0.0.0:5001/advs title="Title 4" body="Body Text Message4" tags:='["tag1", "tag2"]' comments:='["comment text 1", "comment text 2"]'
```
- /adv GET
```
$ http http://0.0.0.0:5001/adv/5f959c59e1d2600eb93045b7
```
- /adv PATCH
```
$ http patch http://0.0.0.0:5001/adv/5f959c59e1d2600eb93045b7 title="New Title"
$ http patch http://0.0.0.0:5001/adv/5f959c59e1d2600eb93045b7 bode="New Body text message"
```
- /adv DELETE
```
$ http delete http://0.0.0.0:5001/adv/5f959c59e1d2600eb93045b7
```
- /tags POST
```
$ http post http://0.0.0.0:5001/tags/5f959c59e1d2600eb93045b7 tags:='["new_tag1", "new_tag2"]'
```
- /tags DELETE
```
$ http delete http://0.0.0.0:5001/tags/5f959c59e1d2600eb93045b7 tags:='["tag_name1", "tag_name2"]'
```
- /comment POST
```
$ http post http://0.0.0.0:5001/comment/5f959c59e1d2600eb93045b7 comment="New Comment text message"
```
- /stat GET
```
$ http http://0.0.0.0:5001/stat/5f959c59e1d2600eb93045b7
```


