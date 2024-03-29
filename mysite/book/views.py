from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect,reverse

def book_list(request):
    current_namespace = request.resolver_match.namespace
    if request.GET.get("username"):
        return HttpResponse("My book list !!!!")
    else:
        print("current_namespace:", current_namespace)
        # return redirect(reverse("login"))
        return redirect(reverse("%s:login" % current_namespace))

def book_login(request):
    return HttpResponse("Please Login!!!!")
