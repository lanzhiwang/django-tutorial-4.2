from django.urls import include, path

from . import views

urlpatterns = [
    path("extra/<extra>/", views.empty_view, name="inner-extra"),
    path("", include("myurl.more_urls")),
]

"""
root@6ae7c8f53871:/django-tutorial-4.2/mysite# python manage.py show_urls

/extra/<extra>/	myurl.views.empty_view	inner-extra

/more/<extra>/	myurl.views.empty_view	inner-more

root@6ae7c8f53871:/django-tutorial-4.2/mysite#
"""
