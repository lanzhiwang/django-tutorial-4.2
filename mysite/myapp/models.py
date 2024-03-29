from django.db import models


class Question(models.Model):
    """
    >>> from django.db import models
    >>> m = set(dir(models.Model))
    >>> m
    {'__weakref__', '__sizeof__', '_check_model', 'validate_constraints', 'date_error_message', 'clean_fields', '_check_field_name_clashes', '__str__', '_get_pk_val', '_check_local_fields', '__lt__', '_perform_unique_checks', '_check_db_table_comment', 'refresh_from_db', '_prepare_related_fields_for_save', '__getstate__', '_perform_date_checks', '_get_next_or_previous_by_FIELD', '_get_expr_references', '_check_default_pk', 'validate_unique', '_set_pk_val', 'save_base', '__gt__', '_check_managers', 'unique_error_message', '__class__', '__repr__', '_check_ordering', '_get_unique_checks', '_check_long_column_names', '_save_table', 'check', 'get_deferred_fields', '_save_parents', 'save', '__reduce__', '__new__', 'arefresh_from_db', 'full_clean', 'pk', '__reduce_ex__', 'asave', '_check_model_name_db_lookup_clashes', '_check_fields', '__setstate__', '_check_property_name_related_field_accessor_clashes', '_check_swappable', '__ne__', '_check_constraints', '__doc__', '_check_unique_together', '__subclasshook__', '_do_update', '_get_next_or_previous_in_order', '_check_column_name_clashes', '__ge__', '__eq__', '_check_id_field', '_check_indexes', '__format__', 'adelete', '__dir__', '_get_FIELD_display', '__module__', '__dict__', '_check_m2m_through_same_relationship', '_check_index_together', '__delattr__', '_check_single_primary_key', '_do_insert', '__init_subclass__', '__le__', '__getattribute__', 'from_db', 'clean', 'get_constraints', 'serializable_value', 'prepare_database_save', 'delete', '__init__', '__setattr__', '__hash__', '_get_field_value_map'}
    >>>
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


class Group(models.Model):
    """
    >>> set(dir(Group)).difference(m)
    {'_meta', 'DoesNotExist', 'objects', 'id', 'name', 'membership_set', 'members', 'MultipleObjectsReturned'}
    >>>
    """
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


# One-to-one relationships
