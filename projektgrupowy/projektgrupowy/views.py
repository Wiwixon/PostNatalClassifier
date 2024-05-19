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
    wyniki = Wynik.objects.all()

    # Pobierz odpowiedzi dla każdego pola
    wiek_stats = Wynik.objects.values('wiek').annotate(count=Count('wiek'))
    poczucie_smutku_stats = Wynik.objects.values('poczucie_smutku').annotate(count=Count('poczucie_smutku'))
    nerwowe_zachowanie_stats = Wynik.objects.values('nerwowe_zachowanie').annotate(count=Count('nerwowe_zachowanie'))
    problemy_ze_spaniem_stats = Wynik.objects.values('problemy_ze_spaniem').annotate(count=Count('problemy_ze_spaniem'))
    problemy_z_koncentracja_stats = Wynik.objects.values('problemy_z_koncentracja').annotate(
        count=Count('problemy_z_koncentracja'))
    przejadanie_sie_stats = Wynik.objects.values('przejadanie_sie').annotate(count=Count('przejadanie_sie'))
    poczucie_winy_stats = Wynik.objects.values('poczucie_winy').annotate(count=Count('poczucie_winy'))
    problem_z_przywiazaniem_stats = Wynik.objects.values('problem_z_przywiazaniem').annotate(
        count=Count('problem_z_przywiazaniem'))
    proba_samobojcza_stats = Wynik.objects.values('proba_samobojcza').annotate(count=Count('proba_samobojcza'))
    wynik_stats = Wynik.objects.values('wynik').annotate(count=Count('wynik'))

    total_count = Wynik.objects.count()  # Całkowita liczba obserwacji

    # Przekształć dane na procentowe udziały
    for stat in [wiek_stats, poczucie_smutku_stats, nerwowe_zachowanie_stats, problemy_ze_spaniem_stats,
                 problemy_z_koncentracja_stats, przejadanie_sie_stats, poczucie_winy_stats,
                 problem_z_przywiazaniem_stats, proba_samobojcza_stats, wynik_stats ]:
        for s in stat:
            s['percent'] = (s['count'] / total_count) * 100 if total_count > 0 else 0

    return render(request, 'wyniki_list.html', {
        'wiek_stats': wiek_stats,
        'poczucie_smutku_stats': poczucie_smutku_stats,
        'nerwowe_zachowanie_stats': nerwowe_zachowanie_stats,
        'problemy_ze_spaniem_stats': problemy_ze_spaniem_stats,
        'problemy_z_koncentracja_stats': problemy_z_koncentracja_stats,
        'przejadanie_sie_stats': przejadanie_sie_stats,
        'poczucie_winy_stats': poczucie_winy_stats,
        'problem_z_przywiazaniem_stats': problem_z_przywiazaniem_stats,
        'proba_samobojcza_stats': proba_samobojcza_stats,
        'wynik_stats' : wynik_stats
    })


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