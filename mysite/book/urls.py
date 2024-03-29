from django.urls import path
from . import views

app_name = "book"
urlpatterns = [
    path('', views.book_list),
    path('login', views.book_login, name="login"),
]

"""
root@d32f59b1b0f0:/django-tutorial-4.2/mysite# python manage.py show_urls

/book1/	book.views.book_list
/book1/login	book.views.book_login	login
/book2/	book.views.book_list
/book2/login	book.views.book_login	login

root@d32f59b1b0f0:/django-tutorial-4.2/mysite#
"""
