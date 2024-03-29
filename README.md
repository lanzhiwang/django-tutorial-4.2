# 第一部分: 基本操作

参考: https://docs.djangoproject.com/en/4.2/intro/tutorial01/

```bash
$ docker run -ti --rm --name my-first-django \
-p 0.0.0.0:8000:8000 \
-v ~/work/code/py_code/django/django-tutorial-4.2:/django-tutorial-4.2 \
-w /django-tutorial-4.2 \
python:3.10-bullseye \
bash

# 安装依赖
$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 创建项目
$ django-admin startproject mysite

# 将 models 转为 SQL
$ python manage.py makemigrations
No changes detected

# 在数据库中执行 SQL
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

```

数据库中存在以下数据表
![](./images/01.png)

```bash

find . -name __pycache__ -type d -exec rm -rf {} \;

# 启动服务
python manage.py runserver 0.0.0.0:8000

```

# 第二部分: Logging

* https://docs.djangoproject.com/en/4.2/topics/logging/
* https://pymotw.com/3/logging/index.html

Logging 默认配置

```bash
$ python manage.py runserver 0.0.0.0:8000
<--""
   Level WARNING
************************************ manage.py ************************************
<--""
   Level WARNING
************************************ manage.py ************************************
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 16, 2024 - 04:32:14
Django version 4.2.11, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

<--""
   Level WARNING
   |
   o<--"asyncio"
   |   Level NOTSET so inherits level WARNING
   |
   o<--[concurrent]
   |   |
   |   o<--"concurrent.futures"
   |       Level NOTSET so inherits level WARNING
   |
   o<--"django"
       Level INFO
       Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
         Level INFO
         Filter <django.utils.log.RequireDebugTrue object at 0x7faa6362a740>
       Handler <AdminEmailHandler (ERROR)>
         Level ERROR
         Filter <django.utils.log.RequireDebugFalse object at 0x7faa635b2ef0>
       |
       o<--[django.db]
       |   |
       |   o<--"django.db.backends"
       |   |   Level NOTSET so inherits level INFO
       |   |   |
       |   |   o<--"django.db.backends.base"
       |   |   |   Level NOTSET so inherits level INFO
       |   |   |
       |   |   o<--"django.db.backends.schema"
       |   |       Level NOTSET so inherits level INFO
       |   |
       |   o<--"django.db.models"
       |       Level NOTSET so inherits level INFO
       |
       o<--"django.dispatch"
       |   Level NOTSET so inherits level INFO
       |
       o<--"django.request"
       |   Level NOTSET so inherits level INFO
       |
       o<--[django.security]
       |   |
       |   o<--"django.security.csrf"
       |       Level NOTSET so inherits level INFO
       |
       o   "django.server"
       |   Level INFO
       |   Propagate OFF
       |   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
       |     Level INFO
       |     Formatter <django.utils.log.ServerFormatter object at 0x7faa636695d0>
       |
       o<--"django.template"
       |   Level NOTSET so inherits level INFO
       |
       o<--[django.utils]
           |
           o<--"django.utils.autoreload"
               Level NOTSET so inherits level INFO
************************************ polls views.py index ************************************
[16/Mar/2024 04:32:20] "GET /polls/ HTTP/1.1" 200 40

```

Logging 增加配置

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.dispatch": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}

```

```bash
$ python manage.py runserver 0.0.0.0:8000
<--""
   Level WARNING
************************************ manage.py ************************************
<--""
   Level WARNING
************************************ manage.py ************************************
Watching for file changes with StatReloader
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
(0.002)
            SELECT name, type FROM sqlite_master
            WHERE type in ('table', 'view') AND NOT name='sqlite_sequence'
            ORDER BY name; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
March 16, 2024 - 04:53:44
Django version 4.2.11, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.


<--""
   Level WARNING
   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
   |
   o<--"asyncio"
   |   Level NOTSET so inherits level WARNING
   |
   o<--[concurrent]
   |   |
   |   o<--"concurrent.futures"
   |       Level NOTSET so inherits level WARNING
   |
   o<--"django"
       Level INFO
       Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
         Level INFO
         Filter <django.utils.log.RequireDebugTrue object at 0x7f47cdbe2a70>
       Handler <AdminEmailHandler (ERROR)>
         Level ERROR
         Filter <django.utils.log.RequireDebugFalse object at 0x7f47cdbe3fd0>
       |
       o   "django.db"
       |   Level DEBUG
       |   Propagate OFF
       |   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
       |   |
       |   o<--"django.db.backends"
       |   |   Level NOTSET so inherits level DEBUG
       |   |   |
       |   |   o<--"django.db.backends.base"
       |   |   |   Level NOTSET so inherits level DEBUG
       |   |   |
       |   |   o<--"django.db.backends.schema"
       |   |       Level NOTSET so inherits level DEBUG
       |   |
       |   o<--"django.db.models"
       |       Level NOTSET so inherits level DEBUG
       |
       o   "django.dispatch"
       |   Level DEBUG
       |   Propagate OFF
       |   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
       |
       o   "django.request"
       |   Level DEBUG
       |   Propagate OFF
       |   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
       |
       o<--[django.security]
       |   |
       |   o<--"django.security.csrf"
       |       Level NOTSET so inherits level INFO
       |
       o   "django.server"
       |   Level INFO
       |   Propagate OFF
       |   Handler Stream <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
       |     Level INFO
       |     Formatter <django.utils.log.ServerFormatter object at 0x7f47cdc8cfd0>
       |
       o<--"django.template"
       |   Level NOTSET so inherits level INFO
       |
       o<--[django.utils]
           |
           o<--"django.utils.autoreload"
               Level NOTSET so inherits level INFO
************************************ polls views.py index ************************************
[16/Mar/2024 04:53:53] "GET /polls/ HTTP/1.1" 200 40


```

# 第三部分: Models and databases

* https://docs.djangoproject.com/en/4.2/topics/db/


# 第四部分: settings

# 第五部分: admin

* https://docs.djangoproject.com/en/4.2/intro/tutorial02/

# 第六部分：URL

```bash
python manage.py startapp myurl

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-extensions==3.2.3

python manage.py show_urls
```

测试用例：tests/urlpatterns

参考：
* https://docs.djangoproject.com/en/4.2/topics/http/urls/
* https://medium.com/@suhast_40578/url-namespacing-and-views-in-django-e792c9308366
* https://www.cnblogs.com/ZFBG/p/11521842.html

