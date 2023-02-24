import sqlite3
from sqlite3 import Error


def str_sql_split(*args):
    return ",".join(args)


def commit(script):
    """
    Faz a conexão com a base de dados SQLite e executa a função decorada que retorna a query SQL.
    :param script: função decorada.
    :return: None
    """
    database = None
    try:
        database = sqlite3.connect(r'C:\Users\KV334VU\PycharmProjects\Personal\DocedeMel\docedemel.db')
        db_cursor = database.cursor()
        db_cursor.execute(script)
        database.commit()
        print(f'Commit realizado')
        if 'SELECT' in script:
            return db_cursor.fetchall()
    except Error as e:
        print(f'Não foi possível acessar o db\n{e}')
    finally:
        if database:
            database.close()


def query_select(**kwargs):
    """
    Constrói a query que executa a consulta das tabelas.
    SELECT
        <COLUNAS(Opcional-)>
    FROM
        <TABLE>
    (INNER, OUTTER, LEFT, RIGHT)
    WHERE
        <EXPRESSION>
    GROUP BY
        <ELEMENTS>
    ORDER BY
        <ELEMENTS>
    :return:
    """
    query_text = 'SELECT '

    # Estabelece as colunas
    if kwargs['colunas'] is None:
        query_text += '*'
    elif type(kwargs['colunas']) is str:
        query_text += f"{kwargs['colunas']} "
    else:
        query_text += f"{str_sql_split(kwargs['colunas'])} "

    # Estabelece a tabela
    query_text += f"FROM {kwargs['tabela']} "

    # Estabelece a condição
    if kwargs['condicao'] is None:
        query_text += ''
    elif type(kwargs['condicao']) is str:
        query_text += f"WHERE {kwargs['condicao']}"
    else:
        query_text += f"WHERE {str_sql_split(kwargs['condicao'])}"
    print(query_text)
    return commit(query_text)


def query_create(tabela: str, colunas: tuple):
    print(f'Query Pronta....')
    commit(f'CREATE TABLE IF NOT EXISTS {tabela}({",".join(colunas)})')


def query_delete():
    pass


def query_insert(tabela: str, dados: dict):
    """
    Alterar a formatação da ‘string’ para acrescentar as aspas.
    :param tabela:
    :param dados:
    :return:
    """
    query_text = f'INSERT INTO {tabela} ({",".join(tuple(dados.keys()))}) ' \
                 f'VALUES({",".join(tuple(dados.values()))})'
    print(query_text)
    commit(query_text)
