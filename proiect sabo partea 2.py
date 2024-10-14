import csv
import re


def citire_csv(nume_fisier):
    jocuri = []
    with open(nume_fisier, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) == 3:
                cod, cuvant_incomplet, cuvant_complet = row
                jocuri.append((cod, cuvant_incomplet, cuvant_complet))
    return jocuri


def citire_dictionar(nume_fisier):
    cuvinte = []
    with open(nume_fisier, mode='r', encoding='utf-8') as file:
        cuvinte = [line.strip().upper() for line in file]
    return cuvinte


def gaseste_cuvant_din_dictionar(cuvant_incomplet, dictionar):

    pattern = cuvant_incomplet.replace('*', '.')
    regex = re.compile(f"^{pattern}$")


    for cuvant in dictionar:
        if regex.match(cuvant):
            return cuvant

    return cuvant_incomplet


def proceseaza_jocuri_optimizat(jocuri, dictionar):
    incercari_totale = 0
    rezultate = []

    for cod, cuvant_incomplet, cuvant_complet in jocuri:
        cuvant_gasit = gaseste_cuvant_din_dictionar(cuvant_incomplet, dictionar)
        incercari = 1 if cuvant_gasit == cuvant_complet else len(cuvant_complet)
        incercari_totale += incercari
        rezultate.append((cod, cuvant_incomplet, cuvant_gasit, incercari))

    return incercari_totale, rezultate


def afiseaza_rezultate(incercari_totale, rezultate):
    print(f"Numar total de incercari: {incercari_totale}")
    for cod, cuvant_incomplet, cuvant_gasit, incercari in rezultate:
        print(f"Joc {cod}: {cuvant_incomplet} -> {cuvant_gasit} in {incercari} incercari")


if __name__ == "__main__":
    nume_fisier_jocuri = "jocuri.csv"
    nume_fisier_dictionar = "dictionar.txt"
    jocuri = citire_csv(nume_fisier_jocuri)
    dictionar = citire_dictionar(nume_fisier_dictionar)

    incercari_totale, rezultate = proceseaza_jocuri_optimizat(jocuri, dictionar)
    afiseaza_rezultate(incercari_totale, rezultate)

    if incercari_totale > 1200:
        print("Numarul de incercari depaseste limita de 1200!")
    else:
        print("Te-ai incadrat in limita de 1200 de incercari.")
