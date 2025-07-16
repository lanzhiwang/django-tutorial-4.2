from django.shortcuts import render
from django.http import HttpResponse
from logging_tree import printout


def index(request):
    printout()
    return HttpResponse("Hello, world. You're at the polls index.")
