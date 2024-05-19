from django.db import models

class Wynik(models.Model):

    wiek = models.IntegerField()
    poczucie_smutku = models.IntegerField()
    nerwowe_zachowanie = models.IntegerField()
    problemy_ze_spaniem = models.IntegerField()
    problemy_z_koncentracja = models.IntegerField()
    przejadanie_sie = models.IntegerField()
    poczucie_winy = models.IntegerField()
    problem_z_przywiazaniem = models.IntegerField()
    proba_samobojcza = models.FloatField()
    wynik = models.IntegerField()
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Wynik {self.id} - {self.wynik}'
