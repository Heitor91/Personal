from random import shuffle, choice


def mega():
    numeros_mega = list(range(1, 61))
    return numeros_mega


def sorteio():
    globo = mega()
    volante = []
    while len(volante) < 6:
        for n in range(20):
            shuffle(globo)
        volante.append(globo[0])
        globo.pop(0)
    volante.sort()
    return volante


apostas = int(input("nº de apostas:"))
volantes = {}
for i in range(apostas):
    volantes[i+1] = sorteio()
for aposta in volantes:
    print(volantes[aposta])
