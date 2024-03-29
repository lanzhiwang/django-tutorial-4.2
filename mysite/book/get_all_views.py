from django.conf import settings
from django.urls import URLResolver, URLPattern

root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
VIEW_NAMES = []  # maintain a global list


def get_all_view_names(urlpatterns):
    global VIEW_NAMES
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            get_all_view_names(pattern.url_patterns)  # call this function recursively
        elif isinstance(pattern, URLPattern):
            view_name = pattern.callback.__name__  # get the view name
            VIEW_NAMES.append(view_name)  # add the view to the global list
    return VIEW_NAMES


get_all_view_names(all_urlpatterns)

"""
from django.conf import settings
from django.urls import reverse

root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns

for pattern in root_urlconf.urls.urlpatterns:
    print(pattern)

reverse("login")

reverse("book:login")

reverse("book1:login")

reverse("book2:login")

reverse("app_book1:login")

reverse("app_book2:login")

################################################################

不做任何设置
>>> from django.conf import settings
>>> from django.urls import reverse
>>>
>>> root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
>>> all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
>>>
>>> for pattern in root_urlconf.urls.urlpatterns:
...     print(pattern)
...
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (None:None) 'book10/'>
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (None:None) 'book20/'>
>>>
>>> reverse("login")
'/book20/login'

>>> reverse("book:login")
django.urls.exceptions.NoReverseMatch: 'book' is not a registered namespace

>>> reverse("book1:login")
django.urls.exceptions.NoReverseMatch: 'book1' is not a registered namespace

>>> reverse("book2:login")
django.urls.exceptions.NoReverseMatch: 'book2' is not a registered namespace

>>> reverse("app_book1:login")
django.urls.exceptions.NoReverseMatch: 'app_book1' is not a registered namespace

>>> reverse("app_book2:login")
django.urls.exceptions.NoReverseMatch: 'app_book2' is not a registered namespace

################################################################

只设置 Application namespace
>>> from django.conf import settings
>>> from django.urls import reverse
>>>
>>> root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
>>> all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
>>>
>>> for pattern in root_urlconf.urls.urlpatterns:
...     print(pattern)
...
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book) 'book10/'>
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book) 'book20/'>
>>>
>>> reverse("login")
django.urls.exceptions.NoReverseMatch: Reverse for 'login' not found. 'login' is not a valid view function or pattern name.

>>> reverse("book:login")
'/book10/login'
>>>
>>> reverse("book1:login")
django.urls.exceptions.NoReverseMatch: 'book1' is not a registered namespace

>>> reverse("book2:login")
django.urls.exceptions.NoReverseMatch: 'book2' is not a registered namespace

>>> reverse("app_book1:login")
django.urls.exceptions.NoReverseMatch: 'app_book1' is not a registered namespace

>>> reverse("app_book2:login")
django.urls.exceptions.NoReverseMatch: 'app_book2' is not a registered namespace

################################################################

只设置 Instance namespace

django.core.exceptions.ImproperlyConfigured:
Specifying a namespace in include() without providing an app_name is not supported.
Set the app_name attribute in the included module, or pass a 2-tuple containing the list of patterns and app_name instead.

只设置 Instance namespace 不支持，设置 Instance namespace 以后一定要设置 Application namespace
这时设置 Application namespace 的方法有两种：
1、使用 app_name = "book"
2、使用 include((pattern_list, app_namesapace), namespace=None)
    path('book1/', include(('book.urls', 'app_book1'), namespace='book1')),
    path('book2/', include(('book.urls', 'app_book2'), namespace='book2')),


1、使用 app_name = "book"
>>> from django.conf import settings
>>> from django.urls import reverse
>>>
>>> root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
>>> all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
>>>
>>> for pattern in root_urlconf.urls.urlpatterns:
...     print(pattern)
...
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book1) 'book11/'>
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book2) 'book21/'>
>>>
>>> reverse("login")
django.urls.exceptions.NoReverseMatch: Reverse for 'login' not found. 'login' is not a valid view function or pattern name.

>>> reverse("book:login")
'/book21/login'

>>> reverse("book1:login")
'/book11/login'

>>> reverse("book2:login")
'/book21/login'

>>> reverse("app_book1:login")
django.urls.exceptions.NoReverseMatch: 'app_book1' is not a registered namespace

>>> reverse("app_book2:login")
django.urls.exceptions.NoReverseMatch: 'app_book2' is not a registered namespace


2、使用 include((pattern_list, app_namesapace), namespace=None)
    path('book1/', include(('book.urls', 'app_book1'), namespace='book1')),
    path('book2/', include(('book.urls', 'app_book2'), namespace='book2')),
>>> from django.conf import settings
>>> from django.urls import reverse
>>>
>>> root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
>>> all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
>>>
>>> for pattern in root_urlconf.urls.urlpatterns:
...     print(pattern)
...
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (app_book1:book1) 'book12/'>
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (app_book2:book2) 'book22/'>
>>>
>>> reverse("login")
django.urls.exceptions.NoReverseMatch: Reverse for 'login' not found. 'login' is not a valid view function or pattern name.

>>> reverse("book:login")
django.urls.exceptions.NoReverseMatch: 'book' is not a registered namespace

>>> reverse("book1:login")
'/book12/login'

>>> reverse("book2:login")
'/book22/login'

>>> reverse("app_book1:login")
'/book12/login'

>>> reverse("app_book2:login")
'/book22/login'


1、使用 app_name = "book"
2、使用 include((pattern_list, app_namesapace), namespace=None)
    path('book1/', include(('book.urls', 'app_book1'), namespace='book1')),
    path('book2/', include(('book.urls', 'app_book2'), namespace='book2')),
>>> from django.conf import settings
>>> from django.urls import reverse
>>>
>>> root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
>>> all_urlpatterns = root_urlconf.urls.urlpatterns  # project's urlpatterns
>>>
>>> for pattern in root_urlconf.urls.urlpatterns:
...     print(pattern)
...
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book1) 'book12/'>
<URLResolver <module 'book.urls' from '/django-tutorial-4.2/mysite/book/urls.py'> (book:book2) 'book22/'>
>>>
>>> reverse("login")
django.urls.exceptions.NoReverseMatch: Reverse for 'login' not found. 'login' is not a valid view function or pattern name.

>>> reverse("book:login")
'/book22/login'

>>> reverse("book1:login")
'/book12/login'
>>>
>>> reverse("book2:login")
'/book22/login'
>>>
>>> reverse("app_book1:login")
django.urls.exceptions.NoReverseMatch: 'app_book1' is not a registered namespace

>>> reverse("app_book2:login")
django.urls.exceptions.NoReverseMatch: 'app_book2' is not a registered namespace
>>>

"""
