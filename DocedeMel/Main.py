from kivy.metrics import dp
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from DocedeMel.Functions.Classes import CADMateriaPrima as cadMP, CADFabricante as cadF
from DocedeMel.Database.SQL import query_create
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window, WindowBase


class ScreenControl(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, transition=NoTransition(), **kwargs)


def startsqlite():
    """
    Rotina que checa a existência das tabelas, caso não exista, cria as tabelas no data base.
    :return:None
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
    """
    Classe do formulário gráfico do cadastro de matérias-primas. Inicializa a variável auto instanciado
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fabricante = cadF()
        self.menu = None

    def perform_actions(self):
        self.mp_erase()  # Chama o método mp_erase
        self.manager.current = 'menu_principal'

    # Trecho de controle do item classificação
    def lista_class(self):
        menu_items = [{"viewclass": "OneLineListItem",
                       "text": f"{item}",
                       "height": dp(35),
                       "on_release": lambda x=f"{item}": self.set_class(x),
                       } for item in ['Animal', 'Planta', 'Outro']
                      ]
        self.menu = MDDropdownMenu(
            caller=self.ids.clas_cadmp,
            items=menu_items,
            position="bottom",
            width_mult=2, )
        self.menu.open()
        self.menu.bind()

    def set_class(self, text_item):
        self.ids.clas_cadmp.set_item(text_item)
        self.menu.dismiss()

    def lista_unidade(self):
        menu_items = [{"viewclass": "OneLineListItem",
                       "text": f"{item}",
                       "height": dp(35),
                       "on_release": lambda x=f"{item}": self.set_unidade(x),
                       } for item in ['Kg', 'g', 'L', 'mL', 'm³', 'mm³']
                      ]
        self.menu = MDDropdownMenu(
            caller=self.ids.unid_cadmp,
            items=menu_items,
            position="bottom",
            width_mult=1.5, )
        self.menu.open()
        self.menu.bind()

    def set_unidade(self, text_item):
        self.ids.unid_cadmp.set_item(text_item)
        self.menu.dismiss()

    def call_busca_fab(self):
        """
        Efetua busca no banco de dados e retorna os dados encontrados.
        :return: None
        """
        busca_fab(input_nome=self.ids.fabr_cadmp.text)

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
            self.ids.clas_cadmp.text,
            self.ids.desc_cadmp.text,
            self.ids.real_cadmp.text,
            self.ids.unid_cadmp.text,
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
        Limpa campos do formulário e reinicializa o objeto instanciado.
        :return:
        """
        self.ids.nome_cadmp.text = ''
        self.ids.fabr_cadmp.text = ''
        self.ids.clas_cadmp.text = '(Classe Produto)'
        self.ids.desc_cadmp.text = ''
        self.ids.real_cadmp.text = ''
        self.ids.qtdd_cadmp.text = ''
        self.ids.unid_cadmp.text = '(UN)'
        self.fabricante.nome = None
        self.fabricante.ramo = None
        self.fabricante.idfab = None


class CadastroEm(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fabricante = cadF()

    def perform_actions(self):
        self.mp_erase()  # Chama o método mp_erase
        self.manager.current = 'menu_principal'
    def emb_capture(self):
        pass

    def emb_erase(self):
        pass


class ProducaoRec(MDScreen):
    def perform_actions(self):
        self.mp_erase()  # Chama o método mp_erase
        self.manager.current = 'menu_principal'


class ProducaoCho(MDScreen):
    def perform_actions(self):
        self.mp_erase()  # Chama o método mp_erase
        self.manager.current = 'menu_principal'


class ProducaoPro(MDScreen):
    def perform_actions(self):
        self.mp_erase()  # Chama o método mp_erase
        self.manager.current = 'menu_principal'


class MyerpApp(MDApp):
    """

    """

    def build(self):
        startsqlite()
        Window.fullscreen = True
        WindowBase.fullscreen = 'auto'
        return ScreenControl()


def busca_fab(**kwargs):
    """
    Efetua busca no banco de dados e retorna os dados encontrados.
    :return: None
    """
    fabricante = cadF()
    fabricante.nome = kwargs["input_nome"]
    fabricante.db_getter_id_w_nome()
    print(fabricante.nome, fabricante.ramo)
    print(fabricante.idfab)
    if type(fabricante.idfab) is int:
        fabricante.idfab = fabricante.idfab
        fabricante.popup_confab()
    elif type(fabricante.idfab) == list and len(fabricante.idfab) == 0:
        fabricante.popup_cadfab()
    else:
        fabricante.popup_opcfab()


if __name__ == '__main__':
    MyerpApp().run()
    """
    RosaSuave	    [0.98, 0.612, 0.98, 1]
    Chocolate	    [0.43, 0.07, 0.06, 1]
    VerdePastel	    [0.54, 1, 0.83, 1]
    AmareloPastel	[1, 1, 0.54, 1]"""
"""Comentários sobre o uso de comandos de botões: Quando você usa um lambda para envolver a chamada de um método em 
Python, você cria uma função anônima que encapsula a chamada. Essa função anônima mantém uma referência ao contexto 
em que foi definida, o que inclui o valor atual das variáveis locais no momento da definição. Ao passar essa função 
anônima como argumento para um evento, como o on_release do KivyMD, ela é executada quando o evento ocorre. Nesse 
momento, a função anônima tem acesso às variáveis locais capturadas no momento da definição, incluindo a referência 
correta ao objeto self. Por outro lado, ao chamar diretamente um método sem o uso de lambda, a chamada é feita 
imediatamente e o valor atual da variável self no momento da chamada é usado. Isso pode causar problemas se a 
referência a self não estiver corretamente associada ao objeto desejado. Ao usar o lambda, você cria uma função 
intermediária que "embala" a chamada do método e garante que ela seja executada no contexto correto, preservando a 
referência correta ao objeto self da classe. Essa abordagem com lambda garante que a chamada do método close ou 
cadastra ocorra com a referência correta a self, permitindo que o método seja executado corretamente. É importante 
ressaltar que outras variáveis e fatores podem influenciar o resultado, e é fundamental revisar cuidadosamente o 
código para garantir que todas as referências e chamadas de métodos estejam corretamente configuradas."""