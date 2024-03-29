from django.urls import path, register_converter

from . import converters, views

register_converter(converters.DynamicConverter, "dynamic")

urlpatterns = [
    path("dynamic/<dynamic:value>/", views.empty_view, name="dynamic"),
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/dynamic/<dynamic:value>/	myurl.views.empty_view	dynamic

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
