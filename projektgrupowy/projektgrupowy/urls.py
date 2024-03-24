"""
URL configuration for projektgrupowy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse  # importujemy moduł HttpResponse

def index(request):  # definiujemy funkcję widoku dla głównej strony
    return HttpResponse("Witaj na stronie głównej!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('suti/', views.siema),
    path('', index),  # dodajemy pusty wzorzec dla głównej strony
    path('klasyfikator/', views.home),

]
