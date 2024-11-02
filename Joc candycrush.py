import random

RANDURI, COLOANE = 11, 11

# codurile de puncte pentru culori
GOL, ROSU, GALBEN, VERDE, ALBASTRU = 0, 1, 2, 3, 4

# scorurile pentru fiecare tip de formatie
PUNCTAJ = {
    "linie_3": 5,
    "linie_4": 10,
    "linie_5": 50,
    "forma_L": 20,
    "forma_T": 30
}

# initializarea tablei de joc cu bomboane aleatorii
def initializare_tabla():
    tabla = [[random.choice([ROSU, GALBEN, VERDE, ALBASTRU]) for _ in range(COLOANE)] for _ in range(RANDURI)]
    return tabla

# afisarea tablei
def afisare_tabla(tabla):
    for rand in tabla:
        print(' '.join(str(celula) for celula in rand))
    print("=" * 30)

# detectarea formatiilor orizontale si verticale de 3, 4 sau 5 bomboane
def gaseste_formatiuni(tabla):
    formatiuni = []

    # detectare linii orizontale
    for i in range(RANDURI):
        for j in range(COLOANE - 2):
            if tabla[i][j] == tabla[i][j + 1] == tabla[i][j + 2] != GOL:
                lungime = 3
                if j + 3 < COLOANE and tabla[i][j] == tabla[i][j + 3]:
                    lungime = 4
                if j + 4 < COLOANE and tabla[i][j] == tabla[i][j + 4]:
                    lungime = 5
                formatiuni.append(((i, j), lungime, 'orizontal'))

    # detectare linii verticale
    for j in range(COLOANE):
        for i in range(RANDURI - 2):
            if tabla[i][j] == tabla[i + 1][j] == tabla[i + 2][j] != GOL:
                lungime = 3
                if i + 3 < RANDURI and tabla[i][j] == tabla[i + 3][j]:
                    lungime = 4
                if i + 4 < RANDURI and tabla[i][j] == tabla[i + 4][j]:
                    lungime = 5
                formatiuni.append(((i, j), lungime, 'vertical'))

    return formatiuni

# detectarea formatiunilor de tip "L" si "T"
def gaseste_forme_LT(tabla):
    formatiuni_LT = []

    # verificare forma "L" si "T"
    for i in range(RANDURI - 2):
        for j in range(COLOANE - 2):

            if tabla[i][j] == tabla[i + 1][j] == tabla[i + 2][j] == tabla[i][j + 1] != GOL:
                formatiuni_LT.append(((i, j), 'L'))
            elif tabla[i][j] == tabla[i][j + 1] == tabla[i][j + 2] == tabla[i + 1][j] != GOL:
                formatiuni_LT.append(((i, j), 'L'))


            if tabla[i][j + 1] == tabla[i + 1][j] == tabla[i + 1][j + 1] == tabla[i + 1][j + 2] == tabla[i + 2][j + 1] != GOL:
                formatiuni_LT.append(((i, j + 1), 'T'))

    return formatiuni_LT

# eliminarea bomboanelor din formatiile gasite
def elimina_formatiuni(tabla, formatiuni):
    punctaj = 0
    for (start, lungime, directie) in formatiuni:
        x, y = start
        if directie == 'orizontal':
            for j in range(y, y + lungime):
                tabla[x][j] = GOL
        elif directie == 'vertical':
            for i in range(x, x + lungime):
                tabla[i][y] = GOL

        # adauga punctaj in functie de lungimea formatiei
        if lungime == 3:
            punctaj += PUNCTAJ["linie_3"]
        elif lungime == 4:
            punctaj += PUNCTAJ["linie_4"]
        elif lungime == 5:
            punctaj += PUNCTAJ["linie_5"]

    return punctaj

# eliminarea formatiilor in forma de "L" si "T"
def elimina_forme_LT(tabla, formatiuni_LT):
    punctaj = 0
    for (start, tip_forma) in formatiuni_LT:
        x, y = start
        tabla[x][y] = GOL
        tabla[x + 1][y] = GOL
        tabla[x + 2][y] = GOL
        tabla[x][y + 1] = GOL
        if tip_forma == 'T':
            tabla[x + 1][y + 1] = GOL
            punctaj += PUNCTAJ["forma_T"]
        else:
            punctaj += PUNCTAJ["forma_L"]
    return punctaj

# aducerea bomboanelor in jos dupa eliminarea formatiilor
def cadere_bomboane(tabla):
    for j in range(COLOANE):
        coloana = [tabla[i][j] for i in range(RANDURI) if tabla[i][j] != GOL]
        coloana = [GOL] * (RANDURI - len(coloana)) + coloana
        for i in range(RANDURI):
            tabla[i][j] = coloana[i]

# verifica si realizeaza mutari posibile care aduc un scor imediat
def mutari_si_scor(tabla):
    for i in range(RANDURI):
        for j in range(COLOANE - 1):
            tabla[i][j], tabla[i][j + 1] = tabla[i][j + 1], tabla[i][j]
            if gaseste_formatiuni(tabla) or gaseste_forme_LT(tabla):
                return True
            tabla[i][j], tabla[i][j + 1] = tabla[i][j + 1], tabla[i][j]

    for j in range(COLOANE):
        for i in range(RANDURI - 1):
            tabla[i][j], tabla[i + 1][j] = tabla[i + 1][j], tabla[i][j]
            if gaseste_formatiuni(tabla) or gaseste_forme_LT(tabla):
                return True
            tabla[i][j], tabla[i + 1][j] = tabla[i + 1][j], tabla[i][j]

    return False

# ruleaza un joc complet
def joaca_joc():
    tabla = initializare_tabla()
    punctaj_total = 0
    mutari = 0

    print("Tabla initiala:")
    afisare_tabla(tabla)

    while punctaj_total < 10000:
        formatiuni = gaseste_formatiuni(tabla)
        formatiuni_LT = gaseste_forme_LT(tabla)

        if formatiuni or formatiuni_LT:
            punctaj_total += elimina_formatiuni(tabla, formatiuni)
            punctaj_total += elimina_forme_LT(tabla, formatiuni_LT)
            cadere_bomboane(tabla)
            mutari += 1
            print(f"Scor: {punctaj_total}, Mutari: {mutari}")
            afisare_tabla(tabla)
        elif mutari_si_scor(tabla):
            mutari += 1
        else:
            break

    print("Scor final:", punctaj_total)
    return punctaj_total, mutari

# simuleaza 100 de jocuri si a calculeaza media punctajului si a numarului de mutari
def simuleaza_jocuri(numar_jocuri=100):
    punctaje = []
    total_mutari = 0

    for _ in range(numar_jocuri):
        punctaj, mutari = joaca_joc()
        punctaje.append(punctaj)
        total_mutari += mutari

    scor_mediu = sum(punctaje) / numar_jocuri
    mutari_medii = total_mutari / numar_jocuri
    return punctaje, scor_mediu, mutari_medii

rezultate_simulare = simuleaza_jocuri(100)

punctaje, scor_mediu, mutari_medii = rezultate_simulare
print("Punctaje individuale:", punctaje)
print("Scor mediu pe joc:", scor_mediu)
print("Numar mediu de mutari pe joc:", mutari_medii)