# Models and databases

主要参考：

* https://docs.djangoproject.com/en/4.2/topics/db/

Django 是一个流行的 Web 框架，Django 使您可以更轻松地使用更少的代码更快地构建更好的 Web 应用程序。

其中 Django Models 提供强大的和数据库交互的相关功能。

本文总结 Django Models 的相关功能和用法。

在数据库中，有几个很基础，但是很重要的操作，分别是：

1. 创建数据表

2. 对数据记录的增加，删除，修改

3. 对数据记录的查找，之所以将查找单独列出来，是因为条件查找很复杂，尤其是多表的条件查找更复杂

Django Models 对上述的三类操作都提供了强大的支持，下面分别描述。

在描述 Django Models 之前，先说明一个调试 Django Models 方法。
因为定义 Django Models 就是定义数据表，相关的操作也会映射为对应的 SQL 语句，
因此，如果能实际看到最终在数据库中执行的 SQL 语句，这样就可以很快理解和判断 Django Models 相关操作是否合理。

要想实际看到在数据库中执行的 SQL 语句，只需要调整对应的日志级别即可，操作如下：

在 django settings.py 中增加如下 Log 配置

重点是将 django.db 日志级别调整为 DEBUG

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

最终效果如下：

迁移数据

```bash
$ python manage.py migrate
(0.002)
            SELECT name, type FROM sqlite_master
            WHERE type in ('table', 'view') AND NOT name='sqlite_sequence'
            ORDER BY name; args=None; alias=default
(0.001)
            SELECT name, type FROM sqlite_master
            WHERE type in ('table', 'view') AND NOT name='sqlite_sequence'
            ORDER BY name; args=None; alias=default
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, myapp, myapp2, polls, sessions
Running migrations:
(0.001)
            SELECT name, type FROM sqlite_master
            WHERE type in ('table', 'view') AND NOT name='sqlite_sequence'
            ORDER BY name; args=None; alias=default
(0.000) PRAGMA foreign_keys = OFF; args=None; alias=default
(0.000) PRAGMA foreign_keys; args=None; alias=default
(0.000) BEGIN; args=None; alias=default
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL); (params None)
(0.004) CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL); args=None; alias=default
(0.000) PRAGMA foreign_key_check; args=None; alias=default
(0.003) COMMIT; args=None; alias=default
(0.000) PRAGMA foreign_keys = ON; args=None; alias=default
  Applying contenttypes.0001_initial...(0.000) PRAGMA foreign_keys = OFF; args=None; alias=default
(0.000) PRAGMA foreign_keys; args=None; alias=default
(0.000) BEGIN; args=None; alias=default
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL); (params None)
```

对数据库进行增删改查操作

```python

>>> from datetime import date
>>> from myapp2.models import Blog, Entry
>>>
>>> beatles = Blog.objects.create(name='Beatles Blog')
(0.020) INSERT INTO "myapp2_blog" ("name", "tagline") VALUES ('Beatles Blog', ''); args=['Beatles Blog', '']; alias=default

>>> pop = Blog.objects.create(name='Pop Music Blog')
(0.014) INSERT INTO "myapp2_blog" ("name", "tagline") VALUES ('Pop Music Blog', ''); args=['Pop Music Blog', '']; alias=default

>>> Entry.objects.create(blog=beatles, headline='New Lennon Biography', pub_date=date(2008, 6, 1))
(0.012) INSERT INTO "myapp2_entry" ("blog_id", "headline", "body_text", "pub_date", "mod_date", "number_of_comments", "number_of_pingbacks", "rating") VALUES (1, 'New Lennon Biography', '', '2008-06-01', '2024-03-16', 0, 0, 5); args=[1, 'New Lennon Biography', '', '2008-06-01', '2024-03-16', 0, 0, 5]; alias=default
<Entry: New Lennon Biography>

>>> Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
(0.001) SELECT "myapp2_blog"."id", "myapp2_blog"."name", "myapp2_blog"."tagline" FROM "myapp2_blog" INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id") WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND "myapp2_entry"."pub_date" BETWEEN '2008-01-01' AND '2008-12-31') LIMIT 21; args=('%Lennon%', '2008-01-01', '2008-12-31'); alias=default
<QuerySet [<Blog: Beatles Blog>]>
>>>

>>> Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
(0.002) SELECT "myapp2_blog"."id", "myapp2_blog"."name", "myapp2_blog"."tagline" FROM "myapp2_blog" INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id") INNER JOIN "myapp2_entry" T3 ON ("myapp2_blog"."id" = T3."blog_id") WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND T3."pub_date" BETWEEN '2008-01-01' AND '2008-12-31') LIMIT 21; args=('%Lennon%', '2008-01-01', '2008-12-31'); alias=default
<QuerySet [<Blog: Beatles Blog>, <Blog: Beatles Blog>, <Blog: Pop Music Blog>]>
>>>

```

**在下面说明的任何操作都会打印对应的日志，应该时刻查看这些日志，这样就可以很好的理解操作是否正确合理。**

## 创建数据表

在数据库中创建数据表，映射到 Django Models 中就是定义 models 类。

例如要创建如下数据表，

```
CREATE TABLE myapp_person (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

只需要在定义如下 models 类即可，

```python
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

这里有几点需要注意：

1. 一个 class Person 类代表数据库中的一张表
2. class Person 类中的类字段代表数据表中的字段

要想在实际项目中正在定义出符合要求的 models 类，还需要知道如下几点：

1. models 类中支持哪些数据类型，比如上面的 models.CharField
完整的支持字段类型参考 https://docs.djangoproject.com/en/4.2/ref/models/fields/#model-field-types
支持的每种字段类型都分别对应数据库支持的各种数据类型，需要根据实际需要合理选择

2. 除了需要定义字段类型，还需要定义字段选项，字段选项就是对字段做出的一些限制，比如最长允许的字符数
完整的支持字段选项参考 https://docs.djangoproject.com/en/4.2/ref/models/fields/#common-model-field-options

3. 我们大部分时候使用的都是关系型数据库，其中最核心的就是定义数据表之间的关联关系
Django 支持三种关联关系的定义，many-to-one, many-to-many and one-to-one
定义关联关系的方法和定义普通字段的方法差不多，

many-to-one 定义方法参考 https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ForeignKey

many-to-many 定义方法参考 https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField

one-to-one 定义方法参考 https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.OneToOneField

定义关联关系之后，怎么进行关联查询是关键，官方文档也有详细的示例参考，https://docs.djangoproject.com/en/4.2/topics/db/examples/

这里说明一个小技巧：

定义 models 类之后，models 类中会有一些相关属性，同时，定义表之间的关联关系也会额外产生一些属性，通过查看已经存在的属性，可以很好的理解定义是否正确，并且知道这些属性之后，对后面的查询操作也很有帮助，特别是多表之前的关联查询

查看 models 类中属性的实例如下：

```python
class Question(models.Model):
    """
    >>> from django.db import models
    >>> m = set(dir(models.Model))
	# models.Model 基类属性
    >>> m
    {'__weakref__', '__sizeof__', '_check_model', 'validate_constraints', 'date_error_message', 'clean_fields', '_check_field_name_clashes', '__str__', '_get_pk_val', '_check_local_fields', '__lt__', '_perform_unique_checks', '_check_db_table_comment', 'refresh_from_db', '_prepare_related_fields_for_save', '__getstate__', '_perform_date_checks', '_get_next_or_previous_by_FIELD', '_get_expr_references', '_check_default_pk', 'validate_unique', '_set_pk_val', 'save_base', '__gt__', '_check_managers', 'unique_error_message', '__class__', '__repr__', '_check_ordering', '_get_unique_checks', '_check_long_column_names', '_save_table', 'check', 'get_deferred_fields', '_save_parents', 'save', '__reduce__', '__new__', 'arefresh_from_db', 'full_clean', 'pk', '__reduce_ex__', 'asave', '_check_model_name_db_lookup_clashes', '_check_fields', '__setstate__', '_check_property_name_related_field_accessor_clashes', '_check_swappable', '__ne__', '_check_constraints', '__doc__', '_check_unique_together', '__subclasshook__', '_do_update', '_get_next_or_previous_in_order', '_check_column_name_clashes', '__ge__', '__eq__', '_check_id_field', '_check_indexes', '__format__', 'adelete', '__dir__', '_get_FIELD_display', '__module__', '__dict__', '_check_m2m_through_same_relationship', '_check_index_together', '__delattr__', '_check_single_primary_key', '_do_insert', '__init_subclass__', '__le__', '__getattribute__', 'from_db', 'clean', 'get_constraints', 'serializable_value', 'prepare_database_save', 'delete', '__init__', '__setattr__', '__hash__', '_get_field_value_map'}
    >>>
	# 自定义 models 类之后的属性，知道这里是关键
    >>> set(dir(Question)).difference(m)
    {
        'get_previous_by_pub_date',
        '_meta',
        'objects',
        'question_text',
        'id',
        'pub_date',
        'get_next_by_pub_date',
        'DoesNotExist',
        'MultipleObjectsReturned'
    }
    >>>
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

```

4. 在 models 中除了定义字段和关联关系，还可选的需要定义元数据，所谓的元数据是指数据表名称，排序规则等等。
完整的元数据定义请参考 https://docs.djangoproject.com/en/4.2/ref/models/options/


## 对数据记录的增加，删除，修改

### 增加

对数据记录的增加其实就是实例化一个 models 对象，然后保存到数据库，如下所示

```python
>>> from blog.models import Blog
>>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
>>> b.save()
```

另一种方法是调用 create 方法，如下所示：

```python
>>> from datetime import date
>>> from myapp2.models import Blog, Entry
>>>
>>> beatles = Blog.objects.create(name='Beatles Blog')
(0.020) INSERT INTO "myapp2_blog" ("name", "tagline") VALUES ('Beatles Blog', ''); args=['Beatles Blog', '']; alias=default

```

一般来说，将数据保存到数据库就是使用 `save()` 或者 `create()` 方法

### 修改和删除

对数据的修改和删除，最关键的逻辑是需要先查询或者获取数据，查询到相关数据之后，

对于修改操作，可以调用 `save()` 或者 `update()` 方法，示例如下：


```python
>>> b5.name = "New name"
>>> b5.save()

>>> Entry.objects.filter(pub_date__year=2007).update(headline="Everything is the same")

```

对于删除操作，可以调用 `delete()` 方法，示例如下：

```python
>>> b = Blog.objects.get(pk=1)
>>> b.delete()

```

## 对数据记录的查询

对数据库的查询是重中之重，为了充分理解 django models 最终执行的查询操作，需要时刻查看上面的日志，看最终的 SQL 语句是否符合要求。

总体来说，使用 django models 进行查询有三个核心要点：

1. 定义 django models 之后，modles 类中会自动注入一个 `object` 属性
`object` 属性是一个 `Managers` 类的实例，`Managers` 类提供了一些方法用于查询操作

`Managers` 类提供的查询方法基本都会返回 `QuerySet` 对象，最终我们的数据都封装在 `QuerySet` 对象中

```python
>>> Blog.objects
<django.db.models.manager.Manager object at ...>

>>> all_entries = Entry.objects.all()
```

2. 对于查询来说，最重要的就是 `Managers` 对象中的 `filter()`、`F()`、`Q()` 三个方法

filter() 用于构建查询条件，类似 SQL 语句中的 where 条件语句

F() 方法用于引用数据字段，引用的数据字段用于 filter() 参数

Q() 方法用于构建复杂的条件查询，查询条件也用于 filter() 参数

3. 如上所述，查询最重要的就是构建查询条件
在 django models 中构建查询条件采用了一种独特的格式

`field__lookuptype=value`

field 表示 models 中的字段

lookuptype 表示查询类型，中间使用双下划线

例如

```python
>>> Entry.objects.filter(pub_date__lte="2006-01-01")
translates (roughly) into the following SQL:

SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

```

pub_date 表示 models 中的字段

lte 表示小于等于

合并起来就是 `pub_date <= '2006-01-01'`

因此掌握 lookuptype 就是重中之重，django 支持多种 lookuptype，例如 exact、iexact、contains、icontains 等等

完整的 lookuptype 请参考 https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups

最快的掌握这些 lookuptype 的方法就是直接查看日志确定最终生成的 SQL 语句。


### 多表关联查询

Django 支持三种关联关系的定义，many-to-one, many-to-many and one-to-one，因此多表关联查询就成为可能。
掌握多表关联查询的关键点就是要知道定义关联关系之后，models 中增加的额外字段的含义，例如

```python
class Manufacturer(models.Model):
    """
    >>> set(dir(Manufacturer)).difference(m)
    {'car_set', '_meta', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    pass


class Car(models.Model):
    """
    >>> set(dir(Car)).difference(m)
    {'manufacturer_id', 'manufacturer', '_meta', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...

```

汽车和汽车制造商之前存在一对一的关系，也就是一辆汽车只有一个汽车制造商，所以在 Car 类中定义了 manufacturer 字段，表示这辆汽车的汽车制造商。

如上所示，Car 类中就有了 manufacturer 属性，Manufacturer 类中就有了 car_set 属性，注意，这个属性是自动添加的，不需要认为干预，并且这个字段的名称可以自定义。

在 Car 类中，如果要查找汽车制造商的信息，直接使用 manufacturer 字段即可
在 Manufacturer 类中，如果要查找汽车信息，直接使用 car_set 字段即可
使用方法和普通字段一样。

同样的，在多对多关系中，也有相应的字段，和多对一完全相同

```python
# Many-to-many relationships
class Topping(models.Model):
    """
    >>> set(dir(Topping)).difference(m)
    {'_meta', 'pizza_set', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    pass


class Pizza(models.Model):
    """
    >>> set(dir(Pizza)).difference(m)
    {'_meta', 'toppings', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    toppings = models.ManyToManyField(Topping)

```

