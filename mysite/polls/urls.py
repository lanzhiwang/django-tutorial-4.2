from django.urls import path, re_path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("", views.index, name="index"),
    # /articles/2003/
    # views.special_case_2003(request)
    # /articles/2003 would not match any of these patterns, because each pattern requires that the URL end with a slash.
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    # /articles/2005/03/
    # views.month_archive(request, year=2005, month=3)
    path("articles/<int:year>/<int:month>/", views.month_archive),
    # /articles/2003/03/building-a-django-site/
    # views.article_detail(request, year=2003, month=3, slug="building-a-django-site").
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
    path("articles/<yyyy:year>/", views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive),
    re_path(
        r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$",
        views.article_detail,
    ),
    re_path(r"^blog/(page-([0-9]+)/)?$", views.blog_articles),  # bad
    re_path(r"^comments/(?:page-(?P<page_number>[0-9]+)/)?$", views.comments),  # good
]

