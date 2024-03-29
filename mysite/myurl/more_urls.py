from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^more/(?P<extra>\w+)/$",
        views.empty_view,
        {"sub-extra": True},
        name="inner-more",
    ),
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/more/<extra>/	myurl.views.empty_view	inner-more

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
