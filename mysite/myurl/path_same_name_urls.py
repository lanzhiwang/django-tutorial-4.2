from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.DynamicConverter, "to_url_value_error")

urlpatterns = [
    # Different number of arguments.
    path("number_of_args/0/", views.empty_view, name="number_of_args"),
    path("number_of_args/1/<value>/", views.empty_view, name="number_of_args"),
    # Different names of the keyword arguments.
    path("kwargs_names/a/<a>/", views.empty_view, name="kwargs_names"),
    path("kwargs_names/b/<b>/", views.empty_view, name="kwargs_names"),
    # Different path converters.
    path("converter/path/<path:value>/", views.empty_view, name="converter"),
    path("converter/str/<str:value>/", views.empty_view, name="converter"),
    path("converter/slug/<slug:value>/", views.empty_view, name="converter"),
    path("converter/int/<int:value>/", views.empty_view, name="converter"),
    path("converter/uuid/<uuid:value>/", views.empty_view, name="converter"),
    # Different regular expressions.
    re_path(r"^regex/uppercase/([A-Z]+)/", views.empty_view, name="regex"),
    re_path(r"^regex/lowercase/([a-z]+)/", views.empty_view, name="regex"),
    # converter.to_url() raises ValueError (no match).
    path(
        "converter_to_url/int/<value>/",
        views.empty_view,
        name="converter_to_url",
    ),
    path(
        "converter_to_url/tiny_int/<to_url_value_error:value>/",
        views.empty_view,
        name="converter_to_url",
    ),
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/number_of_args/0/	myurl.views.empty_view	number_of_args

/number_of_args/1/<value>/	myurl.views.empty_view	number_of_args

/kwargs_names/a/<a>/	myurl.views.empty_view	kwargs_names

/kwargs_names/b/<b>/	myurl.views.empty_view	kwargs_names

/converter/path/<path:value>/	myurl.views.empty_view	converter

/converter/str/<str:value>/	myurl.views.empty_view	converter

/converter/slug/<slug:value>/	myurl.views.empty_view	converter

/converter/int/<int:value>/	myurl.views.empty_view	converter

/converter/uuid/<uuid:value>/	myurl.views.empty_view	converter

/regex/uppercase/<var>/	myurl.views.empty_view	regex

/regex/lowercase/<var>/	myurl.views.empty_view	regex

/converter_to_url/int/<value>/	myurl.views.empty_view	converter_to_url

/converter_to_url/tiny_int/<to_url_value_error:value>/	myurl.views.empty_view	converter_to_url

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
