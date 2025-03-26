# Agence de voyage Les Merguez
Toutes destinations saucisses confondues <img src="static/sausage.png" alt="Merguez" width="40"/>

---

## Getting Started

``` bash
pip install -r requirements.txt
python3 manage.py runserver
```
Visit http://127.0.0.1:5000 to see your app running

Production deployment: https://agencelesmerguez-zoex-dev.fl0.io/

FL0: https://app.fl0.com/agencelesmerguez/kayak-scraper/dev/agencelesmerguez/deployments

## Run the website
 ``` bash
python3 manage.py runserver
 ```

## Create new app (like polls)
``` bash
python3 manage.py startapp APP_NAME
```

## Create an admin
``` bash
python3 manage.py createsuperuser
```

## Three-step guide to making model changes
- Change your models (in models.py).
- Run ```python manage.py makemigrations``` to create migrations for those changes.
- Run ```python manage.py migrate``` to apply those changes to the database.

## Options
```
[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    optimizemigration
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```
