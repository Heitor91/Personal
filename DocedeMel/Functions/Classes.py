from DocedeMel.Database.SQL import query_insert, query_select


def str_sql_set(text: str):
    return text.join(['\'', '\''])


class CADMateriaPrima:
    def __init__(self, formulario: dict):
        self.nome = self.carrega_dados(formulario, 0)
        self.fabricante = self.carrega_dados(formulario, 1)
        self.classificacao = self.carrega_dados(formulario, 2)
        self.descricao = self.carrega_dados(formulario, 3)
        self.valor = self.carrega_dados(formulario, 4)
        self.unidade = self.carrega_dados(formulario, 5)
        self.quantidade = self.carrega_dados(formulario, 6)
        self.valor_unitario = self.carrega_dados(formulario, 7)

    @classmethod
    def carrega_dados(cls, dados, index):
        chaves = ('nome', 'fabr', 'clas', 'desc', 'valor', 'unid', 'quant', 'v_un')
        return str_sql_set(dados[chaves[index]]) if type(dados[chaves[index]]) is str else str(dados[chaves[index]])

    def db_setter(self):
        dados = {'Nome': self.nome, 'Fabricante': self.fabricante, 'Classificacao': self.classificacao,
                 'Valor': self.valor, 'Quantidade': self.quantidade, 'Unidade': self.unidade,
                 'Val_Unitario': self.valor_unitario, 'Descricao': self.descricao}
        query_insert(tabela='Base_MPrima', dados=dados)

    def db_getter(self):
        pass


class CADFabricante:
    def __init__(self, idfab=None, nome=None, ramo=None):
        self.idfab = idfab
        self.nome = nome
        self.ramo = ramo

    def db_setter(self):
        dados = {'Nome': str_sql_set(self.nome), 'Ramo': str_sql_set(self.ramo)}
        query_insert(tabela='Base_Fabricantes', dados=dados)

    def db_getter(self):
        db_table = 'Base_Fabricantes'
        if self.nome is None:
            pass
        elif self.ramo is None and self.nome and self.idfab is None:
            self.idfab = query_select(tabela=db_table,
                                      colunas='ID',
                                      condicao=f'Nome = {str_sql_set(self.nome)}')
            return self.idfab
        elif self.nome and self.idfab and self.ramo is None:
            self.ramo = query_select(tabela=db_table,
                                     colunas='Ramo',
                                     condicao=f'ID = {self.idfab}')
