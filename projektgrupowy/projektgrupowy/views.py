import joblib
from django.shortcuts import render
from django.http import HttpResponse, request
import numpy as np


def home(request):
    context = {
        'moje_dane': 'To są dane dla mojej podstrony.',
    }
    return render(request, 'index.html', context)

def siema(request):
    return HttpResponse("Siema, to jest odpowiedź widoku!")

def home(request):
    return render(request,'index.html')
def index(request):
    return HttpResponse("<h1> siema </h1>")

def info(request):
    return render(request, 'info.html')

xgb_model = joblib.load('xgbClassifier.pkl')
def classify(request):
    if request.method == 'POST':
        # Pobierz dane z formularza
        wiek = int(request.POST.get('wiek'))
        pytania = [
            int(request.POST.get('Poczucie_smutku')),
            int(request.POST.get('Nerwowe_zachowanie_w_stosunku_do_partnera_lub_dziecka')),
            int(request.POST.get('Problemy_ze_spaniem')),
            int(request.POST.get('Problemy_z_koncentracją')),
            int(request.POST.get('Przejadanie_się_lub_niedojadanie')),
            int(request.POST.get('Poczucie_winy')),
            int(request.POST.get('Problem_z_przywiązaniem_do_dziecka')),
            int(request.POST.get('Próba samobójcza'))
        ]

        # Przekształć dane na wektor NumPy
        dane = np.array([[wiek] + pytania])

        # Wykonaj prognozę przy użyciu wcześniej wytrenowanego klasyfikatora XGBoost
        wynik = xgb_model.predict(dane)

        # Wyświetl wynik na stronie
        if wynik == 0:
            wynik_tekst = "Nie odczuwasz depresji."
        elif wynik == 1:
            wynik_tekst = "Troche depresja."
        else:
            wynik_tekst = "Odczuwasz depresję."

        return render(request, 'wynik.html', {'wynik_tekst': wynik_tekst})
    else:
        return render(request, 'index.html')