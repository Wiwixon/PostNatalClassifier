import joblib
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, request
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier
import pickle

from django.db import models
from .models import Wynik
def home(request):
    context = {
        'moje_dane': ' ',
    }
    return render(request, 'index.html', context)

def siema(request):
    return HttpResponse("Siema, to jest odpowiedź widoku!")

def home(request):
    return render(request,'index.html')
def index(request):
    return HttpResponse("<h1> siema </h1>")

def info(request):
    wyniki = Wynik.objects.all()
    return render(request, 'info.html', {'wyniki': wyniki})

def depr(request):
    return render(request, 'depresja.html')

def stats(request):
    wyniki = Wynik.objects.all()
    return render(request, 'info.html', {'wyniki': wyniki})


def wyniki_list(request):
    total_count = Wynik.objects.count()  # Całkowita liczba obserwacji

    # Lista pól do statystyk
    fields = [
        'wiek', 'poczucie_smutku', 'nerwowe_zachowanie', 'problemy_ze_spaniem',
        'problemy_z_koncentracja', 'przejadanie_sie', 'poczucie_winy',
        'problem_z_przywiazaniem', 'proba_samobojcza'
    ]

    stats = {}
    for field in fields:
        stats[field] = list(Wynik.objects.values(field).annotate(count=Count(field)))

    # Przekształć dane na procentowe udziały
    for field in fields:
        for s in stats[field]:
            s['percent'] = (s['count'] / total_count) * 100 if total_count > 0 else 0

    context = {
        'wiek_labels': [item['wiek'] for item in stats['wiek']],
        'wiek_data': [item['percent'] for item in stats['wiek']],
        'poczucie_smutku_labels': [item['poczucie_smutku'] for item in stats['poczucie_smutku']],
        'poczucie_smutku_data': [item['percent'] for item in stats['poczucie_smutku']],
        'nerwowe_zachowanie_labels': [item['nerwowe_zachowanie'] for item in stats['nerwowe_zachowanie']],
        'nerwowe_zachowanie_data': [item['percent'] for item in stats['nerwowe_zachowanie']],
        'problemy_ze_spaniem_labels': [item['problemy_ze_spaniem'] for item in stats['problemy_ze_spaniem']],
        'problemy_ze_spaniem_data': [item['percent'] for item in stats['problemy_ze_spaniem']],
        'problemy_z_koncentracja_labels': [item['problemy_z_koncentracja'] for item in stats['problemy_z_koncentracja']],
        'problemy_z_koncentracja_data': [item['percent'] for item in stats['problemy_z_koncentracja']],
        'przejadanie_sie_labels': [item['przejadanie_sie'] for item in stats['przejadanie_sie']],
        'przejadanie_sie_data': [item['percent'] for item in stats['przejadanie_sie']],
        'poczucie_winy_labels': [item['poczucie_winy'] for item in stats['poczucie_winy']],
        'poczucie_winy_data': [item['percent'] for item in stats['poczucie_winy']],
        'problem_z_przywiazaniem_labels': [item['problem_z_przywiazaniem'] for item in stats['problem_z_przywiazaniem']],
        'problem_z_przywiazaniem_data': [item['percent'] for item in stats['problem_z_przywiazaniem']],
        'proba_samobojcza_labels': [item['proba_samobojcza'] for item in stats['proba_samobojcza']],
        'proba_samobojcza_data': [item['percent'] for item in stats['proba_samobojcza']],
    }

    return render(request, 'wyniki_list.html', context)



xgb_model = pickle.load(open('xgbClassifier.pkl', "rb"))


#xgb_model = joblib.load('xgbClassifier.pkl')
def classify(request):
    if request.method == 'POST':
        # Po

        pytania = [
            int(request.POST.get('wiek')),
            int(request.POST.get('Poczucie_smutku')),
            int(request.POST.get('Nerwowe_zachowanie_w_stosunku_do_partnera_lub_dziecka')),
            int(request.POST.get('Problemy_ze_spaniem')),
            int(request.POST.get('Problemy_z_koncentracją')),
            int(request.POST.get('Przejadanie_się_lub_niedojadanie')),
            int(request.POST.get('Poczucie_winy')),
            int(request.POST.get('Problem_z_przywiązaniem_do_dziecka')),
            float(request.POST.get('Próba_samobójcza'))
        ]
        dane = np.array([pytania])
        print(pytania)


        wynik = xgb_model.predict(dane)

        nowy_wynik = Wynik(
            wiek=pytania[0],
            poczucie_smutku=pytania[1],
            nerwowe_zachowanie=pytania[2],
            problemy_ze_spaniem=pytania[3],
            problemy_z_koncentracja=pytania[4],
            przejadanie_sie=pytania[5],
            poczucie_winy=pytania[6],
            problem_z_przywiazaniem=pytania[7],
            proba_samobojcza=pytania[8],
            wynik=wynik
        )
        nowy_wynik.save()




        print(wynik)
        if wynik == 0:
            wynik_tekst = "Nie stwierdzono ryzyka depresji poporodowej."
        elif wynik == 1:
            wynik_tekst = "Istnieje ryzyko depresji poporodowej."

        return render(request, 'wynik.html', {'wynik_tekst': wynik_tekst})
    else:
        return render(request, 'index.html')