from django.urls import path, re_path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("", views.index, name="index"),
]

