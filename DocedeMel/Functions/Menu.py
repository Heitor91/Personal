from DocedeMel.Ajuda import ajuda
from os import system
from DocedeMel.Functions.Cadastro import materia_prima


def embalagens():
    pass


def cadastros():  # Menu > cadastros
    """
    Função para direcionador os tipos dos cadastros entre matéria-prima e embalagens.:return:
    """
    funcao = (None, materia_prima, embalagens, ajuda)
    while True:
        system("cls")
        print("MENU>CADASTROS")
        op = int(input("1-Materia Prima\n2-Embalagem\n3-Ajuda\n0-Sair\n>"))
        if funcao[op] is None:
            break
        elif 0 > op > 3:
            print("Opção invalida!Tente novamente")
        else:
            funcao[op]()
