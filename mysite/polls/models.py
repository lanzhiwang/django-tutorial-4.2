import datetime

from django.db import models
from django.utils import timezone
"""
$ python manage.py sqlmigrate polls 0001
<--""
   Level WARNING
************************************ manage.py ************************************
(0.002)
            SELECT name, type FROM sqlite_master
            WHERE type in ('table', 'view') AND NOT name='sqlite_sequence'
            ORDER BY name; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
(0.000) PRAGMA foreign_keys = OFF; args=None; alias=default
(0.000) PRAGMA foreign_keys; args=None; alias=default
(0.000) BEGIN; args=None; alias=default
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL); (params None)
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED); (params None)
(0.005) PRAGMA foreign_key_check; args=None; alias=default
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id"); (params ())
(0.000) COMMIT; args=None; alias=default
(0.000) PRAGMA foreign_keys = ON; args=None; alias=default
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "question_text" varchar(200) NOT NULL,
    "pub_date" datetime NOT NULL
);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
$
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


"""
$ python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.13 (main, Mar 12 2024, 12:27:52) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>> from polls.models import Choice, Question

>>> Question.objects.all()
(0.004) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" LIMIT 21; args=(); alias=default
<QuerySet []>
>>>

>>> from django.utils import timezone

>>> q = Question(question_text="What's new?", pub_date=timezone.now())

>>> q.save()
(0.015) INSERT INTO "polls_question" ("question_text", "pub_date") VALUES ('What''s new?', '2024-03-16 07:46:23.100030'); args=["What's new?", '2024-03-16 07:46:23.100030']; alias=default

>>> q.id
1

>>> q.question_text
"What's new?"

>>> q.pub_date
datetime.datetime(2024, 3, 16, 7, 46, 23, 100030, tzinfo=datetime.timezone.utc)

>>> q.question_text = "What's up?"
>>> q.save()
(0.013) UPDATE "polls_question" SET "question_text" = 'What''s up?', "pub_date" = '2024-03-16 07:46:23.100030' WHERE "polls_question"."id" = 1; args=("What's up?", '2024-03-16 07:46:23.100030', 1); alias=default

>>> Question.objects.all()
(0.003) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" LIMIT 21; args=(); alias=default
<QuerySet [<Question: Question object (1)>]>
>>>

$ python manage.py shell
<--""
   Level WARNING
************************************ manage.py ************************************
Python 3.10.13 (main, Mar 12 2024, 12:27:52) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>>
>>> from polls.models import Choice, Question
>>> Question.objects.all()
(0.003) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" LIMIT 21; args=(); alias=default
<QuerySet [<Question: What's up?>]>
>>>
>>> Question.objects.filter(id=1)
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith="What")
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."question_text" LIKE 'What%' ESCAPE '\' LIMIT 21; args=('What%',); alias=default
<QuerySet [<Question: What's up?>]>
>>>
>>>
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."pub_date" BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59.999999' LIMIT 21; args=('2024-01-01 00:00:00', '2024-12-31 23:59:59.999999'); alias=default
<Question: What's up?>
>>>
>>> Question.objects.get(id=2)
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."id" = 2 LIMIT 21; args=(2,); alias=default
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.10/site-packages/django/db/models/query.py", line 637, in get
    raise self.model.DoesNotExist(
polls.models.Question.DoesNotExist: Question matching query does not exist.
>>>
>>> Question.objects.get(pk=1)
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."id" = 1 LIMIT 21; args=(1,); alias=default
<Question: What's up?>
>>> q = Question.objects.get(pk=1)
(0.001) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."id" = 1 LIMIT 21; args=(1,); alias=default
>>> q.was_published_recently()
True
>>> q = Question.objects.get(pk=1)
(0.002) SELECT "polls_question"."id", "polls_question"."question_text", "polls_question"."pub_date" FROM "polls_question" WHERE "polls_question"."id" = 1 LIMIT 21; args=(1,); alias=default
>>> q.choice_set.all()
(0.003) SELECT "polls_choice"."id", "polls_choice"."question_id", "polls_choice"."choice_text", "polls_choice"."votes" FROM "polls_choice" WHERE "polls_choice"."question_id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet []>
>>> q.choice_set.create(choice_text="Not much", votes=0)
(0.019) INSERT INTO "polls_choice" ("question_id", "choice_text", "votes") VALUES (1, 'Not much', 0); args=[1, 'Not much', 0]; alias=default
<Choice: Not much>
>>> q.choice_set.create(choice_text="The sky", votes=0)
(0.022) INSERT INTO "polls_choice" ("question_id", "choice_text", "votes") VALUES (1, 'The sky', 0); args=[1, 'The sky', 0]; alias=default
<Choice: The sky>
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)
(0.018) INSERT INTO "polls_choice" ("question_id", "choice_text", "votes") VALUES (1, 'Just hacking again', 0); args=[1, 'Just hacking again', 0]; alias=default
>>> c.question
<Question: What's up?>
>>> q.choice_set.all()
(0.003) SELECT "polls_choice"."id", "polls_choice"."question_id", "polls_choice"."choice_text", "polls_choice"."votes" FROM "polls_choice" WHERE "polls_choice"."question_id" = 1 LIMIT 21; args=(1,); alias=default
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
(0.001) SELECT COUNT(*) AS "__count" FROM "polls_choice" WHERE "polls_choice"."question_id" = 1; args=(1,); alias=default
3
>>>
>>> Choice.objects.filter(question__pub_date__year=current_year)
(0.002) SELECT "polls_choice"."id", "polls_choice"."question_id", "polls_choice"."choice_text", "polls_choice"."votes" FROM "polls_choice" INNER JOIN "polls_question" ON ("polls_choice"."question_id" = "polls_question"."id") WHERE "polls_question"."pub_date" BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59.999999' LIMIT 21; args=('2024-01-01 00:00:00', '2024-12-31 23:59:59.999999'); alias=default
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>>
>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete()
(0.000) BEGIN; args=None; alias=default
(0.010) DELETE FROM "polls_choice" WHERE ("polls_choice"."question_id" = 1 AND "polls_choice"."choice_text" LIKE 'Just hacking%' ESCAPE '\'); args=(1, 'Just hacking%'); alias=default
(0.005) COMMIT; args=None; alias=default
(1, {'polls.Choice': 1})
>>>
>>>
"""
