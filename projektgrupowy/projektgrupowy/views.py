from django.shortcuts import render
from django.http import HttpResponse


def siema(request):
    return HttpResponse("Siema, to jest odpowiedź widoku!")

def home(request):
    return render(request,'index.html')
def index(request):
    return HttpResponse("<h1> siema </h1>")