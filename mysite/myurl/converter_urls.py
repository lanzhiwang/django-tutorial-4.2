from django.urls import path

from . import views

urlpatterns = [
    path("{x}/<{x}:{x}>/".format(x=name), views.empty_view, name=name)
    for name in ("int", "path", "slug", "str", "uuid")
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/int/<int:int>/	myurl.views.empty_view	int

/path/<path:path>/	myurl.views.empty_view	path

/slug/<slug:slug>/	myurl.views.empty_view	slug

/str/<str:str>/	myurl.views.empty_view	str

/uuid/<uuid:uuid>/	myurl.views.empty_view	uuid

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
