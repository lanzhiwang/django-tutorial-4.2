from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("articles/2003/", views.empty_view, name="articles-2003"),
    path("articles/<int:year>/", views.empty_view, name="articles-year"),
    path(
        "articles/<int:year>/<int:month>/", views.empty_view, name="articles-year-month"
    ),
    path(
        "articles/<int:year>/<int:month>/<int:day>/",
        views.empty_view,
        name="articles-year-month-day",
    ),
    path("books/2007/", views.empty_view, {"extra": True}, name="books-2007"),
    path(
        "books/<int:year>/<int:month>/<int:day>/",
        views.empty_view,
        {"extra": True},
        name="books-year-month-day",
    ),
    path("users/", views.empty_view, name="users"),
    path("users/<id>/", views.empty_view, name="user-with-id"),
    path("included_urls/", include("myurl.included_urls")),
    re_path(r"^regex/(?P<pk>[0-9]+)/$", views.empty_view, name="regex"),
    re_path(
        r"^regex_optional/(?P<arg1>\d+)/(?:(?P<arg2>\d+)/)?",
        views.empty_view,
        name="regex_optional",
    ),
    re_path(
        r"^regex_only_optional/(?:(?P<arg1>\d+)/)?",
        views.empty_view,
        name="regex_only_optional",
    ),
    path("", include("myurl.more_urls"), {"sub-extra": False}),
    path("<lang>/<path:url>/", views.empty_view, name="lang-and-path"),
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/articles/2003/	myurl.views.empty_view	articles-2003

/articles/<int:year>/	myurl.views.empty_view	articles-year

/articles/<int:year>/<int:month>/	myurl.views.empty_view	articles-year-month

/articles/<int:year>/<int:month>/<int:day>/	myurl.views.empty_view	articles-year-month-day

/books/2007/	myurl.views.empty_view	books-2007

/books/<int:year>/<int:month>/<int:day>/	myurl.views.empty_view	books-year-month-day

/users/	myurl.views.empty_view	users

/users/<id>/	myurl.views.empty_view	user-with-id

/included_urls/extra/<extra>/	myurl.views.empty_view	inner-extra
/included_urls/more/<extra>/	myurl.views.empty_view	inner-more

/regex/<pk>/	myurl.views.empty_view	regex

/regex_optional/<arg1>/	myurl.views.empty_view	regex_optional

/regex_only_optional/	myurl.views.empty_view	regex_only_optional

/more/<extra>/	myurl.views.empty_view	inner-more

/<lang>/<path:url>/	myurl.views.empty_view	lang-and-path

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
