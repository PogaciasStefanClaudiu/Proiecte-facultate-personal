import random

RANDURI = 11
COLOANE = 11

SCORURI = {
    'linie_3': 5,
    'linie_4': 10,
    'linie_5': 50,
    'L_3': 20,
    'T_3': 30
}

def initializeaza_tabla():
    tabla = []
    for i in range(RANDURI):
        rand = [random.randint(1, 4) for _ in range(COLOANE)]
        tabla.append(rand)
    return tabla


def afiseaza_tabla(tabla):
    for rand in tabla:
        print(rand)
    print()


def detecteaza_si_elimina(tabla):
    scor = 0
    de_eliminat = []


    for i in range(RANDURI):
        for j in range(COLOANE - 2):
            if tabla[i][j] == tabla[i][j + 1] == tabla[i][j + 2] != 0:
                de_eliminat.append((i, j))
                de_eliminat.append((i, j + 1))
                de_eliminat.append((i, j + 2))
                scor += SCORURI['linie_3']


    for i in range(RANDURI - 2):
        for j in range(COLOANE):
            if tabla[i][j] == tabla[i + 1][j] == tabla[i + 2][j] != 0:
                de_eliminat.append((i, j))
                de_eliminat.append((i + 1, j))
                de_eliminat.append((i + 2, j))
                scor += SCORURI['linie_3']

    for (i, j) in de_eliminat:
        tabla[i][j] = 0

    return scor, tabla


def actualizeaza_tabla(tabla):
    for j in range(COLOANE):
        coloana = [tabla[i][j] for i in range(RANDURI) if tabla[i][j] != 0]
        coloana = [0] * (RANDURI - len(coloana)) + coloana
        for i in range(RANDURI):
            tabla[i][j] = coloana[i]
    return tabla


def simuleaza_joc():
    tabla = initializeaza_tabla()
    scor_total = 0
    mutari = 0

    while mutari < 10000:
        scor, tabla = detecteaza_si_elimina(tabla)
        if scor == 0:
            break
        scor_total += scor
        tabla = actualizeaza_tabla(tabla)
        mutari += 1

    return scor_total, mutari

def simuleaza_jocuri_multiple(n=100):
    scor_total = 0
    mutari_total = 0
    for _ in range(n):
        scor, mutari = simuleaza_joc()
        scor_total += scor
        mutari_total += mutari

    scor_mediu = scor_total / n
    mutari_medii = mutari_total / n
    return scor_mediu, mutari_medii


scor_mediu, mutari_medii = simuleaza_jocuri_multiple()
print(f"Scor mediu: {scor_mediu}")
print(f"Numar mediu de mutari: {mutari_medii}")
