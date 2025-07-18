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

## [Making queries](https://docs.djangoproject.com/en/4.2/topics/db/queries/)


```python
from datetime import date

from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="related_name_blog",  # default: entry_set
        related_query_name="related_query_name_blog"  # default: entry
    )
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline

```

```bash
root@0374edb82005:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>> from myapp.models import Blog, Author, Entry
>>>

from datetime import date
beatles = Blog.objects.create(name='Beatles Blog')
pop = Blog.objects.create(name='Pop Music Blog')
Entry.objects.create(blog=beatles, headline='New Lennon Biography', pub_date=date(2008, 6, 1))
Entry.objects.create(blog=beatles, headline='New Lennon Biography in Paperback', pub_date=date(2009, 6, 1))
Entry.objects.create(blog=pop, headline='Best Albums of 2008', pub_date=date(2008, 12, 15))
Entry.objects.create(blog=pop, headline='Lennon Would Have Loved Hip Hop', pub_date=date(2020, 4, 1))

>>> Entry.objects.filter(blog__name=beatles)
(0.001) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 21; args=('Beatles Blog',); alias=default
<QuerySet [<Entry: New Lennon Biography>, <Entry: New Lennon Biography in Paperback>]>

>>> q1 = Entry.objects.filter(blog__name=beatles)
>>> q1
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 21; args=('Beatles Blog',); alias=default
<QuerySet [<Entry: New Lennon Biography>, <Entry: New Lennon Biography in Paperback>]>
>>> q1[0]
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 1; args=('Beatles Blog',); alias=default
<Entry: New Lennon Biography>
>>> q1[0].headline
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 1; args=('Beatles Blog',); alias=default
'New Lennon Biography'
>>> q1[0].blog.name
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 1; args=('Beatles Blog',); alias=default
(0.001) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" WHERE "myapp_blog"."id" = 5 LIMIT 21; args=(5,); alias=default
'Beatles Blog'
>>>
>>> type(q1[0])
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 1; args=('Beatles Blog',); alias=default
<class 'myapp.models.Entry'>
>>> type(q1[0].blog)
(0.002) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE "myapp_blog"."name" = 'Beatles Blog' LIMIT 1; args=('Beatles Blog',); alias=default
(0.001) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" WHERE "myapp_blog"."id" = 5 LIMIT 21; args=(5,); alias=default
<class 'myapp.models.Blog'>
>>>

# related_query_name="related_query_name_blog"
# 将 entry 替换为 related_query_name_blog
>>> Blog.objects.filter(entry__headline="Best Albums of 2008")
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 21; args=('Best Albums of 2008',); alias=default
<QuerySet [<Blog: Pop Music Blog>]>
>>> q2 = Blog.objects.filter(entry__headline="Best Albums of 2008")
>>> q2
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 21; args=('Best Albums of 2008',); alias=default
<QuerySet [<Blog: Pop Music Blog>]>
>>> q2[0]
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 1; args=('Best Albums of 2008',); alias=default
<Blog: Pop Music Blog>
>>> type(q2[0])
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 1; args=('Best Albums of 2008',); alias=default
<class 'myapp.models.Blog'>
>>> dir(q2[0])
(0.003) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 1; args=('Best Albums of 2008',); alias=default
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'entry_set', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'tagline', 'unique_error_message', 'validate_constraints', 'validate_unique']

# related_name="related_name_blog"
# 将 entry_set 替换为 related_name_blog
>>> type(q2[0].entry_set)
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 1; args=('Best Albums of 2008',); alias=default
<class 'django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager'>
>>> q2[0].entry_set.filter(blog__name=beatles)
(0.002) SELECT "myapp_blog"."id", "myapp_blog"."name", "myapp_blog"."tagline" FROM "myapp_blog" INNER JOIN "myapp_entry" ON ("myapp_blog"."id" = "myapp_entry"."blog_id") WHERE "myapp_entry"."headline" = 'Best Albums of 2008' LIMIT 1; args=('Best Albums of 2008',); alias=default
(0.001) SELECT "myapp_entry"."id", "myapp_entry"."blog_id", "myapp_entry"."headline", "myapp_entry"."body_text", "myapp_entry"."pub_date", "myapp_entry"."mod_date", "myapp_entry"."number_of_comments", "myapp_entry"."number_of_pingbacks", "myapp_entry"."rating" FROM "myapp_entry" INNER JOIN "myapp_blog" ON ("myapp_entry"."blog_id" = "myapp_blog"."id") WHERE ("myapp_entry"."blog_id" = 6 AND "myapp_blog"."name" = 'Beatles Blog') LIMIT 21; args=(6, 'Beatles Blog'); alias=default
<QuerySet []>
>>>

```



## [multi-table-inheritance](https://docs.djangoproject.com/en/4.2/topics/db/models/#multi-table-inheritance)

```python
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

```bash
root@8925f1ab9350:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from myapp.models import Place, Restaurant
>>>
>>> p = Place.objects.create(name="name1", address="address1")
(0.016) INSERT INTO "myapp_place" ("name", "address") VALUES ('name1', 'address1'); args=['name1', 'address1']; alias=default
>>> r = Restaurant.objects.create(name="name2", address="address2")
(0.000) BEGIN; args=None; alias=default
(0.013) INSERT INTO "myapp_place" ("name", "address") VALUES ('name2', 'address2'); args=['name2', 'address2']; alias=default
(0.006) INSERT INTO "myapp_restaurant" ("place_ptr_id", "serves_hot_dogs", "serves_pizza") VALUES (2, 0, 0); args=(2, False, False); alias=default
(0.008) COMMIT; args=None; alias=default
>>>

>>> Restaurant.objects.all()
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 21; args=(); alias=default
<QuerySet [<Restaurant: Restaurant object (2)>]>
>>> r = Restaurant.objects.all()
>>> r
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 21; args=(); alias=default
<QuerySet [<Restaurant: Restaurant object (2)>]>
>>> r[0]
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
<Restaurant: Restaurant object (2)>
>>> type(r[0])
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
<class 'myapp.models.Restaurant'>
>>> dir(r[0])
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'address', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'place_ptr', 'place_ptr_id', 'prepare_database_save', 'refresh_from_db', 'restaurant', 'save', 'save_base', 'serializable_value', 'serves_hot_dogs', 'serves_pizza', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>> type(r[0].place_ptr)
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
<class 'myapp.models.Place'>
>>> type(r[0].place_ptr_id)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
<class 'int'>
>>> type(r[0].restaurant)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") LIMIT 1; args=(); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") WHERE "myapp_restaurant"."place_ptr_id" = 2 LIMIT 21; args=(2,); alias=default
<class 'myapp.models.Restaurant'>
>>>

>>> Place.objects.all()
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 21; args=(); alias=default
<QuerySet [<Place: Place object (1)>, <Place: Place object (2)>]>
>>> p = Place.objects.all()
>>> p[0]
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1; args=(); alias=default
<Place: Place object (1)>
>>> p[1]
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1 OFFSET 1; args=(); alias=default
<Place: Place object (2)>
>>> type(p[0])
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1; args=(); alias=default
<class 'myapp.models.Place'>
>>> type(p[1])
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1 OFFSET 1; args=(); alias=default
<class 'myapp.models.Place'>
>>> dir(p[0])
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1; args=(); alias=default
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'address', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'restaurant', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>> dir(p[1])
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1 OFFSET 1; args=(); alias=default
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 'address', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'restaurant', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
>>>
>>> type(p[0].restaurant)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1; args=(); alias=default
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") WHERE "myapp_restaurant"."place_ptr_id" = 1 LIMIT 21; args=(1,); alias=default
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/fields/related_descriptors.py", line 492, in __get__
    raise self.RelatedObjectDoesNotExist(
myapp.models.Place.restaurant.RelatedObjectDoesNotExist: Place has no restaurant.
>>> type(p[1].restaurant)
(0.001) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address" FROM "myapp_place" LIMIT 1 OFFSET 1; args=(); alias=default
(0.002) SELECT "myapp_place"."id", "myapp_place"."name", "myapp_place"."address", "myapp_restaurant"."place_ptr_id", "myapp_restaurant"."serves_hot_dogs", "myapp_restaurant"."serves_pizza" FROM "myapp_restaurant" INNER JOIN "myapp_place" ON ("myapp_restaurant"."place_ptr_id" = "myapp_place"."id") WHERE "myapp_restaurant"."place_ptr_id" = 2 LIMIT 21; args=(2,); alias=default
<class 'myapp.models.Restaurant'>
>>>

```

## [Aggregation](https://docs.djangoproject.com/en/4.2/topics/db/aggregation/)

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

```

```bash

root@bc7ca7b801c7:/django-tutorial-4.2/mysite# python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.18 (main, Jul  1 2025, 05:26:33) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

from datetime import datetime
import random
from faker import Faker
from myapp.models import Author, Publisher, Book, Store


fake = Faker()

authors = []
today = datetime.today()
for _ in range(300):
    birth_date = fake.date_of_birth()
    author = Author.objects.create(
        name=fake.name(),
        age=today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    authors.append(author)


publisher = []
for _ in range(100):
    publisher.append(Publisher.objects.create(
        name=fake.company()
    ))

books = []
for _ in range(600):
    num_words = fake.random_int(min=2, max=5)
    title = ' '.join(fake.words(nb=num_words)).title()
    book = Book.objects.create(
        name=title,
        pages=fake.random_int(min=120, max=500),
        price=fake.pyfloat(right_digits=2, positive=True, min_value=1.0, max_value=2000.0),
        rating=fake.random_int(min=1, max=10),
        #authors=random.sample(authors, fake.random_int(min=1, max=5)),
        publisher=publisher[fake.random_int(min=0, max=len(publisher)-1)],
        pubdate=fake.date_of_birth()
    )
    book.authors.set(random.sample(authors, fake.random_int(min=1, max=5)))
    books.append(book)

for _ in range(30):
    store = Store.objects.create(
        name=fake.company()
    )
    store.books.set(random.sample(books, fake.random_int(min=1, max=len(books)-100)))


>>> Book.objects.count()
(0.004) SELECT COUNT(*) AS "__count" FROM "myapp_book"; args=(); alias=default
600
>>>
>>> Book.objects.filter(publisher__name="Proctor-Beard").count()
(0.001) SELECT COUNT(*) AS "__count" FROM "myapp_book" INNER JOIN "myapp_publisher" ON ("myapp_book"."publisher_id" = "myapp_publisher"."id") WHERE "myapp_publisher"."name" = 'Proctor-Beard'; args=('Proctor-Beard',); alias=default
5

SELECT COUNT(*) AS "__count"
FROM "myapp_book"
INNER JOIN "myapp_publisher"
ON ("myapp_book"."publisher_id" = "myapp_publisher"."id")
WHERE "myapp_publisher"."name" = 'Proctor-Beard'

>>>

>>> from django.db.models import Avg
>>> Book.objects.aggregate(Avg("price", default=0))
(0.002) SELECT CAST(COALESCE(CAST(AVG("myapp_book"."price") AS NUMERIC), CAST('0' AS NUMERIC)) AS NUMERIC) AS "price__avg" FROM "myapp_book"; args=(Decimal('0'),); alias=default
{'price__avg': Decimal('990.719616666667')}

SELECT CAST(
    COALESCE(
        CAST(
            AVG("myapp_book"."price") AS NUMERIC
        ),
        CAST('0' AS NUMERIC)
    ) AS NUMERIC
) AS "price__avg"
FROM "myapp_book"

FROM "myapp_book"
含义：指定查询的目标数据表是 myapp_book。

AVG("myapp_book"."price")
含义：这是查询的核心计算。AVG() 是一个聚合函数，用于计算 price 列中所有值的平均数。

CAST(...) AS NUMERIC)
含义：CAST 是一个类型转换函数。这里，它将 AVG() 函数的计算结果显式地转换为 NUMERIC (或 DECIMAL) 数据类型。
目的：这样做是为了保证数值的精度，尤其在处理像价格这样的货币数据时。AVG 的结果可能是浮点数，将其转换为 NUMERIC 可以避免潜在的浮点数精度问题。

COALESCE(..., ...)
含义：COALESCE 函数接受一个参数列表，并返回其中第一个非 NULL 的值。这是这条语句中非常关键的一步。
第一个参数：CAST(AVG(...) AS NUMERIC)，即我们刚刚计算出的平均价格。
第二个参数：CAST('0' AS NUMERIC)，即将字符 '0' 转换为 NUMERIC 类型的 0。
目的：这是一个健壮性设计。如果 myapp_book 表是空的（没有任何行），AVG("price") 的计算结果将是 NULL。COALESCE 函数会检测到这个 NULL 值，并返回它的下一个参数，也就是 0。这样就确保了查询总能返回一个有效的数值，而不是 NULL。

CAST(...) AS NUMERIC (最外层)
含义：将 COALESCE 函数的最终结果再次转换为 NUMERIC 类型。
目的：在多数情况下，这一步是冗余的，因为 COALESCE 的两个可能输入值都已经事先被转换成了 NUMERIC 类型。然而，ORM为了保证在任何数据库后端和任何分支逻辑下都能得到绝对确定的数据类型，常常会生成这样“以防万一”的冗余代码。

AS "price__avg"
含义：为最终计算出的结果列指定一个别名（alias），名为 price__avg。在查询结果中，这一列的列名就会是 price__avg。
命名约定：这种 field__agg (字段名__聚合函数名) 的命名方式是Django ORM的典型特征。

>>>
>>> from django.db.models import Max
>>> Book.objects.aggregate(Max("price", default=0))
(0.001) SELECT CAST(COALESCE(CAST(MAX("myapp_book"."price") AS NUMERIC), CAST('0' AS NUMERIC)) AS NUMERIC) AS "price__max" FROM "myapp_book"; args=(Decimal('0'),); alias=default
{'price__max': Decimal('1999.81000000000')}

SELECT CAST(
    COALESCE(
        CAST(
            MAX("myapp_book"."price") AS NUMERIC
        ),
        CAST('0' AS NUMERIC)
    ) AS NUMERIC
) AS "price__max"
FROM "myapp_book"
>>>

>>> from django.db.models import FloatField
>>> Book.objects.aggregate(price_diff=Max("price") - Avg("price"))
(0.002) SELECT CAST((CAST(MAX("myapp_book"."price") AS NUMERIC) - CAST(AVG("myapp_book"."price") AS NUMERIC)) AS NUMERIC) AS "price_diff" FROM "myapp_book"; args=(); alias=default
{'price_diff': Decimal('1009.09038333333')}
>>>
>>> Book.objects.aggregate(price_diff=Max("price", output_field=FloatField()) - Avg("price", output_field=FloatField()))
(0.002) SELECT (MAX("myapp_book"."price") - AVG("myapp_book"."price")) AS "price_diff" FROM "myapp_book"; args=(); alias=default
{'price_diff': 1009.0903833333329}
>>>

SELECT CAST(
    (
        CAST(
            MAX("myapp_book"."price") AS NUMERIC
        )
        -
        CAST(
            AVG("myapp_book"."price") AS NUMERIC
        )
    ) AS NUMERIC
) AS "price_diff"
FROM "myapp_book"

SELECT (
    MAX("myapp_book"."price") - AVG("myapp_book"."price")
) AS "price_diff"
FROM "myapp_book"

>>> from django.db.models import Count
>>> Publisher.objects.annotate(num_books=Count("book"))
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 21; args=(); alias=default
<QuerySet [<Publisher: Publisher object (1)>, <Publisher: Publisher object (2)>, <Publisher: Publisher object (3)>, <Publisher: Publisher object (4)>, <Publisher: Publisher object (5)>, <Publisher: Publisher object (6)>, <Publisher: Publisher object (7)>, <Publisher: Publisher object (8)>, <Publisher: Publisher object (9)>, <Publisher: Publisher object (10)>, <Publisher: Publisher object (11)>, <Publisher: Publisher object (12)>, <Publisher: Publisher object (13)>, <Publisher: Publisher object (14)>, <Publisher: Publisher object (15)>, <Publisher: Publisher object (16)>, <Publisher: Publisher object (17)>, <Publisher: Publisher object (18)>, <Publisher: Publisher object (19)>, <Publisher: Publisher object (20)>, '...(remaining elements truncated)...']>
>>> pubs = Publisher.objects.annotate(num_books=Count("book"))
>>> pubs
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 21; args=(); alias=default
<QuerySet [<Publisher: Publisher object (1)>, <Publisher: Publisher object (2)>, <Publisher: Publisher object (3)>, <Publisher: Publisher object (4)>, <Publisher: Publisher object (5)>, <Publisher: Publisher object (6)>, <Publisher: Publisher object (7)>, <Publisher: Publisher object (8)>, <Publisher: Publisher object (9)>, <Publisher: Publisher object (10)>, <Publisher: Publisher object (11)>, <Publisher: Publisher object (12)>, <Publisher: Publisher object (13)>, <Publisher: Publisher object (14)>, <Publisher: Publisher object (15)>, <Publisher: Publisher object (16)>, <Publisher: Publisher object (17)>, <Publisher: Publisher object (18)>, <Publisher: Publisher object (19)>, <Publisher: Publisher object (20)>, '...(remaining elements truncated)...']>
>>> pubs[0].num_books
(0.007) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1; args=(); alias=default
6
>>> pubs[1].num_books
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1 OFFSET 1; args=(); alias=default
4

SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books"
FROM "myapp_publisher"
LEFT OUTER JOIN "myapp_book"
ON ("myapp_publisher"."id" = "myapp_book"."publisher_id")
GROUP BY "myapp_publisher"."id", "myapp_publisher"."name"
LIMIT 21

>>>
>>> from django.db.models import Q
>>> above_5 = Count("book", filter=Q(book__rating__gt=5))
>>> above_5
Count(F(book), filter=(AND: ('book__rating__gt', 5)))
>>> below_5 = Count("book", filter=Q(book__rating__lte=5))
>>> below_5
Count(F(book), filter=(AND: ('book__rating__lte', 5)))
>>> Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 21; args=(5.0, 5.0); alias=default
<QuerySet [<Publisher: Publisher object (1)>, <Publisher: Publisher object (2)>, <Publisher: Publisher object (3)>, <Publisher: Publisher object (4)>, <Publisher: Publisher object (5)>, <Publisher: Publisher object (6)>, <Publisher: Publisher object (7)>, <Publisher: Publisher object (8)>, <Publisher: Publisher object (9)>, <Publisher: Publisher object (10)>, <Publisher: Publisher object (11)>, <Publisher: Publisher object (12)>, <Publisher: Publisher object (13)>, <Publisher: Publisher object (14)>, <Publisher: Publisher object (15)>, <Publisher: Publisher object (16)>, <Publisher: Publisher object (17)>, <Publisher: Publisher object (18)>, <Publisher: Publisher object (19)>, <Publisher: Publisher object (20)>, '...(remaining elements truncated)...']>
>>> pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
>>>
>>> pubs[0].above_5
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1; args=(5.0, 5.0); alias=default
1
>>> pubs[0].below_5
(0.001) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1; args=(5.0, 5.0); alias=default
5
>>> pubs[1].above_5
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1 OFFSET 1; args=(5.0, 5.0); alias=default
0
>>> pubs[1].below_5
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5", COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 1 OFFSET 1; args=(5.0, 5.0); alias=default
4

SELECT
    "myapp_publisher"."id",
    "myapp_publisher"."name",
    COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" <= 5.0) AS "below_5",
    COUNT("myapp_book"."id") FILTER (WHERE "myapp_book"."rating" > 5.0) AS "above_5"
FROM "myapp_publisher"
LEFT OUTER JOIN "myapp_book"
ON ("myapp_publisher"."id" = "myapp_book"."publisher_id")
GROUP BY "myapp_publisher"."id", "myapp_publisher"."name"
LIMIT 21
>>>

>>> Publisher.objects.annotate(num_books=Count("book"))
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" LIMIT 21; args=(); alias=default
<QuerySet [<Publisher: Publisher object (1)>, <Publisher: Publisher object (2)>, <Publisher: Publisher object (3)>, <Publisher: Publisher object (4)>, <Publisher: Publisher object (5)>, <Publisher: Publisher object (6)>, <Publisher: Publisher object (7)>, <Publisher: Publisher object (8)>, <Publisher: Publisher object (9)>, <Publisher: Publisher object (10)>, <Publisher: Publisher object (11)>, <Publisher: Publisher object (12)>, <Publisher: Publisher object (13)>, <Publisher: Publisher object (14)>, <Publisher: Publisher object (15)>, <Publisher: Publisher object (16)>, <Publisher: Publisher object (17)>, <Publisher: Publisher object (18)>, <Publisher: Publisher object (19)>, <Publisher: Publisher object (20)>, '...(remaining elements truncated)...']>
>>> Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" ORDER BY 3 DESC LIMIT 21; args=(); alias=default
<QuerySet [<Publisher: Publisher object (19)>, <Publisher: Publisher object (98)>, <Publisher: Publisher object (32)>, <Publisher: Publisher object (45)>, <Publisher: Publisher object (74)>, <Publisher: Publisher object (15)>, <Publisher: Publisher object (43)>, <Publisher: Publisher object (90)>, <Publisher: Publisher object (91)>, <Publisher: Publisher object (99)>, <Publisher: Publisher object (5)>, <Publisher: Publisher object (8)>, <Publisher: Publisher object (14)>, <Publisher: Publisher object (23)>, <Publisher: Publisher object (39)>, <Publisher: Publisher object (55)>, <Publisher: Publisher object (73)>, <Publisher: Publisher object (77)>, <Publisher: Publisher object (79)>, <Publisher: Publisher object (84)>, '...(remaining elements truncated)...']>
>>> Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")[:5]
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" ORDER BY 3 DESC LIMIT 5; args=(); alias=default
<QuerySet [<Publisher: Publisher object (19)>, <Publisher: Publisher object (98)>, <Publisher: Publisher object (32)>, <Publisher: Publisher object (45)>, <Publisher: Publisher object (74)>]>
>>> pubs = Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")[:5]
>>> pubs[0].num_books
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" ORDER BY 3 DESC LIMIT 1; args=(); alias=default
12
>>> pubs[1].num_books
(0.002) SELECT "myapp_publisher"."id", "myapp_publisher"."name", COUNT("myapp_book"."id") AS "num_books" FROM "myapp_publisher" LEFT OUTER JOIN "myapp_book" ON ("myapp_publisher"."id" = "myapp_book"."publisher_id") GROUP BY "myapp_publisher"."id", "myapp_publisher"."name" ORDER BY 3 DESC LIMIT 1 OFFSET 1; args=(); alias=default
11

SELECT
    "myapp_publisher"."id",
    "myapp_publisher"."name",
    COUNT("myapp_book"."id") AS "num_books"
FROM "myapp_publisher"
LEFT OUTER JOIN "myapp_book"
ON ("myapp_publisher"."id" = "myapp_book"."publisher_id")
GROUP BY "myapp_publisher"."id", "myapp_publisher"."name"
LIMIT 21

SELECT
    "myapp_publisher"."id",
    "myapp_publisher"."name",
    COUNT("myapp_book"."id") AS "num_books"
FROM "myapp_publisher"
LEFT OUTER JOIN "myapp_book"
ON ("myapp_publisher"."id" = "myapp_book"."publisher_id")
GROUP BY "myapp_publisher"."id", "myapp_publisher"."name"
ORDER BY 3 DESC
LIMIT 21

SELECT
    "myapp_publisher"."id",
    "myapp_publisher"."name",
    COUNT("myapp_book"."id") AS "num_books"
FROM "myapp_publisher"
LEFT OUTER JOIN "myapp_book"
ON ("myapp_publisher"."id" = "myapp_book"."publisher_id")
GROUP BY "myapp_publisher"."id", "myapp_publisher"."name"
ORDER BY 3 DESC
LIMIT 5
>>>

>>> from django.db.models import Count
>>> Book.objects.annotate(Count("authors"))
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(); alias=default
<QuerySet [<Book: Book object (6)>, <Book: Book object (17)>, <Book: Book object (25)>, <Book: Book object (98)>, <Book: Book object (138)>, <Book: Book object (201)>, <Book: Book object (257)>, <Book: Book object (330)>, <Book: Book object (464)>, <Book: Book object (507)>, <Book: Book object (50)>, <Book: Book object (419)>, <Book: Book object (558)>, <Book: Book object (66)>, <Book: Book object (166)>, <Book: Book object (381)>, <Book: Book object (424)>, <Book: Book object (431)>, <Book: Book object (592)>, <Book: Book object (55)>, '...(remaining elements truncated)...']>
>>> q = Book.objects.annotate(Count("authors"))
>>> q
(0.001) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(); alias=default
<QuerySet [<Book: Book object (6)>, <Book: Book object (17)>, <Book: Book object (25)>, <Book: Book object (98)>, <Book: Book object (138)>, <Book: Book object (201)>, <Book: Book object (257)>, <Book: Book object (330)>, <Book: Book object (464)>, <Book: Book object (507)>, <Book: Book object (50)>, <Book: Book object (419)>, <Book: Book object (558)>, <Book: Book object (66)>, <Book: Book object (166)>, <Book: Book object (381)>, <Book: Book object (424)>, <Book: Book object (431)>, <Book: Book object (592)>, <Book: Book object (55)>, '...(remaining elements truncated)...']>
>>> q[0]
(0.001) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1; args=(); alias=default
<Book: Book object (6)>
>>> q[0].authors__count
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1; args=(); alias=default
2
>>> q[1]
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1 OFFSET 1; args=(); alias=default
<Book: Book object (17)>
>>> q[1].authors__count
(0.001) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1 OFFSET 1; args=(); alias=default
3

SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate",
    COUNT("myapp_book_authors"."author_id") AS "authors__count"
FROM "myapp_book"
LEFT OUTER JOIN "myapp_book_authors"
ON ("myapp_book"."id" = "myapp_book_authors"."book_id")
GROUP BY
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
LIMIT 21

>>>

>>> from django.db.models import Count
>>> Book.objects.filter(rating__gt=5).annotate(Count("authors"))
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") WHERE "myapp_book"."rating" > 5.0 GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(5.0,); alias=default
<QuerySet [<Book: Book object (2)>, <Book: Book object (7)>, <Book: Book object (12)>, <Book: Book object (14)>, <Book: Book object (16)>, <Book: Book object (19)>, <Book: Book object (20)>, <Book: Book object (27)>, <Book: Book object (30)>, <Book: Book object (32)>, <Book: Book object (33)>, <Book: Book object (35)>, <Book: Book object (36)>, <Book: Book object (37)>, <Book: Book object (39)>, <Book: Book object (40)>, <Book: Book object (41)>, <Book: Book object (42)>, <Book: Book object (44)>, <Book: Book object (48)>, '...(remaining elements truncated)...']>

SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate",
    COUNT("myapp_book_authors"."author_id") AS "authors__count"
FROM "myapp_book"
LEFT OUTER JOIN "myapp_book_authors"
ON ("myapp_book"."id" = "myapp_book_authors"."book_id")
WHERE "myapp_book"."rating" > 5.0
GROUP BY
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
LIMIT 21

>>>

>>> Book.objects.first()
(0.001) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" FROM "myapp_book" ORDER BY "myapp_book"."id" ASC LIMIT 1; args=(); alias=default
<Book: Book object (1)>
>>> book = Book.objects.first()
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" FROM "myapp_book" ORDER BY "myapp_book"."id" ASC LIMIT 1; args=(); alias=default
>>> type(book)
<class 'myapp.models.Book'>
>>>
SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
FROM "myapp_book"
ORDER BY "myapp_book"."id" ASC
LIMIT 1

>>> book.authors.count()
(0.002) SELECT COUNT(*) AS "__count" FROM "myapp_author" INNER JOIN "myapp_book_authors" ON ("myapp_author"."id" = "myapp_book_authors"."author_id") WHERE "myapp_book_authors"."book_id" = 1; args=(1,); alias=default
3

SELECT
    COUNT(*) AS "__count"
FROM "myapp_author"
INNER JOIN "myapp_book_authors"
ON ("myapp_author"."id" = "myapp_book_authors"."author_id")
WHERE "myapp_book_authors"."book_id" = 1

>>>

>>> book.store_set.count()
(0.002) SELECT COUNT(*) AS "__count" FROM "myapp_store" INNER JOIN "myapp_store_books" ON ("myapp_store"."id" = "myapp_store_books"."store_id") WHERE "myapp_store_books"."book_id" = 1; args=(1,); alias=default
9

SELECT COUNT(*) AS "__count"
FROM "myapp_store"
INNER JOIN "myapp_store_books"
ON ("myapp_store"."id" = "myapp_store_books"."store_id")
WHERE "myapp_store_books"."book_id" = 1

>>>

>>> Book.objects.annotate(Count('authors'), Count('store'))
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count", COUNT("myapp_store_books"."store_id") AS "store__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") LEFT OUTER JOIN "myapp_store_books" ON ("myapp_book"."id" = "myapp_store_books"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(); alias=default
<QuerySet [<Book: Book object (6)>, <Book: Book object (17)>, <Book: Book object (25)>, <Book: Book object (98)>, <Book: Book object (138)>, <Book: Book object (201)>, <Book: Book object (257)>, <Book: Book object (330)>, <Book: Book object (464)>, <Book: Book object (507)>, <Book: Book object (50)>, <Book: Book object (419)>, <Book: Book object (558)>, <Book: Book object (66)>, <Book: Book object (166)>, <Book: Book object (381)>, <Book: Book object (424)>, <Book: Book object (431)>, <Book: Book object (592)>, <Book: Book object (55)>, '...(remaining elements truncated)...']>
>>> q = Book.objects.annotate(Count('authors'), Count('store'))
>>> q
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count", COUNT("myapp_store_books"."store_id") AS "store__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") LEFT OUTER JOIN "myapp_store_books" ON ("myapp_book"."id" = "myapp_store_books"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(); alias=default
<QuerySet [<Book: Book object (6)>, <Book: Book object (17)>, <Book: Book object (25)>, <Book: Book object (98)>, <Book: Book object (138)>, <Book: Book object (201)>, <Book: Book object (257)>, <Book: Book object (330)>, <Book: Book object (464)>, <Book: Book object (507)>, <Book: Book object (50)>, <Book: Book object (419)>, <Book: Book object (558)>, <Book: Book object (66)>, <Book: Book object (166)>, <Book: Book object (381)>, <Book: Book object (424)>, <Book: Book object (431)>, <Book: Book object (592)>, <Book: Book object (55)>, '...(remaining elements truncated)...']>
>>> q[0].authors__count
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count", COUNT("myapp_store_books"."store_id") AS "store__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") LEFT OUTER JOIN "myapp_store_books" ON ("myapp_book"."id" = "myapp_store_books"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1; args=(); alias=default
22
>>> q[0].store__count
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT("myapp_book_authors"."author_id") AS "authors__count", COUNT("myapp_store_books"."store_id") AS "store__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") LEFT OUTER JOIN "myapp_store_books" ON ("myapp_book"."id" = "myapp_store_books"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 1; args=(); alias=default
22
>>>

SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate",
    COUNT("myapp_book_authors"."author_id") AS "authors__count",
    COUNT("myapp_store_books"."store_id") AS "store__count"
FROM "myapp_book"
LEFT OUTER JOIN "myapp_book_authors"
ON ("myapp_book"."id" = "myapp_book_authors"."book_id")
LEFT OUTER JOIN "myapp_store_books"
ON ("myapp_book"."id" = "myapp_store_books"."book_id")
GROUP BY
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
LIMIT 21

SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate",
    COUNT("myapp_book_authors"."author_id") AS "authors__count",
    COUNT("myapp_store_books"."store_id") AS "store__count"
FROM "myapp_book"
LEFT OUTER JOIN "myapp_book_authors"
ON ("myapp_book"."id" = "myapp_book_authors"."book_id")
LEFT OUTER JOIN "myapp_store_books"
ON ("myapp_book"."id" = "myapp_store_books"."book_id")
GROUP BY
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
LIMIT 1
>>>

>>> Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
(0.002) SELECT "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate", COUNT(DISTINCT "myapp_book_authors"."author_id") AS "authors__count", COUNT(DISTINCT "myapp_store_books"."store_id") AS "store__count" FROM "myapp_book" LEFT OUTER JOIN "myapp_book_authors" ON ("myapp_book"."id" = "myapp_book_authors"."book_id") LEFT OUTER JOIN "myapp_store_books" ON ("myapp_book"."id" = "myapp_store_books"."book_id") GROUP BY "myapp_book"."id", "myapp_book"."name", "myapp_book"."pages", "myapp_book"."price", "myapp_book"."rating", "myapp_book"."publisher_id", "myapp_book"."pubdate" LIMIT 21; args=(); alias=default
<QuerySet [<Book: Book object (6)>, <Book: Book object (17)>, <Book: Book object (25)>, <Book: Book object (98)>, <Book: Book object (138)>, <Book: Book object (201)>, <Book: Book object (257)>, <Book: Book object (330)>, <Book: Book object (464)>, <Book: Book object (507)>, <Book: Book object (50)>, <Book: Book object (419)>, <Book: Book object (558)>, <Book: Book object (66)>, <Book: Book object (166)>, <Book: Book object (381)>, <Book: Book object (424)>, <Book: Book object (431)>, <Book: Book object (592)>, <Book: Book object (55)>, '...(remaining elements truncated)...']>

SELECT
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate",
    COUNT(DISTINCT "myapp_book_authors"."author_id") AS "authors__count",
    COUNT(DISTINCT "myapp_store_books"."store_id") AS "store__count"
FROM "myapp_book"
LEFT OUTER JOIN "myapp_book_authors"
ON ("myapp_book"."id" = "myapp_book_authors"."book_id")
LEFT OUTER JOIN "myapp_store_books"
ON ("myapp_book"."id" = "myapp_store_books"."book_id")
GROUP BY
    "myapp_book"."id",
    "myapp_book"."name",
    "myapp_book"."pages",
    "myapp_book"."price",
    "myapp_book"."rating",
    "myapp_book"."publisher_id",
    "myapp_book"."pubdate"
LIMIT 21

>>>

>>> from django.db.models import Max, Min
>>> Store.objects.annotate(min_price=Min("books__price"), max_price=Max("books__price"))
(0.002) SELECT "myapp_store"."id", "myapp_store"."name", CAST(MIN("myapp_book"."price") AS NUMERIC) AS "min_price", CAST(MAX("myapp_book"."price") AS NUMERIC) AS "max_price" FROM "myapp_store" LEFT OUTER JOIN "myapp_store_books" ON ("myapp_store"."id" = "myapp_store_books"."store_id") LEFT OUTER JOIN "myapp_book" ON ("myapp_store_books"."book_id" = "myapp_book"."id") GROUP BY "myapp_store"."id", "myapp_store"."name" LIMIT 21; args=(); alias=default
<QuerySet [<Store: Store object (1)>, <Store: Store object (2)>, <Store: Store object (3)>, <Store: Store object (4)>, <Store: Store object (5)>, <Store: Store object (6)>, <Store: Store object (7)>, <Store: Store object (8)>, <Store: Store object (9)>, <Store: Store object (10)>, <Store: Store object (11)>, <Store: Store object (12)>, <Store: Store object (13)>, <Store: Store object (14)>, <Store: Store object (15)>, <Store: Store object (16)>, <Store: Store object (17)>, <Store: Store object (18)>, <Store: Store object (19)>, <Store: Store object (20)>, '...(remaining elements truncated)...']>

SELECT
    "myapp_store"."id",
    "myapp_store"."name",
    CAST(
        MIN("myapp_book"."price") AS NUMERIC
    ) AS "min_price",
    CAST(
        MAX("myapp_book"."price") AS NUMERIC
    ) AS "max_price"
FROM "myapp_store"
LEFT OUTER JOIN "myapp_store_books"
ON ("myapp_store"."id" = "myapp_store_books"."store_id")
LEFT OUTER JOIN "myapp_book"
ON ("myapp_store_books"."book_id" = "myapp_book"."id")
GROUP BY
    "myapp_store"."id",
    "myapp_store"."name"
LIMIT 21

>>>

```

## [User authentication in Django](https://docs.djangoproject.com/en/4.2/topics/auth/)

```bash
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
(0.019) INSERT INTO "auth_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES ('pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=', NULL, 0, 'john', '', '', 'lennon@thebeatles.com', 0, 1, '2025-07-18 07:29:05.845970'); args=['pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=', None, False, 'john', '', '', 'lennon@thebeatles.com', False, True, '2025-07-18 07:29:05.845970']; alias=default
>>>

INSERT INTO "auth_user" (
    "password",
    "last_login",
    "is_superuser",
    "username",
    "first_name",
    "last_name",
    "email",
    "is_staff",
    "is_active",
    "date_joined"
) VALUES (
    'pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=',
    NULL,
    0,
    'john',
    '',
    '',
    'lennon@thebeatles.com',
    0,
    1,
    '2025-07-18 07:29:05.845970'
)

>>> user.last_name = "Lennon"
>>> user.save()
(0.020) UPDATE "auth_user" SET "password" = 'pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=', "last_login" = NULL, "is_superuser" = 0, "username" = 'john', "first_name" = '', "last_name" = 'Lennon', "email" = 'lennon@thebeatles.com', "is_staff" = 0, "is_active" = 1, "date_joined" = '2025-07-18 07:29:05.845970' WHERE "auth_user"."id" = 1; args=('pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=', False, 'john', '', 'Lennon', 'lennon@thebeatles.com', False, True, '2025-07-18 07:29:05.845970', 1); alias=default
>>>
UPDATE "auth_user"
SET
    "password" = 'pbkdf2_sha256$600000$LVOHL2JIlDQGQpxkbFFcuJ$eyjCbpFRSnp0yty+zQ/Z8E3qXTJBZikxTvOOyf9Mxng=',
    "last_login" = NULL,
    "is_superuser" = 0,
    "username" = 'john',
    "first_name" = '',
    "last_name" = 'Lennon',
    "email" = 'lennon@thebeatles.com',
    "is_staff" = 0,
    "is_active" = 1,
    "date_joined" = '2025-07-18 07:29:05.845970'
WHERE "auth_user"."id" = 1

>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username="john")
(0.007) SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'john' LIMIT 21; args=('john',); alias=default
>>> u.set_password("new password")
>>> u.save()
(0.015) UPDATE "auth_user" SET "password" = 'pbkdf2_sha256$600000$0WO2KTDIkumyqMrX1RPLF5$f0Mc7jZUVkyMii9y9AGmVt7wCOIUPLgc0rrZQtnfj0o=', "last_login" = NULL, "is_superuser" = 0, "username" = 'john', "first_name" = '', "last_name" = 'Lennon', "email" = 'lennon@thebeatles.com', "is_staff" = 0, "is_active" = 1, "date_joined" = '2025-07-18 07:29:05.845970' WHERE "auth_user"."id" = 1; args=('pbkdf2_sha256$600000$0WO2KTDIkumyqMrX1RPLF5$f0Mc7jZUVkyMii9y9AGmVt7wCOIUPLgc0rrZQtnfj0o=', False, 'john', '', 'Lennon', 'lennon@thebeatles.com', False, True, '2025-07-18 07:29:05.845970', 1); alias=default
>>>

>>> from django.contrib.auth import authenticate
>>> user = authenticate(username="john", password="new password")
(0.006) SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'john' LIMIT 21; args=('john',); alias=default
>>> user
<User: john>
>>>
>>> user = authenticate(username="john", password="old password")
(0.002) SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'john' LIMIT 21; args=('john',); alias=default
>>> user
>>>

```

