from DocedeMel.Database.SQL import query_insert, commit
from DocedeMel.Functions.Classes import str_sql_set


def fabricantes(nome: str, qtype: str, ramo='indefinido'):
    if qtype == 'con':
        return commit(f'SELECT ID, Nome FROM Base_Fabricantes WHERE Nome = \'{nome.capitalize()}\'')
    if qtype == 'cad':
        query_insert(tabela='Base_Fabricantes', dados={'Nome': str_sql_set(nome),
                                                       'Ramo': ramo.capitalize()})
