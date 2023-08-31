from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from DocedeMel.Database.SQL import query_insert, query_select


def str_sql_set(text: str):
    """
    Retorna sequencia em formato string para usar em uma query text ao buscar um determinado item no banco de dados.
    :param text:
    :return:
    """
    return text.join(['\'', '\''])


class CADMateriaPrima:
    """
    Classe resposável por gerenciar os dados do formulário de matéria-prima.
    """

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
    """
    Gerencia o cadastro de fabricantes
    """

    def __init__(self, idfab=None, nome=None, ramo=None):
        self.dialog = None
        self.db_table = 'Base_Fabricantes'
        self.idfab = idfab
        self.nome = nome
        self.ramo = ramo

    def db_setter(self):
        dados = {'Nome': str_sql_set(self.nome), 'Ramo': str_sql_set(self.ramo)}
        query_insert(tabela='Base_Fabricantes', dados=dados)
        self.db_getter_id_w_nome()

    def db_getter_id_w_nome(self):
        result = query_select(tabela=self.db_table,
                              colunas='ID',
                              condicao=f'Nome = {str_sql_set(self.nome)}')
        self.idfab = result[0][0] if len(result) == 1 else result

    def db_getter_ramo_w_id(self):
        self.ramo = query_select(tabela=self.db_table,
                                 colunas='Ramo',
                                 condicao=f'ID = {self.idfab}')

    def db_getter_nome_w_id(self):
        pass

    def popup_cadfab(self):
        print('LOG:POPCadastrar')
        self.dialog = MDDialog(title="Cadastrar empresa:",
                               type="custom",
                               content_cls=MDBoxLayout(MDTextField(id="fabnomcad",
                                                                   hint_text="Fabricante",
                                                                   text=self.nome,
                                                                   readonly=True),
                                                       MDBoxLayout(
                                                           MDCheckbox(id="consumiveis_checkbox", group="ramo", ),
                                                           MDLabel(text="Consumíveis"),
                                                           MDCheckbox(id="embalagens_checkbox", group="ramo"),
                                                           MDLabel(text="Embalagens"),
                                                           orientation="horizontal",
                                                           spacing="10dp",
                                                           size_hint_y=None,
                                                           height="40dp"),
                                                       orientation="vertical",
                                                       spacing="12dp",
                                                       size_hint_y=None,
                                                       height="120dp", ),
                               buttons=[MDFlatButton(text="Cancelar", on_release=lambda x: self.close()),
                                        MDRaisedButton(text="Cadastrar",
                                                       on_release=lambda x: self.cadastra(consumivel=self.dialog.content_cls.ids.consumiveis_checkbox.active)
                                                       )
                                        ]
                               )
        print(self.nome)
        self.dialog.open()

    def popup_confab(self):
        print('LOG:POPConfirmacao')
        self.db_getter_ramo_w_id()
        self.dialog = MDDialog(text=f"{self.nome} já está cadastrado",
                               buttons=[MDRaisedButton(text="Ok", on_release=lambda x: self.close())],
                               auto_dismiss=True)
        self.dialog.open()

    def popup_opcfab(self):
        print('LOG:POPEscolher')
        self.dialog = MDDialog(
            title="Mais de um fabricante encontrado:",
            buttons=[MDFlatButton(text="Cancelar", on_release=self.close),
                     MDRaisedButton(text="Cadastrar")]
        )
        self.dialog.open()

    def cadastra(self, **kwargs):
        print("Start_CADASTRO")
        self.ramo = "Consumíveis" if kwargs.get("consumivel",False) else "Embalagens"
        print(self.nome, self.ramo)
        self.db_setter()
        self.close()

    def close(self, *args):
        return self.dialog.dismiss(force=True)


class CADEmbalagem:
    def __init__(self, formulario: dict):
        self.nome = self.carrega_dados(dados=formulario, index=0)
        self.fabricante = self.carrega_dados(dados=formulario, index=0)
        self.tipo_dim = self.carrega_dados(dados=formulario, index=0)
        self.dimensao = self.carrega_dados(dados=formulario, index=0)
        self.quantidade = self.carrega_dados(dados=formulario, index=0)
        self.valor = self.carrega_dados(dados=formulario, index=0)
        self.val_unitario = self.carrega_dados(dados=formulario, index=0)
        self.descricao = self.carrega_dados(dados=formulario, index=0)

    @classmethod
    def carrega_dados(cls, dados, index):
        chaves = ('nome', 'fabr', 'clas', 'desc', 'valor', 'unid', 'quant', 'v_un')
        return str_sql_set(dados[chaves[index]]) if type(dados[chaves[index]]) is str else str(dados[chaves[index]])
