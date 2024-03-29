from datetime import date
from django.db import models


class Question(models.Model):
    """
    >>> from django.db import models
    >>> m = set(dir(models.Model))
    >>> m
    {'__hash__', '_save_parents', 'full_clean', '_get_unique_checks', '__repr__', '_prepare_related_fields_for_save', '_perform_date_checks', '_do_update', '_set_pk_val', 'refresh_from_db', '__dir__', '__lt__', '_do_insert', 'arefresh_from_db', 'validate_unique', '__doc__', '__reduce__', 'unique_error_message', '_check_model_name_db_lookup_clashes', '__format__', '_check_constraints', '_check_model', '__setattr__', 'clean_fields', 'check', '_check_column_name_clashes', 'pk', '_get_FIELD_display', '__reduce_ex__', '__eq__', '_get_pk_val', 'clean', '__class__', '__gt__', '_check_field_name_clashes', '_save_table', 'delete', 'get_constraints', '_get_next_or_previous_in_order', '_check_m2m_through_same_relationship', '_get_next_or_previous_by_FIELD', '__module__', '_check_swappable', '_get_expr_references', '_check_id_field', 'prepare_database_save', 'from_db', '_check_ordering', 'serializable_value', 'asave', '__ne__', '_check_db_table_comment', '__getattribute__', 'validate_constraints', '_check_indexes', '__ge__', 'save_base', '__getstate__', '__str__', 'get_deferred_fields', 'adelete', '_check_index_together', '_perform_unique_checks', '_check_fields', '_check_unique_together', '_check_single_primary_key', '__subclasshook__', 'date_error_message', '__le__', '__init__', '_check_long_column_names', '_check_default_pk', '_get_field_value_map', '_check_local_fields', '__new__', '__dict__', '__delattr__', '_check_property_name_related_field_accessor_clashes', '__setstate__', '__init_subclass__', '__sizeof__', '_check_managers', '__weakref__', 'save'}
    >>>
    >>> from myapp2.models import Question, Choice, Person, Manufacturer, Car, Topping, Pizza, Group, Membership
    >>> set(dir(Question)).difference(m)
    {
        'pub_date',
        '_meta',
        'id',
        'DoesNotExist',
        'question_text',
        'get_previous_by_pub_date',
        'objects',
        'get_next_by_pub_date',
        'MultipleObjectsReturned'
    }
    >>>
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    """
    >>> set(dir(Choice)).difference(m)
    {'choice_text', '_meta', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned', 'votes'}
    >>>
    """
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Person(models.Model):
    """
    CREATE TABLE "myapp_person" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "first_name" varchar(30) NOT NULL,
        "last_name" varchar(30) NOT NULL
    )
    >>> set(dir(Person)).difference(m)
    {
        'last_name',
        '_meta',
        'objects',
        'id',
        'name',
        'membership_set',
        'DoesNotExist',
        'MultipleObjectsReturned',
        'group_set',
        'first_name'
    }
    >>>
    >>> set(dir(Person)).difference(m)
    {
        'groups',
        'last_name',
        'name',
        'membershippersons',
        '_meta',
        'id',
        'DoesNotExist',
        'first_name',
        'objects',
        'MultipleObjectsReturned'
    }
    >>>
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    name = models.CharField(max_length=128)


# Many-to-one relationships
class Manufacturer(models.Model):
    """
    >>> set(dir(Manufacturer)).difference(m)
    {'car_set', '_meta', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    >>> set(dir(Manufacturer)).difference(m)
    {'_meta', 'id', 'DoesNotExist', 'cars', 'objects', 'MultipleObjectsReturned'}
    >>>
    """
    pass


class Car(models.Model):
    """
    >>> set(dir(Car)).difference(m)
    {'manufacturer_id', 'manufacturer', '_meta', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    manufacturer = models.ForeignKey(Manufacturer,
                                     on_delete=models.CASCADE,
                                     related_name="cars",
                                     related_query_name="car")
    # ...


# Many-to-many relationships
class Topping(models.Model):
    """
    >>> set(dir(Topping)).difference(m)
    {'_meta', 'pizza_set', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    >>> set(dir(Topping)).difference(m)
    {'_meta', 'id', 'DoesNotExist', 'pizzas', 'objects', 'MultipleObjectsReturned'}
    >>>
    """
    pass


class Pizza(models.Model):
    """
    >>> set(dir(Pizza)).difference(m)
    {'_meta', 'toppings', 'objects', 'id', 'DoesNotExist', 'MultipleObjectsReturned'}
    >>>
    """
    toppings = models.ManyToManyField(Topping,
                                      related_name="pizzas",
                                      related_query_name="pizza")


class Group(models.Model):
    """
    >>> set(dir(Group)).difference(m)
    {'_meta', 'DoesNotExist', 'objects', 'id', 'name', 'membership_set', 'members', 'MultipleObjectsReturned'}
    >>>
    >>> set(dir(Group)).difference(m)
    {'name', '_meta', 'id', 'DoesNotExist', 'membershipgroups', 'objects', 'members', 'MultipleObjectsReturned'}
    >>>
    """
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person,
                                     through="Membership",
                                     related_name="groups",
                                     related_query_name="group")

    def __str__(self):
        return self.name


class Membership(models.Model):
    """
    >>> set(dir(Membership)).difference(m)
    {
        'person',
        'invite_reason',
        '_meta',
        'get_next_by_date_joined',
        'objects',
        'group_id',
        'id',
        'date_joined',
        'group',
        'person_id',
        'DoesNotExist',
        'MultipleObjectsReturned',
        'get_previous_by_date_joined'
    }
    >>>
    """
    person = models.ForeignKey(Person,
                               on_delete=models.CASCADE,
                               related_name="membershippersons",
                               related_query_name="membershipperson")
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name="membershipgroups",
                              related_query_name="membershipgroup")
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


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
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
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


"""
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
>>>
INSERT INTO "myapp2_entry" (
    "blog_id",
    "headline",
    "body_text",
    "pub_date",
    "mod_date",
    "number_of_comments",
    "number_of_pingbacks",
    "rating"
) VALUES (
    1,
    'New Lennon Biography',
    '',
    '2008-06-01',
    '2024-03-16',
    0,
    0,
    5
)


>>> Entry.objects.create(blog=beatles, headline='New Lennon Biography in Paperback', pub_date=date(2009, 6, 1))
(0.011) INSERT INTO "myapp2_entry" ("blog_id", "headline", "body_text", "pub_date", "mod_date", "number_of_comments", "number_of_pingbacks", "rating") VALUES (1, 'New Lennon Biography in Paperback', '', '2009-06-01', '2024-03-16', 0, 0, 5); args=[1, 'New Lennon Biography in Paperback', '', '2009-06-01', '2024-03-16', 0, 0, 5]; alias=default
<Entry: New Lennon Biography in Paperback>
>>>
INSERT INTO "myapp2_entry" (
    "blog_id",
    "headline",
    "body_text",
    "pub_date",
    "mod_date",
    "number_of_comments",
    "number_of_pingbacks",
    "rating"
) VALUES (
    1,
    'New Lennon Biography in Paperback',
    '',
    '2009-06-01',
    '2024-03-16',
    0,
    0,
    5
)


>>> Entry.objects.create(blog=pop, headline='Best Albums of 2008', pub_date=date(2008, 12, 15))
(0.009) INSERT INTO "myapp2_entry" ("blog_id", "headline", "body_text", "pub_date", "mod_date", "number_of_comments", "number_of_pingbacks", "rating") VALUES (2, 'Best Albums of 2008', '', '2008-12-15', '2024-03-16', 0, 0, 5); args=[2, 'Best Albums of 2008', '', '2008-12-15', '2024-03-16', 0, 0, 5]; alias=default
<Entry: Best Albums of 2008>
>>>
INSERT INTO "myapp2_entry" (
    "blog_id",
    "headline",
    "body_text",
    "pub_date",
    "mod_date",
    "number_of_comments",
    "number_of_pingbacks",
    "rating"
) VALUES (
    2,
    'Best Albums of 2008',
    '',
    '2008-12-15',
    '2024-03-16',
    0,
    0,
    5
)


>>> Entry.objects.create(blog=pop, headline='Lennon Would Have Loved Hip Hop', pub_date=date(2020, 4, 1))
(0.011) INSERT INTO "myapp2_entry" ("blog_id", "headline", "body_text", "pub_date", "mod_date", "number_of_comments", "number_of_pingbacks", "rating") VALUES (2, 'Lennon Would Have Loved Hip Hop', '', '2020-04-01', '2024-03-16', 0, 0, 5); args=[2, 'Lennon Would Have Loved Hip Hop', '', '2020-04-01', '2024-03-16', 0, 0, 5]; alias=default
<Entry: Lennon Would Have Loved Hip Hop>
>>>
INSERT INTO "myapp2_entry" (
    "blog_id",
    "headline",
    "body_text",
    "pub_date",
    "mod_date",
    "number_of_comments",
    "number_of_pingbacks",
    "rating"
) VALUES (
    2,
    'Lennon Would Have Loved Hip Hop',
    '',
    '2020-04-01',
    '2024-03-16',
    0,
    0,
    5
)


>>> Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
(0.001) SELECT "myapp2_blog"."id", "myapp2_blog"."name", "myapp2_blog"."tagline" FROM "myapp2_blog" INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id") WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND "myapp2_entry"."pub_date" BETWEEN '2008-01-01' AND '2008-12-31') LIMIT 21; args=('%Lennon%', '2008-01-01', '2008-12-31'); alias=default
<QuerySet [<Blog: Beatles Blog>]>
>>>
SELECT
    "myapp2_blog"."id",
    "myapp2_blog"."name",
    "myapp2_blog"."tagline"
FROM "myapp2_blog"
INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id")
WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND "myapp2_entry"."pub_date" BETWEEN '2008-01-01' AND '2008-12-31')
LIMIT 21


>>> Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
(0.002) SELECT "myapp2_blog"."id", "myapp2_blog"."name", "myapp2_blog"."tagline" FROM "myapp2_blog" INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id") INNER JOIN "myapp2_entry" T3 ON ("myapp2_blog"."id" = T3."blog_id") WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND T3."pub_date" BETWEEN '2008-01-01' AND '2008-12-31') LIMIT 21; args=('%Lennon%', '2008-01-01', '2008-12-31'); alias=default
<QuerySet [<Blog: Beatles Blog>, <Blog: Beatles Blog>, <Blog: Pop Music Blog>]>
>>>
SELECT
    "myapp2_blog"."id",
    "myapp2_blog"."name",
    "myapp2_blog"."tagline"
FROM "myapp2_blog"
INNER JOIN "myapp2_entry" ON ("myapp2_blog"."id" = "myapp2_entry"."blog_id")
INNER JOIN "myapp2_entry" T3 ON ("myapp2_blog"."id" = T3."blog_id")
WHERE ("myapp2_entry"."headline" LIKE '%Lennon%' ESCAPE '\' AND T3."pub_date" BETWEEN '2008-01-01' AND '2008-12-31')
LIMIT 21

"""
