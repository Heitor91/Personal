from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from DocedeMel.Functions.Classes import CADMateriaPrima as cadMP, CADFabricante as cadF
from DocedeMel.Database.SQL import query_create
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, CheckboxLeftWidget


class ScreenControl(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def startsqlite():
    """

    :return:
    """
    db_struct = {'Base_Fabricantes': ('ID INTEGER PRIMARY KEY',
                                      'Nome TEXT',
                                      'Ramo TEXT'),
                 'Classificacao_Consumiveis': ('ID INTEGER PRIMARY KEY',
                                               'Nome TEXT'),
                 'Base_Embalagens': ('ID INTEGER PRIMARY KEY',
                                     'Nome TEXT',
                                     'Fabricante INTEGER ',
                                     'Tipo_DIM INTEGER ',
                                     'Dimensao TEXT',
                                     'Quantidade INTEGER',
                                     'Valor REAL',
                                     'Val_Unitario REAL',
                                     'Descricao TEXT',
                                     'FOREIGN KEY(Fabricante) '
                                     'REFERENCES Base_Fabricantes(ID)'),
                 'Base_MPrima': ('ID INTEGER PRIMARY KEY',
                                 'Nome TEXT',
                                 'Fabricante INTEGER ',
                                 'Classificacao INTEGER ',
                                 'Valor REAL',
                                 'Quantidade INTEGER',
                                 'Unidade TEXT',
                                 'Val_Unitario REAL',
                                 'Descricao TEXT',
                                 'FOREIGN KEY(Fabricante) '
                                 'REFERENCES Base_Fabricantes(ID)',
                                 'FOREIGN KEY(Classificacao) '
                                 'REFERENCES Classificacao_Consumiveis(ID)'),
                 'Base_Recheios': ('ID INTEGER PRIMARY KEY',
                                   'Tipo TEXT',
                                   'FOREIGN KEY(Tipo) '
                                   'REFERENCES Classificacao_Consumiveis(ID)'),
                 'Itens_Embalagens': ('ID INTEGER PRIMARY KEY',
                                      'Embalagem INTEGER',
                                      'Quantidade INTEGER',
                                      'Produto INTEGER',
                                      'FOREIGN KEY(Embalagem)'
                                      'REFERENCES Base_Embalagens(ID)',
                                      'FOREIGN KEY(Produto)'
                                      'REFERENCES Base_Produtos(ID)'),
                 'Base_Coberturas': ('ID INTEGER PRIMARY KEY',
                                     'Nome TEXT',
                                     'MPrima INTEGER',
                                     'Peso INTEGER',
                                     'FOREIGN KEY(MPrima)'
                                     'REFERENCES Base_MPrima(ID)'),
                 'Base_Receitas': ('ID INTEGER PRIMARY KEY',
                                   'Nome TEXT',
                                   'MPrima INTEGER',
                                   'Recheio INTEGER',
                                   'FOREIGN KEY(MPrima)'
                                   'REFERENCES Base_MPrima(ID)',
                                   'FOREIGN KEY(Recheio)'
                                   'REFERENCES Base_Recheios(ID)'),
                 'Base_Consumíveis': ('ID INTEGER PRIMARY KEY',
                                      'Nome TEXT',
                                      'Cobertura INTEGER',
                                      'Recheio INTEGER',
                                      'PesoRecheio INTEGER',
                                      'PesoTotal INTEGER',
                                      'FOREIGN KEY(Cobertura)'
                                      'REFERENCES Base_Coberturas(ID)',
                                      'FOREIGN KEY(Recheio)'
                                      'REFERENCES Base_Recheios(ID)'),
                 'Base_Produtos': ('ID INTEGER PRIMARY KEY',
                                   'Nome TEXT',
                                   'Consumivel INTEGER',
                                   'QtdConsumivel INT',
                                   'MaoDeObra REAL',
                                   'Margem REAL',
                                   'FOREIGN KEY(Consumivel)'
                                   'REFERENCES Base_Consumíveis(ID)')
                 }
    for chave in db_struct:
        print(f'Criando:{chave}')
        query_create(tabela=chave, colunas=db_struct[chave])


class MenuPrincipal(MDScreen):
    pass


class CadFabPop(MDBoxLayout):
    pass


class CadastroMP(MDScreen):
    dialog = None
    fabricante = cadF()

    def busca_fab(self):
        """
        Efetua busca no banco de dados e retorna os dados encontrados.
        :return: None
        """
        self.fabricante.nome = self.ids.fabr_cadmp.text
        result = self.fabricante.db_getter()
        print(self.fabricante.nome, self.fabricante.ramo)
        print(result)
        if len(result) == 1:
            self.fabricante.idfab = self.fabricante.idfab[0]
            self.popup_confab()
        elif len(result) == 0:
            self.popup_cadfab()
        else:
            self.popup_chofab()

    def cadastra(self, *args):
        self.fabricante.ramo = self.dialog.content_cls.ids.fabramcad.text
        print(self.fabricante.nome, self.fabricante.ramo)
        self.fabricante.db_setter()
        self.close()

    def close(self, *args):
        return self.dialog.dismiss(force=True)

    def popup_cadfab(self):
        print('LOG:POPCadastrar')
        print(self.fabricante.nome)
        self.dialog = MDDialog(title="Cadastrar empresa:",
                               type="custom",
                               content_cls=MDBoxLayout(MDTextField(id="fabnomcad",
                                                                   hint_text="Fabricante",
                                                                   text=self.fabricante.nome),
                                                       MDTextField(id="fabramcad",
                                                                   hint_text="Ramo", ),
                                                       orientation="vertical",
                                                       spacing="12dp",
                                                       size_hint_y=None,
                                                       height="120dp", ),
                               buttons=[MDFlatButton(text="Cancelar", on_release=self.close),
                                        MDRaisedButton(text="Cadastrar",
                                                       on_release=self.cadastra
                                                       )
                                        ]
                               )
        self.dialog.open()

    def popup_confab(self):
        print('LOG:POPConfirmacao')
        self.fabricante.db_getter()
        self.dialog = MDDialog(text=f"{self.fabricante.nome} já está cadastrado",
                               buttons=[MDRaisedButton(text="Ok", on_release=self.close)])
        self.dialog.open()

    def popup_chofab(self):
        print('LOG:POPEscolher')
        dialog = MDDialog(
            title="Mais de um fabricante encontrado:",
            buttons=[MDFlatButton(text="Cancelar", on_release=self.close),
                     MDRaisedButton(text="Cadastrar")]
        )
        self.dialog.open()

    # Captura dos dados para gravar na base de matéria-prima

    def mp_capture(self):
        """
        Chamada por ação de um botão no arquivo kv, realiza a captura dos textos do usuário e grava
        no banco de dados utilizando chaves já definidas. Caso não consiga grava um log. no console
        com o erro.
        :returns:None
        """
        chaves = ('nome', 'fabr', 'clas', 'desc', 'valor', 'unid', 'quant', 'v_un')
        valores = [
            self.ids.nome_cadmp.text,
            self.fabricante.idfab,
            '1',
            self.ids.desc_cadmp.text,
            self.ids.real_cadmp.text,
            'ml',
            self.ids.qtdd_cadmp.text,
            float(self.ids.real_cadmp.text) / int(self.ids.qtdd_cadmp.text)
        ]
        try:
            dados = cadMP(dict(zip(chaves, valores)))
            dados.db_setter()
        except AttributeError as e:
            print(f'ERRO NOS DADOS:{e}')
        else:
            print(dados.nome)
            print(dados.fabricante)
            print(dados.classificacao)
            print(dados.descricao)
            print(dados.valor)
            print(dados.quantidade)
            self.mp_erase()

    def mp_erase(self):
        """
        Limpa campos do formulário
        :return:
        """
        self.ids.nome_cadmp.text = ''
        self.ids.fabr_cadmp.text = ''
        self.ids.desc_cadmp.text = ''
        self.ids.real_cadmp.text = ''
        self.ids.qtdd_cadmp.text = ''


class CadastroEm(MDScreen):
    pass


class ProducaoRec(MDScreen):
    pass


class ProducaoCho(MDScreen):
    pass


class ProducaoPro(MDScreen):
    pass


class MyerpApp(MDApp):
    """

    """

    def build(self):
        startsqlite()
        return ScreenControl()


if __name__ == '__main__':
    MyerpApp().run()
    """
    RosaSuave	    [0.98, 0.612, 0.98, 1]
    Chocolate	    [0.43, 0.07, 0.06, 1]
    VerdePastel	    [0.54, 1, 0.83, 1]
    AmareloPastel	[1, 1, 0.54, 1]"""
