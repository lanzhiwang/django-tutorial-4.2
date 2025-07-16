# Models and databases

## [Many-to-many relationships](https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_many/)

```python
from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline

"""
CREATE TABLE "myapp_article" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "headline" varchar(100) NOT NULL
)

CREATE TABLE "myapp_publication" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(30) NOT NULL
)

CREATE TABLE "myapp_article_publications" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "article_id" bigint NOT NULL REFERENCES "myapp_article" ("id") DEFERRABLE INITIALLY DEFERRED,
    "publication_id" bigint NOT NULL REFERENCES "myapp_publication" ("id") DEFERRABLE INITIALLY DEFERRED
)

"""

```

```bash
root@0867e20c8b98:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>> from myapp.models import Publication, Article
>>>
>>> p1 = Publication(title="The Python Journal")
>>> p1.save()
(0.018) INSERT INTO "myapp_publication" ("title") VALUES ('The Python Journal'); args=['The Python Journal']; alias=default
>>>
>>> p2 = Publication(title="Science News")
>>> p2.save()
(0.017) INSERT INTO "myapp_publication" ("title") VALUES ('Science News'); args=['Science News']; alias=default
>>>
>>> p3 = Publication(title="Science Weekly")
>>> p3.save()
(0.018) INSERT INTO "myapp_publication" ("title") VALUES ('Science Weekly'); args=['Science Weekly']; alias=default
>>>
>>> a1 = Article(headline="Django lets you build web apps easily")
>>> a1.publications.add(p1)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/fields/related_descriptors.py", line 617, in __get__
    return self.related_manager_cls(instance)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/fields/related_descriptors.py", line 1022, in __init__
    raise ValueError(
ValueError: "<Article: Django lets you build web apps easily>" needs to have a value for field "id" before this many-to-many relationship can be used.
>>>
>>> a1.save()
(0.018) INSERT INTO "myapp_article" ("headline") VALUES ('Django lets you build web apps easily'); args=['Django lets you build web apps easily']; alias=default
>>>
# 使用 publications 属性
>>> a1.publications.add(p1)
(0.000) BEGIN; args=None; alias=default
(0.020) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (1, 1); args=(1, 1); alias=default
(0.006) COMMIT; args=None; alias=default
>>>
>>> a2 = Article(headline="NASA uses Python")
>>> a2.save()
(0.021) INSERT INTO "myapp_article" ("headline") VALUES ('NASA uses Python'); args=['NASA uses Python']; alias=default

>>> a2.publications.add(p1, p2)
(0.000) BEGIN; args=None; alias=default
(0.021) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (2, 1), (2, 2); args=(2, 1, 2, 2); alias=default
(0.008) COMMIT; args=None; alias=default

>>> a2.publications.add(p3)
(0.000) BEGIN; args=None; alias=default
(0.015) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (2, 3); args=(2, 3); alias=default
(0.007) COMMIT; args=None; alias=default
>>>

>>> a2.publications.add(p3)
(0.000) BEGIN; args=None; alias=default
(0.009) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (2, 3); args=(2, 3); alias=default
(0.005) COMMIT; args=None; alias=default
>>>

# 使用 publications 属性
>>> new_publication = a2.publications.create(title="Highlights for Children")
(0.016) INSERT INTO "myapp_publication" ("title") VALUES ('Highlights for Children'); args=['Highlights for Children']; alias=default
(0.000) BEGIN; args=None; alias=default
(0.015) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (2, 4); args=(2, 4); alias=default
(0.008) COMMIT; args=None; alias=default
>>>

>>> dir(Publication)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'adelete', 'arefresh_from_db', 'article_set', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'title', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>>
>>> dir(p1)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'adelete',
    'arefresh_from_db',
    'article_set',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'id',
    'objects',
    'pk',
    'prepare_database_save',
    'refresh_from_db',
    'save',
    'save_base',
    'serializable_value',
    'title',
    'unique_error_message',
    'validate_constraints',
    'validate_unique'
]
>>>

>>> dir(Article)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'headline', 'id', 'objects', 'pk', 'prepare_database_save', 'publications', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>>
>>> dir(a1)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'adelete',
    'arefresh_from_db',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'headline',
    'id',
    'objects',
    'pk',
    'prepare_database_save',
    'publications',
    'refresh_from_db',
    'save',
    'save_base',
    'serializable_value',
    'unique_error_message',
    'validate_constraints',
    'validate_unique'
]
>>>


# 使用 publications 属性
>>> a1.publications.all()
(0.004) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> a2.publications.all()
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 2 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>, <Publication: The Python Journal>]>
>>>

# 使用 article_set 属性
>>> p2.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: NASA uses Python>]>
>>>
>>> p1.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Publication.objects.get(id=4).article_set.all()
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" WHERE "myapp_publication"."id" = 4 LIMIT 21; args=(4,); alias=default
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 4 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(4,); alias=default
<QuerySet [<Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__id=1)
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__pk=1)
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications=1)
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications=p1)
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__title__startswith="Science")
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") INNER JOIN "myapp_publication" ON ("myapp_article_publications"."publication_id" = "myapp_publication"."id") WHERE "myapp_publication"."title" LIKE 'Science%' ESCAPE '\' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('Science%',); alias=default
<QuerySet [<Article: NASA uses Python>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__title__startswith="Science").distinct()
(0.002) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") INNER JOIN "myapp_publication" ON ("myapp_article_publications"."publication_id" = "myapp_publication"."id") WHERE "myapp_publication"."title" LIKE 'Science%' ESCAPE '\' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('Science%',); alias=default
<QuerySet [<Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__title__startswith="Science").count()
(0.001) SELECT COUNT(*) AS "__count" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") INNER JOIN "myapp_publication" ON ("myapp_article_publications"."publication_id" = "myapp_publication"."id") WHERE "myapp_publication"."title" LIKE 'Science%' ESCAPE '\'; args=('Science%',); alias=default
2
>>>
>>> Article.objects.filter(publications__title__startswith="Science").distinct().count()
(0.002) SELECT COUNT(*) FROM (SELECT DISTINCT "myapp_article"."id" AS "col1", "myapp_article"."headline" AS "col2" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") INNER JOIN "myapp_publication" ON ("myapp_article_publications"."publication_id" = "myapp_publication"."id") WHERE "myapp_publication"."title" LIKE 'Science%' ESCAPE '\') subquery; args=('Science%',); alias=default
1
>>>
>>> Article.objects.filter(publications__in=[1, 2]).distinct()
(0.002) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" IN (1, 2) ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Article.objects.filter(publications__in=[p1, p2]).distinct()
(0.001) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" IN (1, 2) ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA uses Python>]>
>>>
>>> Publication.objects.filter(id=1)
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" WHERE "myapp_publication"."id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(pk=1)
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" WHERE "myapp_publication"."id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>

# 使用 article 属性, 没有使用 article_set 属性
>>> Publication.objects.filter(article__headline__startswith="NASA")
(0.003) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") INNER JOIN "myapp_article" ON ("myapp_article_publications"."article_id" = "myapp_article"."id") WHERE "myapp_article"."headline" LIKE 'NASA%' ESCAPE '\' ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=('NASA%',); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>, <Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article__id=1)
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article__pk=1)
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article=1)
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article=a1)
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article__in=[1, 2]).distinct()
(0.002) SELECT DISTINCT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" IN (1, 2) ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>, <Publication: The Python Journal>]>
>>>
>>> Publication.objects.filter(article__in=[a1, a2]).distinct()
(0.002) SELECT DISTINCT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" IN (1, 2) ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>, <Publication: The Python Journal>]>
>>>
>>> Article.objects.exclude(publications=p2)
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" WHERE NOT (EXISTS(SELECT 1 AS "a" FROM "myapp_article_publications" U1 WHERE (U1."publication_id" = 2 AND U1."article_id" = ("myapp_article"."id")) LIMIT 1)) ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Article: Django lets you build web apps easily>]>
>>>
>>> p1.delete()
(0.000) BEGIN; args=None; alias=default
(0.014) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."publication_id" IN (1); args=(1,); alias=default
(0.002) DELETE FROM "myapp_publication" WHERE "myapp_publication"."id" IN (1); args=(1,); alias=default
(0.006) COMMIT; args=None; alias=default
(3, {'myapp.Article_publications': 2, 'myapp.Publication': 1})
>>>
>>> Publication.objects.all()
(0.004) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>]>
>>>
>>> a1 = Article.objects.get(pk=1)
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" WHERE "myapp_article"."id" = 1 LIMIT 21; args=(1,); alias=default
>>>
>>> a1.publications.all()
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 1 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(1,); alias=default
<QuerySet []>
>>>
>>> a2.delete()
(0.000) BEGIN; args=None; alias=default
(0.013) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."article_id" IN (2); args=(2,); alias=default
(0.002) DELETE FROM "myapp_article" WHERE "myapp_article"."id" IN (2); args=(2,); alias=default
(0.008) COMMIT; args=None; alias=default
(4, {'myapp.Article_publications': 3, 'myapp.Article': 1})
>>>
>>> Article.objects.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Article: Django lets you build web apps easily>]>
>>>
>>> p2.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet []>
>>>
>>> a4 = Article(headline="NASA finds intelligent life on Earth")
>>> a4.save()
(0.013) INSERT INTO "myapp_article" ("headline") VALUES ('NASA finds intelligent life on Earth'); args=['NASA finds intelligent life on Earth']; alias=default
# 使用 article_set 属性
>>> p2.article_set.add(a4)
(0.000) BEGIN; args=None; alias=default
(0.015) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (3, 2); args=(3, 2); alias=default
(0.009) COMMIT; args=None; alias=default
>>> p2.article_set.all()
(0.004) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: NASA finds intelligent life on Earth>]>
>>> a4.publications.all()
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet [<Publication: Science News>]>
>>>

# 使用 article_set 属性
>>> new_article = p2.article_set.create(headline="Oxygen-free diet works wonders")
(0.015) INSERT INTO "myapp_article" ("headline") VALUES ('Oxygen-free diet works wonders'); args=['Oxygen-free diet works wonders']; alias=default
(0.000) BEGIN; args=None; alias=default
(0.016) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (4, 2); args=(4, 2); alias=default
(0.006) COMMIT; args=None; alias=default
>>> p2.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: NASA finds intelligent life on Earth>, <Article: Oxygen-free diet works wonders>]>
>>> a5 = p2.article_set.all()[1]
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 1 OFFSET 1; args=(2,); alias=default
>>> a5.publications.all()
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 4 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(4,); alias=default
<QuerySet [<Publication: Science News>]>
>>>
>>> a4.publications.remove(p2)
(0.000) BEGIN; args=None; alias=default
(0.015) DELETE FROM "myapp_article_publications" WHERE ("myapp_article_publications"."article_id" = 3 AND "myapp_article_publications"."publication_id" IN (2)); args=(3, 2); alias=default
(0.006) COMMIT; args=None; alias=default
>>> a4.publications.all()
(0.004) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet []>
>>>
>>> p2.article_set.all()
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: Oxygen-free diet works wonders>]>
>>>

# 使用 article_set 属性
>>> p2.article_set.remove(a5)
(0.000) BEGIN; args=None; alias=default
(0.015) DELETE FROM "myapp_article_publications" WHERE ("myapp_article_publications"."publication_id" = 2 AND "myapp_article_publications"."article_id" IN (4)); args=(2, 4); alias=default
(0.006) COMMIT; args=None; alias=default
>>> p2.article_set.all()
(0.004) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet []>
>>> a5.publications.all()
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 4 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(4,); alias=default
<QuerySet []>
>>>

>>> a4.publications.all()
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet []>
>>> a4.publications.set([p3])
(0.000) BEGIN; args=None; alias=default
(0.002) SELECT "myapp_publication"."id" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC; args=(3,); alias=default
(0.014) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (3, 3); args=(3, 3); alias=default
(0.007) COMMIT; args=None; alias=default
>>> a4.publications.all()
(0.003) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet [<Publication: Science Weekly>]>
>>>

>>> p3.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 3 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(3,); alias=default
<QuerySet [<Article: NASA finds intelligent life on Earth>]>
>>> p3.article_set.clear()
(0.000) BEGIN; args=None; alias=default
(0.014) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."publication_id" = 3; args=(3,); alias=default
(0.006) COMMIT; args=None; alias=default
>>> p3.article_set.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 3 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(3,); alias=default
<QuerySet []>
>>>

>>> p2.article_set.add(a4, a5)
(0.000) BEGIN; args=None; alias=default
(0.016) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (3, 2), (4, 2); args=(3, 2, 4, 2); alias=default
(0.008) COMMIT; args=None; alias=default
>>> p2.article_set.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: NASA finds intelligent life on Earth>, <Article: Oxygen-free diet works wonders>]>
>>> a4.publications.all()
(0.002) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet [<Publication: Science News>]>
>>> a4.publications.clear()
(0.000) BEGIN; args=None; alias=default
(0.011) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."article_id" = 3; args=(3,); alias=default
(0.006) COMMIT; args=None; alias=default
>>> a4.publications.all()
(0.004) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 3 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(3,); alias=default
<QuerySet []>
>>> p2.article_set.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: Oxygen-free diet works wonders>]>
>>>
>>> p1 = Publication(title="The Python Journal")
>>> p1.save()
(0.016) INSERT INTO "myapp_publication" ("title") VALUES ('The Python Journal'); args=['The Python Journal']; alias=default
>>> a2 = Article(headline="NASA uses Python")
>>> a2.save()
(0.020) INSERT INTO "myapp_article" ("headline") VALUES ('NASA uses Python'); args=['NASA uses Python']; alias=default
>>> a2.publications.add(p1, p2, p3)
(0.000) BEGIN; args=None; alias=default
(0.018) INSERT OR IGNORE INTO "myapp_article_publications" ("article_id", "publication_id") VALUES (5, 2), (5, 3), (5, 5); args=(5, 2, 5, 3, 5, 5); alias=default
(0.006) COMMIT; args=None; alias=default
>>> Publication.objects.filter(title__startswith="Science").delete()
(0.003) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" WHERE "myapp_publication"."title" LIKE 'Science%' ESCAPE '\'; args=('Science%',); alias=default
(0.000) BEGIN; args=None; alias=default
(0.015) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."publication_id" IN (2, 3); args=(2, 3); alias=default
(0.002) DELETE FROM "myapp_publication" WHERE "myapp_publication"."id" IN (3, 2); args=(3, 2); alias=default
(0.007) COMMIT; args=None; alias=default
(5, {'myapp.Article_publications': 3, 'myapp.Publication': 2})
>>> Publication.objects.all()
(0.004) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Publication: Highlights for Children>, <Publication: The Python Journal>]>
>>> Article.objects.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Article: Django lets you build web apps easily>, <Article: NASA finds intelligent life on Earth>, <Article: NASA uses Python>, <Article: Oxygen-free diet works wonders>]>
>>> a2.publications.all()
(0.001) SELECT "myapp_publication"."id", "myapp_publication"."title" FROM "myapp_publication" INNER JOIN "myapp_article_publications" ON ("myapp_publication"."id" = "myapp_article_publications"."publication_id") WHERE "myapp_article_publications"."article_id" = 5 ORDER BY "myapp_publication"."title" ASC LIMIT 21; args=(5,); alias=default
<QuerySet [<Publication: The Python Journal>]>
>>>
>>> q = Article.objects.filter(headline__startswith="Django")
>>> q
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" WHERE "myapp_article"."headline" LIKE 'Django%' ESCAPE '\' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('Django%',); alias=default
<QuerySet [<Article: Django lets you build web apps easily>]>
>>> q.delete()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" WHERE "myapp_article"."headline" LIKE 'Django%' ESCAPE '\'; args=('Django%',); alias=default
(0.000) BEGIN; args=None; alias=default
(0.001) DELETE FROM "myapp_article_publications" WHERE "myapp_article_publications"."article_id" IN (1); args=(1,); alias=default
(0.007) DELETE FROM "myapp_article" WHERE "myapp_article"."id" IN (1); args=(1,); alias=default
(0.005) COMMIT; args=None; alias=default
(1, {'myapp.Article': 1})
>>> q
(0.004) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" WHERE "myapp_article"."headline" LIKE 'Django%' ESCAPE '\' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('Django%',); alias=default
<QuerySet []>
>>> p1.article_set.all()
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline" FROM "myapp_article" INNER JOIN "myapp_article_publications" ON ("myapp_article"."id" = "myapp_article_publications"."article_id") WHERE "myapp_article_publications"."publication_id" = 5 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(5,); alias=default
<QuerySet [<Article: NASA uses Python>]>
>>>

```

## [Many-to-one relationships](https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/)

```python
from django.db import models


"""
In this example, a Reporter can be associated with many Article objects, but an Article can only have one Reporter object:
"""
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["headline"]

"""
CREATE TABLE "myapp_article" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "headline" varchar(100) NOT NULL,
    "pub_date" date NOT NULL,
    "reporter_id" bigint NOT NULL REFERENCES "myapp_reporter" ("id") DEFERRABLE INITIALLY DEFERRED
)

CREATE TABLE "myapp_reporter" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(254) NOT NULL
)
"""

```

```bash
root@3ba3f34d6e40:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>>
>>> from myapp.models import Reporter, Article
>>>
>>> r = Reporter(first_name="John", last_name="Smith", email="john@example.com")
>>> r.save()
(0.017) INSERT INTO "myapp_reporter" ("first_name", "last_name", "email") VALUES ('John', 'Smith', 'john@example.com'); args=['John', 'Smith', 'john@example.com']; alias=default
>>>
>>> r2 = Reporter(first_name="Paul", last_name="Jones", email="paul@example.com")
>>> r2.save()
(0.020) INSERT INTO "myapp_reporter" ("first_name", "last_name", "email") VALUES ('Paul', 'Jones', 'paul@example.com'); args=['Paul', 'Jones', 'paul@example.com']; alias=default
>>>
>>> from datetime import date
>>> a = Article(id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
>>> a.save()
(0.023) INSERT INTO "myapp_article" ("headline", "pub_date", "reporter_id") VALUES ('This is a test', '2005-07-27', 1); args=['This is a test', '2005-07-27', 1]; alias=default
>>> a.reporter.id
1
>>> a.reporter
<Reporter: John Smith>
>>>

>>> dir(Reporter)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'adelete', 'arefresh_from_db', 'article_set', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'email', 'first_name', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'last_name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>>
>>> dir(r)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'adelete',
    'arefresh_from_db',
    'article_set',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'email',
    'first_name',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'id',
    'last_name',
    'objects',
    'pk',
    'prepare_database_save',
    'refresh_from_db',
    'save',
    'save_base',
    'serializable_value',
    'unique_error_message',
    'validate_constraints',
    'validate_unique'
]
>>>
>>> dir(Article)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'get_next_by_pub_date', 'get_previous_by_pub_date', 'headline', 'id', 'objects', 'pk', 'prepare_database_save', 'pub_date', 'refresh_from_db', 'reporter', 'reporter_id', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>>
>>> dir(a)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'adelete',
    'arefresh_from_db',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'get_next_by_pub_date',
    'get_previous_by_pub_date',
    'headline',
    'id',
    'objects',
    'pk',
    'prepare_database_save',
    'pub_date',
    'refresh_from_db',
    'reporter',
    'reporter_id',
    'save',
    'save_base',
    'serializable_value',
    'unique_error_message',
    'validate_constraints',
    'validate_unique'
]
>>>

>>> r3 = Reporter(first_name="John", last_name="Smith", email="john@example.com")
>>> Article.objects.create(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r3)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/base.py", line 778, in save
    self._prepare_related_fields_for_save(operation_name="save")
  File "/usr/local/lib/python3.10/site-packages/django/db/models/base.py", line 1093, in _prepare_related_fields_for_save
    raise ValueError(
ValueError: save() prohibited to prevent data loss due to unsaved related object 'reporter'.
>>>

>>> r = a.reporter
>>> new_article = r.article_set.create(headline="John's second story", pub_date=date(2005, 7, 29))
(0.020) INSERT INTO "myapp_article" ("headline", "pub_date", "reporter_id") VALUES ('John''s second story', '2005-07-29', 1); args=["John's second story", '2005-07-29', 1]; alias=default
>>> new_article
<Article: John's second story>
>>> new_article.reporter
<Reporter: John Smith>
>>> new_article.reporter.id
1
>>>

>>> new_article2 = Article.objects.create( headline="Paul's story", pub_date=date(2006, 1, 17), reporter=r)
(0.019) INSERT INTO "myapp_article" ("headline", "pub_date", "reporter_id") VALUES ('Paul''s story', '2006-01-17', 1); args=["Paul's story", '2006-01-17', 1]; alias=default
>>> new_article2.reporter
<Reporter: John Smith>
>>> new_article2.reporter.id
1
>>> r.article_set.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
>>>

>>> r2.article_set.add(new_article2)
(0.017) UPDATE "myapp_article" SET "reporter_id" = 2 WHERE "myapp_article"."id" IN (3); args=(2, 3); alias=default
>>> new_article2.reporter.id
2
>>> new_article2.reporter
<Reporter: Paul Jones>
>>>
>>>
>>> r.article_set.all()
(0.004) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> r2.article_set.all()
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 2 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(2,); alias=default
<QuerySet [<Article: Paul's story>]>
>>> r.article_set.count()
(0.001) SELECT COUNT(*) AS "__count" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1; args=(1,); alias=default
2
>>> r2.article_set.count()
(0.002) SELECT COUNT(*) AS "__count" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 2; args=(2,); alias=default
1
>>>

>>> r.article_set.filter(headline__startswith="This")
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE ("myapp_article"."reporter_id" = 1 AND "myapp_article"."headline" LIKE 'This%' ESCAPE '\') ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 'This%'); alias=default
<QuerySet [<Article: This is a test>]>
>>>
>>> Article.objects.filter(reporter__first_name="John")
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" INNER JOIN "myapp_reporter" ON ("myapp_article"."reporter_id" = "myapp_reporter"."id") WHERE "myapp_reporter"."first_name" = 'John' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('John',); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>>

>>> Article.objects.filter(reporter__first_name="John")
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" INNER JOIN "myapp_reporter" ON ("myapp_article"."reporter_id" = "myapp_reporter"."id") WHERE "myapp_reporter"."first_name" = 'John' ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('John',); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter__first_name="John", reporter__last_name="Smith")
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" INNER JOIN "myapp_reporter" ON ("myapp_article"."reporter_id" = "myapp_reporter"."id") WHERE ("myapp_reporter"."first_name" = 'John' AND "myapp_reporter"."last_name" = 'Smith') ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('John', 'Smith'); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>>

>>> Article.objects.filter(reporter__pk=1)
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter=1)
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter=r)
(0.001) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" = 1 ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1,); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter__in=[1, 2]).distinct()
(0.001) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" IN (1, 2) ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter__in=[r, r2]).distinct()
(0.001) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" IN (1, 2) ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(1, 2); alias=default
<QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
>>> Article.objects.filter(reporter__in=Reporter.objects.filter(first_name="John")).distinct()
(0.002) SELECT DISTINCT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" WHERE "myapp_article"."reporter_id" IN (SELECT U0."id" FROM "myapp_reporter" U0 WHERE U0."first_name" = 'John') ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=('John',); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>>

>>> Reporter.objects.filter(article__pk=1)
(0.002) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article=1)
(0.001) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article=a)
(0.001) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article__headline__startswith="This")
(0.001) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."headline" LIKE 'This%' ESCAPE '\' LIMIT 21; args=('This%',); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article__headline__startswith="This").distinct()
(0.001) SELECT DISTINCT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."headline" LIKE 'This%' ESCAPE '\' LIMIT 21; args=('This%',); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article__headline__startswith="This").count()
(0.001) SELECT COUNT(*) AS "__count" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."headline" LIKE 'This%' ESCAPE '\'; args=('This%',); alias=default
1
>>> Reporter.objects.filter(article__headline__startswith="This").distinct().count()
(0.002) SELECT COUNT(*) FROM (SELECT DISTINCT "myapp_reporter"."id" AS "col1", "myapp_reporter"."first_name" AS "col2", "myapp_reporter"."last_name" AS "col3", "myapp_reporter"."email" AS "col4" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."headline" LIKE 'This%' ESCAPE '\') subquery; args=('This%',); alias=default
1
>>>

>>> Reporter.objects.filter(article__reporter__first_name__startswith="John")
(0.002) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") INNER JOIN "myapp_reporter" T3 ON ("myapp_article"."reporter_id" = T3."id") WHERE T3."first_name" LIKE 'John%' ESCAPE '\' LIMIT 21; args=('John%',); alias=default
<QuerySet [<Reporter: John Smith>, <Reporter: John Smith>]>
>>> Reporter.objects.filter(article__reporter__first_name__startswith="John").distinct()
(0.001) SELECT DISTINCT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") INNER JOIN "myapp_reporter" T3 ON ("myapp_article"."reporter_id" = T3."id") WHERE T3."first_name" LIKE 'John%' ESCAPE '\' LIMIT 21; args=('John%',); alias=default
<QuerySet [<Reporter: John Smith>]>
>>> Reporter.objects.filter(article__reporter=r).distinct()
(0.002) SELECT DISTINCT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."reporter_id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Reporter: John Smith>]>
>>>

>>> Article.objects.all()
(0.002) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
>>> Reporter.objects.order_by("first_name")
(0.001) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" ORDER BY "myapp_reporter"."first_name" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Reporter: John Smith>, <Reporter: Paul Jones>]>
>>> r2.delete()
(0.000) BEGIN; args=None; alias=default
(0.009) DELETE FROM "myapp_article" WHERE "myapp_article"."reporter_id" IN (2); args=(2,); alias=default
(0.002) DELETE FROM "myapp_reporter" WHERE "myapp_reporter"."id" IN (2); args=(2,); alias=default
(0.006) COMMIT; args=None; alias=default
(2, {'myapp.Article': 1, 'myapp.Reporter': 1})
>>> Article.objects.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Article: John's second story>, <Article: This is a test>]>
>>> Reporter.objects.order_by("first_name")
(0.002) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" ORDER BY "myapp_reporter"."first_name" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Reporter: John Smith>]>
>>>

>>> Reporter.objects.filter(article__headline__startswith="This").delete()
(0.002) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" INNER JOIN "myapp_article" ON ("myapp_reporter"."id" = "myapp_article"."reporter_id") WHERE "myapp_article"."headline" LIKE 'This%' ESCAPE '\'; args=('This%',); alias=default
(0.000) BEGIN; args=None; alias=default
(0.009) DELETE FROM "myapp_article" WHERE "myapp_article"."reporter_id" IN (1); args=(1,); alias=default
(0.002) DELETE FROM "myapp_reporter" WHERE "myapp_reporter"."id" IN (1); args=(1,); alias=default
(0.006) COMMIT; args=None; alias=default
(3, {'myapp.Article': 2, 'myapp.Reporter': 1})
>>> Reporter.objects.all()
(0.003) SELECT "myapp_reporter"."id", "myapp_reporter"."first_name", "myapp_reporter"."last_name", "myapp_reporter"."email" FROM "myapp_reporter" LIMIT 21; args=(); alias=default
<QuerySet []>
>>> Article.objects.all()
(0.003) SELECT "myapp_article"."id", "myapp_article"."headline", "myapp_article"."pub_date", "myapp_article"."reporter_id" FROM "myapp_article" ORDER BY "myapp_article"."headline" ASC LIMIT 21; args=(); alias=default
<QuerySet []>
>>>

```

## [One-to-one relationships](https://docs.djangoproject.com/en/4.2/topics/db/examples/one_to_one/)

```python
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)

"""
CREATE TABLE "myapp_place" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL,
    "address" varchar(80) NOT NULL
)

CREATE TABLE "myapp_restaurant" (
    "place_id" bigint NOT NULL PRIMARY KEY REFERENCES "myapp_place" ("id") DEFERRABLE INITIALLY DEFERRED,
    "serves_hot_dogs" bool NOT NULL,
    "serves_pizza" bool NOT NULL
)

CREATE TABLE "myapp_waiter" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL,
    "restaurant_id" bigint NOT NULL REFERENCES "myapp_restaurant" ("place_id") DEFERRABLE INITIALLY DEFERRED
)
"""

```

```bash
root@3ba3f34d6e40:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from myapp.models import Place, Restaurant, Waiter
>>>
>>> p1 = Place(name="Demon Dogs", address="944 W. Fullerton")
>>> p1.save()
(0.020) INSERT INTO "myapp_place" ("name", "address") VALUES ('Demon Dogs', '944 W. Fullerton'); args=['Demon Dogs', '944 W. Fullerton']; alias=default
>>> p2 = Place(name="Ace Hardware", address="1013 N. Ashland")
>>> p2.save()
(0.016) INSERT INTO "myapp_place" ("name", "address") VALUES ('Ace Hardware', '1013 N. Ashland'); args=['Ace Hardware', '1013 N. Ashland']; alias=default
>>>
>>> r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
>>> r.save()
(0.004) UPDATE "myapp_restaurant" SET "serves_hot_dogs" = 1, "serves_pizza" = 0 WHERE "myapp_restaurant"."place_id" = 1; args=(True, False, 1); alias=default
(0.017) INSERT INTO "myapp_restaurant" ("place_id", "serves_hot_dogs", "serves_pizza") VALUES (1, 1, 0); args=(1, True, False); alias=default
>>>

>>> dir(Place)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'address', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'restaurant', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>> dir(p1)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'address',
    'adelete',
    'arefresh_from_db',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'id',
    'name',
    'objects',
    'pk',
    'prepare_database_save',
    'refresh_from_db',
    'restaurant',
    'save',
    'save_base',
    'serializable_value',
    'unique_error_message',
    'validate_constraints',
    'validate_unique'
]
>>> dir(Restaurant)
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'objects', 'pk', 'place', 'place_id', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'serves_hot_dogs', 'serves_pizza', 'unique_error_message', 'validate_constraints', 'validate_unique', 'waiter_set']
>>> dir(r)
[
    'DoesNotExist',
    'MultipleObjectsReturned',
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_check_column_name_clashes',
    '_check_constraints',
    '_check_db_table_comment',
    '_check_default_pk',
    '_check_field_name_clashes',
    '_check_fields',
    '_check_id_field',
    '_check_index_together',
    '_check_indexes',
    '_check_local_fields',
    '_check_long_column_names',
    '_check_m2m_through_same_relationship',
    '_check_managers',
    '_check_model',
    '_check_model_name_db_lookup_clashes',
    '_check_ordering',
    '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key',
    '_check_swappable',
    '_check_unique_together',
    '_do_insert',
    '_do_update',
    '_get_FIELD_display',
    '_get_expr_references',
    '_get_field_value_map',
    '_get_next_or_previous_by_FIELD',
    '_get_next_or_previous_in_order',
    '_get_pk_val',
    '_get_unique_checks',
    '_meta',
    '_perform_date_checks',
    '_perform_unique_checks',
    '_prepare_related_fields_for_save',
    '_save_parents',
    '_save_table',
    '_set_pk_val',
    '_state',  # 多了这个属性
    'adelete',
    'arefresh_from_db',
    'asave',
    'check',
    'clean',
    'clean_fields',
    'date_error_message',
    'delete',
    'from_db',
    'full_clean',
    'get_constraints',
    'get_deferred_fields',
    'objects',
    'pk',
    'place',
    'place_id',
    'prepare_database_save',
    'refresh_from_db',
    'save',
    'save_base',
    'serializable_value',
    'serves_hot_dogs',
    'serves_pizza',
    'unique_error_message',
    'validate_constraints',
    'validate_unique',
    'waiter_set'
]
>>>

>>> r.place
<Place: Demon Dogs the place>
>>>
>>> p1.restaurant
<Restaurant: Demon Dogs the restaurant>
>>>

>>> p2.restaurant
(0.004) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" = 2 LIMIT 21; args=(2,); alias=default
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/fields/related_descriptors.py", line 492, in __get__
    raise self.RelatedObjectDoesNotExist(
myapp.models.Place.restaurant.RelatedObjectDoesNotExist: Place has no restaurant.
>>>

>>> hasattr(p2, "restaurant")
False
>>> hasattr(p1, "restaurant")
True
>>>

>>> r.place = p2
>>> r.save()
(0.001) UPDATE "myapp_restaurant" SET "serves_hot_dogs" = 1, "serves_pizza" = 0 WHERE "myapp_restaurant"."place_id" = 2; args=(True, False, 2); alias=default
(0.013) INSERT INTO "myapp_restaurant" ("place_id", "serves_hot_dogs", "serves_pizza") VALUES (2, 1, 0); args=(2, True, False); alias=default
>>> p2.restaurant
<Restaurant: Ace Hardware the restaurant>
>>> r.place
<Place: Ace Hardware the place>
>>>

>>> p1.restaurant = r
>>> p1.restaurant
<Restaurant: Demon Dogs the restaurant>
>>>

>>> p3 = Place(name="Demon Dogs", address="944 W. Fullerton")
>>> Restaurant.objects.create(place=p3, serves_hot_dogs=True, serves_pizza=False)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/base.py", line 778, in save
    self._prepare_related_fields_for_save(operation_name="save")
  File "/usr/local/lib/python3.10/site-packages/django/db/models/base.py", line 1093, in _prepare_related_fields_for_save
    raise ValueError(
ValueError: save() prohibited to prevent data loss due to unsaved related object 'place'.
>>>

>>> Restaurant.objects.all()
(0.004) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" LIMIT 21; args=(); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 2 LIMIT 21; args=(2,); alias=default
<QuerySet [<Restaurant: Demon Dogs the restaurant>, <Restaurant: Ace Hardware the restaurant>]>
>>>
>>> Place.objects.order_by("name")
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" ORDER BY "myapp_place"."name" ASC LIMIT 21; args=(); alias=default
<QuerySet [<Place: Ace Hardware the place>, <Place: Demon Dogs the place>]>
>>>

>>> Restaurant.objects.get(place=p1)
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<Restaurant: Demon Dogs the restaurant>
>>> Restaurant.objects.get(place__pk=1)
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<Restaurant: Demon Dogs the restaurant>
>>> Restaurant.objects.filter(place__name__startswith="Demon")
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_id" = "myapp_place"."id") WHERE "myapp_place"."name" LIKE 'Demon%' ESCAPE '\' LIMIT 21; args=('Demon%',); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Restaurant: Demon Dogs the restaurant>]>
>>> Restaurant.objects.exclude(place__address__contains="Ashland")
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_id" = "myapp_place"."id") WHERE NOT ("myapp_place"."address" LIKE '%Ashland%' ESCAPE '\') LIMIT 21; args=('%Ashland%',); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Restaurant: Demon Dogs the restaurant>]>
>>> Place.objects.get(pk=1)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant__place=p1)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" INNER JOIN "myapp_restaurant" ON ("myapp_place"."id" = "myapp_restaurant"."place_id") WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant=r)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" INNER JOIN "myapp_restaurant" ON ("myapp_place"."id" = "myapp_restaurant"."place_id") WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant__place__name__startswith="Demon")
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" INNER JOIN "myapp_restaurant" ON ("myapp_place"."id" = "myapp_restaurant"."place_id") INNER JOIN "myapp_place" T3 ON ("myapp_restaurant"."place_id" = T3."id") WHERE T3."name" LIKE 'Demon%' ESCAPE '\' LIMIT 21; args=('Demon%',); alias=default
<Place: Demon Dogs the place>
>>>

>>> p2.delete()
(0.002) SELECT "myapp_restaurant"."place_id" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" IN (2); args=(2,); alias=default
(0.000) BEGIN; args=None; alias=default
(0.003) DELETE FROM "myapp_waiter" WHERE "myapp_waiter"."restaurant_id" IN (2); args=(2,); alias=default
(0.008) DELETE FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" IN (2); args=(2,); alias=default
(0.003) DELETE FROM "myapp_place" WHERE "myapp_place"."id" IN (2); args=(2,); alias=default
(0.006) COMMIT; args=None; alias=default
(2, {'myapp.Restaurant': 1, 'myapp.Place': 1})
>>> Restaurant.objects.all()
(0.003) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" LIMIT 21; args=(); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Restaurant: Demon Dogs the restaurant>]>
>>>

>>> w = r.waiter_set.create(name="Joe")
(0.018) INSERT INTO "myapp_waiter" ("restaurant_id", "name") VALUES (1, 'Joe'); args=[1, 'Joe']; alias=default
>>> w
<Waiter: Joe the waiter at Demon Dogs the restaurant>
>>> Waiter.objects.filter(restaurant__place=p1)
(0.003) SELECT "myapp_waiter"."id", "myapp_waiter"."restaurant_id", "myapp_waiter"."name" FROM "myapp_waiter" WHERE "myapp_waiter"."restaurant_id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
>>> Waiter.objects.filter(restaurant__place__name__startswith="Demon")
(0.002) SELECT "myapp_waiter"."id", "myapp_waiter"."restaurant_id", "myapp_waiter"."name" FROM "myapp_waiter" INNER JOIN "myapp_restaurant" ON ("myapp_waiter"."restaurant_id" = "myapp_restaurant"."place_id") INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_id" = "myapp_place"."id") WHERE "myapp_place"."name" LIKE 'Demon%' ESCAPE '\' LIMIT 21; args=('Demon%',); alias=default
(0.001) SELECT "myapp_restaurant"."place_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" WHERE "myapp_restaurant"."place_id" = 1 LIMIT 21; args=(1,); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" WHERE "myapp_place"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
>>>

```
