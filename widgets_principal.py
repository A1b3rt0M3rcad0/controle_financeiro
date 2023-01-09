import customtkinter
import tkinter as tk
import bd
import pandas as pd

class CriarCategoria(customtkinter.CTkFrame):

    def __init__(self, *args, username, password, carteira_id, app, **kwargs):
        super().__init__(*args, **kwargs)
        self.USERNAME = username
        self.PASSWORD = password
        self.CARTEIRA_ID = carteira_id
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.APP = app
        self.DESCRICAO = None
        ## tipo categoria ##
        self.combobox = customtkinter.CTkComboBox(master=self, values=['Entrada', 'Saida'], width=25*self.WIDTH, height=self.HEIGHT)
        self.combobox.grid(row=0, column=0, padx=self.PADX, pady=self.PADY, columnspan=3)
        ## nome entry ##
        self.nome_categoria_entry = customtkinter.CTkEntry(master=self, width=15*self.WIDTH, height=self.HEIGHT)
        self.nome_categoria_entry.grid(row=1, column=1, padx=self.PADX, pady=self.PADY)
        ## nome categoria ##
        self.nome_categoria_label = customtkinter.CTkLabel(master=self, text='Nome:', width=self.WIDTH, height=self.HEIGHT)
        self.nome_categoria_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)
        ## button ##
        self.nome_categoria_entry_button = customtkinter.CTkButton(master=self, text='confirmar', width=self.WIDTH, height=self.HEIGHT, command=self.criar_categoria)
        self.nome_categoria_entry_button.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)
    
    def criar_categoria(self):
        self.nome_categoria = self.nome_categoria_entry.get()
        self.descricao = 'None'
        self.tipo = self.combobox.get()
        if self.tipo == 'Entrada':
            resultado = bd.criar_categoria(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, 'e', self.nome_categoria,self.descricao)
            self.APP.selecionar_carteira()
            MsgMovimentarSaldo(resultado)
        elif self.tipo == 'Saida':
            resultado = bd.criar_categoria(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, 's', self.nome_categoria,self.descricao)
            self.APP.selecionar_carteira()
            MsgMovimentarSaldo(resultado)
        else:
            MsgMovimentarSaldo('Error: criar_categoria() parameer "Tipo"')
###### Deletar Categorias #######################################################################################################################################
class DeletarCategorias(customtkinter.CTkFrame):
    def __init__(self, *args,  username, password, carteira_id, app, tipo, **kwargs):
        super().__init__(*args, **kwargs)
        self.USERNAME = username
        self.PASSWORD = password
        self.CARTEIRA_ID = carteira_id
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.TIPO = tipo
        self.APP = app
        self.lista = bd.ver_categorias_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, self.TIPO)
        # lista de categorias
        self.combobox = customtkinter.CTkComboBox(self, width=25*self.WIDTH, height=self.HEIGHT, values=self.lista)
        self.combobox.grid(column=0, row=0, padx=self.PADX, pady=self.PADY)
        self.button = customtkinter.CTkButton(self, text= 'Deletar', width=self.WIDTH, height=self.HEIGHT, command=self.deletar)
        self.button.grid(column=0, row=1)
    
    def deletar(self):
        categoria = self.combobox.get()
        categoria_selecionada = bd.ver_categorias_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, self.TIPO, retorno=None)
        categoria_selecionada = categoria_selecionada.loc[categoria_selecionada[2] == categoria][:][0]
        categoria_selecionada = categoria_selecionada.iloc[0]
        result = bd.deletar_categoria(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, int(categoria_selecionada), self.TIPO)
        self.APP.selecionar_carteira()
        if result == '1':
            MsgMovimentarSaldo('Categoria Deletada')
        else:
            MsgMovimentarSaldo(result)
###### Deletar Categorias #######################################################################################################################################

####### Trabsferir Saldo #######################################################################################################################################
class TransferirSaldo(customtkinter.CTkFrame):
    def __init__(self, *args, username, password, carteira_origem, app, **kwargs):
        super().__init__(*args, **kwargs)
        self.USERNAME = username
        self.PASSWORD = password
        self.CARTEIRA_ORIGEM = carteira_origem
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.APP = app
        # Carteira Destino
        self.entry = customtkinter.CTkEntry(self, width=15*self.WIDTH, height=self.HEIGHT)
        self.entry.grid(column=1, row=0, padx=self.PADX, pady=self.PADY)
        self.label = customtkinter.CTkLabel(self, text='ID Carteira Destino', width=5*self.WIDTH, height=self.HEIGHT)
        self.label.grid(column=0, row=0, padx=self.PADX, pady=self.PADY)
        # valor
        self.entry_valor = customtkinter.CTkEntry(self, width=15*self.WIDTH, height=self.HEIGHT)
        self.entry_valor.grid(column=1, row=1, padx=self.PADX, pady=self.PADY)
        self.label_valor = customtkinter.CTkLabel(self, text='Valor', width=5*self.WIDTH, height=self.HEIGHT)
        self.label_valor.grid(column=0, row=1, padx=self.PADX, pady=self.PADY)
        # Button
        self.button = customtkinter.CTkButton(self, text='Confirmar', width=self.WIDTH, height=self.HEIGHT, command=self.transferir)
        self.button.grid(column=0, row=2, columnspan=2)
    
    def transferir(self):
        carteira_destino = self.entry.get()
        valor = self.entry_valor.get()
        resultado = bd.transferir(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ORIGEM, carteira_destino, valor)
        self.APP.selecionar_carteira()
        MsgMovimentarSaldo(text=resultado)

####### Trabsferir Saldo #######################################################################################################################################


####### Adicionar e Retirar Saldo #######################################################################################################################################
class MsgMovimentarSaldo(customtkinter.CTk):
    def __init__(self, text):
        super().__init__()
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.label = customtkinter.CTkLabel(self, text=text, width=15*self.WIDTH, height=self.HEIGHT)
        self.label.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        self.button = customtkinter.CTkButton(self, text='OK', width=self.WIDTH, height=self.HEIGHT, command=self.destroy_window)
        self.button.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)
        self.mainloop()
    
    def destroy_window(self):
        self.destroy()


class MovimentarSaldo(customtkinter.CTkFrame):
    def __init__(self, *args, username, password, carteira_id, tipo, app, **kwargs):
        super().__init__(*args, **kwargs)
        # CONSTANTES
        self.USERNAME = username
        self.PASSWORD = password
        self.APP = app
        self.TIPO = tipo
        self.CARTEIRA_ID = carteira_id
        self.TIPO = tipo
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        # COMBO BOX
        self.categorias = bd.ver_categorias_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, self.TIPO)
        self.combobox = customtkinter.CTkComboBox(self, width=25*self.WIDTH, height=self.HEIGHT, values=self.categorias)
        self.combobox.grid(column=0, row=0, padx=self.PADX, pady=self.PADY, columnspan=3)
        # valor
            # Label
        self.valor = customtkinter.CTkLabel(self, width=self.WIDTH, height=self.HEIGHT, text='Valor: ')
        self.valor.grid(column=0, row=1, padx=self.PADX, pady=self.PADY)
            # Entry
        self.valor = customtkinter.CTkEntry(self, width=15*self.WIDTH, height=self.HEIGHT)
        self.valor.grid(column=1, row=1, padx=self.PADX, pady=self.PADY)
        # Button confirma
        self.button = customtkinter.CTkButton(self,text='Confirmar', width=self.WIDTH, height=self.HEIGHT, command=self.adicionar_retirar)
        self.button.grid(column=0, row=2, padx=self.PADX, pady=self.PADY, columnspan=3)
    
    def adicionar_retirar(self):
        if self.TIPO == 'e':
            valor = self.valor.get()
            self.valor.delete(0, customtkinter.END)
            try:
                valor = float(valor)
            except:
                return MsgMovimentarSaldo(text='Error: Value not correct')
            if valor == 0:
                return MsgMovimentarSaldo(text='Error: Null Value')
            categoria = self.combobox.get()
            categoria_id = bd.ver_categorias_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, self.TIPO, retorno=None)
            categoria_selecionada = categoria_id[0].loc[categoria_id[2] == categoria]
            print(categoria_selecionada)
            resultado = bd.adicionar_saldo(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_ID), int(categoria_selecionada), valor)
            self.APP.selecionar_carteira()
            return MsgMovimentarSaldo(text=resultado)
        else:
            valor = self.valor.get()
            self.valor.delete(0, customtkinter.END)
            try:
                valor = float(valor)
            except:
                return MsgMovimentarSaldo(text='Error: Value not correct')
            if valor == 0:
                return MsgMovimentarSaldo(text='Error: Null Value')
            categoria = self.combobox.get()
            categoria_id = bd.ver_categorias_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.CARTEIRA_ID, self.TIPO, retorno=None)
            categoria_selecionada = categoria_id[0].loc[categoria_id[2] == categoria]
            resultado = bd.retirar_saldo(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_ID), int(categoria_selecionada), valor)
            self.APP.selecionar_carteira()
            return MsgMovimentarSaldo(text=resultado)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.teste = DeletarCategorias(master = self, username='user3', password='abcdef',carteira_id=3 ,tipo='e', app=self)
        self.teste.grid(column=0, row=0)
        self.mainloop()
####### Adicionar e Retirar Saldo #######################################################################################################################################

if __name__ == '__main__':
       App()