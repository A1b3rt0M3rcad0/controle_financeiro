import customtkinter
import bd
import tkinter as tk
from tkinter import ttk
import widgets_principal as wp

arial24 = ('Arial', 24)
arial15 = ('Arial', 15)
arial18 = ('Arial', 18)
arial8 = ('Arial', 8)
name = 'Controle Financeiro'

######################################################################################################################
############################################ APP #####################################################################
######################################################################################################################

class App(customtkinter.CTk):
    def __init__(self, USERNAME, PASSWORD):
        super().__init__()
        # Constantes do APP
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.title(name)
        self.CARTEIRA_SELECIONADA = None
        self.resizable(False, False)
        # Cria o notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky='n')
        # Cria os widgets para as abas
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        # Adiciona os widgets ás abas
        self.notebook.add(self.tab1, text='Principal')
        self.notebook.add(self.tab2, text='Transações')
        self.notebook.add(self.tab3, text='Estatistícas')
        # Cria a frame de informações do usuario
        self.informacoes_usuario = tk.Frame(self)
        # Posiciona as frames de informações do usuario
        self.informacoes_usuario.grid(column=0, row=0, padx=self.PADX, pady= self.PADY)
        # Cria labels do frame de informações de usuario
            # Nome usuario
        self.nome = customtkinter.CTkLabel(self.informacoes_usuario, text=self.USERNAME, font=arial24, width=self.WIDTH, height=self.HEIGHT)
        self.nome.grid(column=0, row=0, padx=5*self.PADX, pady=self.PADY)
            # lista carteiras combobox
                ## Label COMBOBOX
        self.label_id = customtkinter.CTkLabel(self.informacoes_usuario, text='WALLET ID:', font=arial15, width=self.WIDTH, height=self.HEIGHT)
        self.label_id.grid(column=0, row=1, padx=5*self.PADX, pady=self.PADY)
                ## COMBOBOX
        self.carteiras = bd.ver_carteiras(bd.cnx(), self.USERNAME, self.PASSWORD)
        self.lista_carteiras = customtkinter.CTkComboBox(self.informacoes_usuario, values=self.carteiras, font=arial15, width=8*self.WIDTH, height=self.HEIGHT)
        self.lista_carteiras.grid(column=0, row=2, padx=5*self.PADX, pady=self.PADY)
            # Button selecionar carteira
        self.selecionar_atualizar = customtkinter.CTkButton(self.informacoes_usuario, text='Select/Update', command=self.selecionar_carteira)
        self.selecionar_atualizar.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)
        self.CARTEIRA_SELECIONADA = self.lista_carteiras.get()
            # Nome carteira
        self.nome_carteira_label = bd.ver_nome_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.nome_carteira = customtkinter.CTkLabel(self.informacoes_usuario, text=f'{self.nome_carteira_label}', font=arial18)
        self.nome_carteira.grid(column=0, row=4, padx=self.PADX, pady=self.PADY)
            # Saldo
        self.saldo_carteira_label = bd.ver_saldo_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.saldo_carteira = customtkinter.CTkLabel(self.informacoes_usuario, text=f'Saldo: {self.saldo_carteira_label}', width=8*self.WIDTH, height=self.HEIGHT, font=arial15)
        self.saldo_carteira.grid(column=0, row=5, padx=self.PADX, pady=self.PADY)
            # Space
        self.space = customtkinter.CTkLabel(self.informacoes_usuario, width=8*self.WIDTH, height=5*self.HEIGHT, text='')
        self.space.grid(column=0, row=6, padx=self.PADX, pady=self.PADY)
            # Detalhes da conta
        self.logout_button = customtkinter.CTkButton(self.informacoes_usuario, text='Account Details', width=8*self.WIDTH, height=self.HEIGHT)
        self.logout_button.grid(column=0, row=7, padx=self.PADX, pady=self.PADY)
            # Button Criar Carteira
        self.logout_button = customtkinter.CTkButton(self.informacoes_usuario, text='Create Wallet', width=8*self.WIDTH, height=self.HEIGHT)
        self.logout_button.grid(column=0, row=8, padx=self.PADX, pady=self.PADY)
            # Button Logout
        self.logout_button = customtkinter.CTkButton(self.informacoes_usuario, text='Logout', width=8*self.WIDTH, height=self.HEIGHT, command=self.logout)
        self.logout_button.grid(column=0, row=9, padx=self.PADX, pady=self.PADY)

        ######### widgets principal #########
            # adicionar saldo
        self.adicionar_saldo_name = customtkinter.CTkLabel(self.tab1, text='Adicionar Saldo', width=self.WIDTH, height=self.HEIGHT)
        self.adicionar_saldo_name.grid(column=0, row=0, padx=self.PADX, pady=self.PADY)
        self.adicionar_saldo = wp.MovimentarSaldo(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id=self.CARTEIRA_SELECIONADA, tipo='e', app=self)
        self.adicionar_saldo.grid(column=0, row=1, padx=self.PADX, pady=self.PADY)
            # retirar saldo
        self.retirar_saldo_name = self.adicionar_saldo_name = customtkinter.CTkLabel(self.tab1, text='Retirar Saldo', width=self.WIDTH, height=self.HEIGHT)
        self.retirar_saldo_name.grid(column=1, row=0, padx=self.PADX, pady=self.PADY)
        self.retirar_saldo = wp.MovimentarSaldo(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id=self.CARTEIRA_SELECIONADA, tipo='s', app=self)
        self.retirar_saldo.grid(column=1, row=1, padx=self.PADX, pady=self.PADY)
            # Transfeir Saldo
        self.transferir_saldo_name = customtkinter.CTkLabel(self.tab1, text='Transferir Saldo', width=self.WIDTH, height=self.HEIGHT)
        self.transferir_saldo_name.grid(column=2, row=0, padx=self.PADX, pady=self.PADY)
        self.transferir_saldo = wp.TransferirSaldo(self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_origem=self.CARTEIRA_SELECIONADA, app=self)
        self.transferir_saldo.grid(column=2, row=1, padx=self.PADX, pady=self.PADY)
        # Deletar Categoria Entrada
        self.deletar_categoria_nome_e = customtkinter.CTkLabel(self.tab1, text='Deletar Categoria Entrada', width=self.WIDTH, height=self.HEIGHT)
        self.deletar_categoria_nome_e.grid(column=0, row=2, padx=self.PADX, pady=self.PADY)
        self.deletar_categoria_e = wp.DeletarCategorias(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, tipo='e', app=self)
        self.deletar_categoria_e.grid(column=0, row=3, padx=self.PADX, pady=self.PADY)
        # Deletar Categoria saida
        self.deletar_categoria_nome_s = customtkinter.CTkLabel(self.tab1, text='Deletar Categoria Saida', width=self.WIDTH, height=self.HEIGHT)
        self.deletar_categoria_nome_s.grid(column=1, row=2, padx=self.PADX, pady=self.PADY)
        self.deletar_categoria_s = wp.DeletarCategorias(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, tipo='s', app=self)
        self.deletar_categoria_s.grid(column=1, row=3, padx=self.PADX, pady=self.PADY)
        # Criar CAtegoria
        self.criar_categoria_label = customtkinter.CTkLabel(self.tab1, text='Criar Categoria', width=self.WIDTH, height=self.HEIGHT)
        self.criar_categoria_label.grid(column=2, row=2, padx=self.PADX, pady=self.PADY)
        self.criar_categoria = wp.CriarCategoria(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, app=self)
        self.criar_categoria.grid(column=2, row=3, padx=self.PADX, pady=self.PADY)
        ######### widgets principal #########

        self.mainloop()

    def selecionar_carteira(self):
        self.CARTEIRA_SELECIONADA = self.lista_carteiras.get()
        # ATUALIZA O NOME DA CARTEIRA
        self.nome_carteira_label = bd.ver_nome_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.nome_carteira.configure(text=f'{self.nome_carteira_label}')
        # ATUALIZA O SALDO DA CARTEIRA
        self.saldo_carteira_label = bd.ver_saldo_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.saldo_carteira.configure(text=f'{self.saldo_carteira_label}')
        # ATUALIZA ADICIONAR SALDO
        self.adicionar_saldo.destroy()
        self.adicionar_saldo = wp.MovimentarSaldo(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id=self.CARTEIRA_SELECIONADA, tipo='e', app=self)
        self.adicionar_saldo.grid(column=0, row=1, padx=self.PADX, pady=self.PADY)
        # ATUALIZA O RETIRA SALDO
        self.retirar_saldo.destroy()
        self.retirar_saldo = wp.MovimentarSaldo(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id=self.CARTEIRA_SELECIONADA, tipo='s', app=self)
        self.retirar_saldo.grid(column=1, row=1, padx=self.PADX, pady=self.PADY)
        # ATUALIZAR O TRANSFERIR SALDO
        self.transferir_saldo.destroy()
        self.transferir_saldo = wp.TransferirSaldo(self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_origem=self.CARTEIRA_SELECIONADA, app=self)
        self.transferir_saldo.grid(column=2, row=1, padx=self.PADX, pady=self.PADY)
        # ATUALIZA DELETAR CATEGORIA ENTRADAS
        self.deletar_categoria_e.destroy()
        self.deletar_categoria_e = wp.DeletarCategorias(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, tipo='e', app=self)
        self.deletar_categoria_e.grid(column=0, row=3, padx=self.PADX, pady=self.PADY)
        # ATUALIZA DELETAR CATEGORIA SAIDAS
        self.deletar_categoria_s.destroy()
        self.deletar_categoria_s = wp.DeletarCategorias(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, tipo='s', app=self)
        self.deletar_categoria_s.grid(column=1, row=3, padx=self.PADX, pady=self.PADY)
        # Criar Categoria
        self.criar_categoria.destroy()
        self.criar_categoria = wp.CriarCategoria(master=self.tab1, username=self.USERNAME, password=self.PASSWORD, carteira_id= self.CARTEIRA_SELECIONADA, app=self)
        self.criar_categoria.grid(column=2, row=3, padx=self.PADX, pady=self.PADY)
        self.update_idletasks()
        self.update()
    
    def logout(self):
        self.USERNAME = None
        self.PASWORD = None
        self.CARTEIRA_SELECIONADA = None
        self.destroy()
        MainLogin()


######################################################################################################################
######################################################################################################################
######################################################################################################################












######################################################################################################################
############################################ TELA DE LOGIN ###########################################################
######################################################################################################################


class MsgRememberPassword(customtkinter.CTk):

    def __init__(self, dica):
        super().__init__()
        self.PADY = 5
        self.PADX = 5
        self.title('Password')
        self.title(name)
        self.resizable(width=False, height=False)
        self.label_dica = customtkinter.CTkLabel(self, text='PASSWORD HINT:', font=arial24)
        self.label_dica.grid(row=0, column=0, pady=self.PADY, padx= 5*self.PADX, columnspan=2)
        self.label = customtkinter.CTkLabel(self, text=f'{dica}', font=arial15)
        self.label.grid(row=1, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.button_ok = customtkinter.CTkButton(self, text='OK', font=arial8, command=self.close)
        self.button_ok.grid(row=2, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.mainloop()

    def close(self):
        self.destroy()


# tela para relembrar password
class RememberPassword(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.PADY = 5
        self.PADX = 5
        self.resizable(width=False, height=False)
        self.title(name)
        self.label = customtkinter.CTkLabel(self, text='Remember Account', font=arial24)
        self.label.grid(row=0, column=0, padx=5*self.PADX, pady=self.PADY, columnspan=2)
        self.label_username = customtkinter.CTkLabel(self, text='Username')
        self.label_username.grid(row=1, column=0, padx=5*self.PADX, pady=self.PADY)
        self.entry_username = customtkinter.CTkEntry(self)
        self.entry_username.grid(row=1, column=1, padx=5*self.PADX, pady=self.PADY)
        self.button_confirm = customtkinter.CTkButton(self, text='Confirmar', command=self.remember_password)
        self.button_confirm.grid(row=2, column=0, padx=5*self.PADX, pady=self.PADY, columnspan=2)
        self.mainloop()
    
    def remember_password(self):
        USERNAME = self.entry_username.get()
        dica = bd.ver_dica_password(bd.cnx(), USERNAME)
        self.entry_username.delete(0, customtkinter.END)
        MsgRememberPassword(dica)



# Retirna um erro para o password
class ErrorPassword(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.PADY = 5
        self.PADX = 5
        self.title('Error')
        self.title(name)
        self.resizable(width=False, height=False)
        self.label = customtkinter.CTkLabel(self, text='Passwords do not match', font=arial15)
        self.label.grid(row=0, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.button_ok = customtkinter.CTkButton(self, text='OK', font=arial8, command=self.close)
        self.button_ok.grid(row=1, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.mainloop()

    def close(self):
        self.destroy()

# retornar que a conta foir criada
class AccountCreated(customtkinter.CTk):

    def __init__(self, msg):
        super().__init__()
        self.PADY = 5
        self.PADX = 5
        self.title(name)
        self.resizable(width=False, height=False)
        self.label = customtkinter.CTkLabel(self, text=f'{msg}', font=arial15)
        self.label.grid(row=0, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.button_ok = customtkinter.CTkButton(self, text='OK', font=arial8, command=self.close)
        self.button_ok.grid(row=1, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.mainloop()

    def close(self):
        self.destroy()

# tela para criar conta
class CreateAccount(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(width=False, height=False)
        self.title(name)
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.create_account = customtkinter.CTkLabel(self, text='CREATE ACCOUNT', font=arial24, width=self.WIDTH, height=self.HEIGHT)
        self.create_account.grid(row=0, column=0, pady=self.PADY, padx=self.PADX, columnspan=2)
        self.label_username = customtkinter.CTkLabel(self, text='Username', width=self.WIDTH, height=self.HEIGHT)
        self.label_username.grid(row=1, column=0, pady=self.PADY, padx=self.PADX)
        self.entry_username = customtkinter.CTkEntry(self)
        self.entry_username.grid(row=1, column=1, pady=self.PADY, padx=self.PADX)
        self.label_password = customtkinter.CTkLabel(self, text='Password', width=self.WIDTH, height=self.HEIGHT)
        self.label_password.grid(row=2, column=0, pady=self.PADY, padx=self.PADX)
        self.entry_password = customtkinter.CTkEntry(self, show='*')
        self.entry_password.grid(row=2, column=1, pady=self.PADY, padx=self.PADX)
        self.clabel_password = customtkinter.CTkLabel(self, text='Confirme Password', width=self.WIDTH, height=self.HEIGHT)
        self.clabel_password.grid(row=3, column=0, pady=self.PADY, padx=self.PADX)
        self.centry_password = customtkinter.CTkEntry(self, show='*')
        self.centry_password.grid(row=3, column=1, pady=self.PADY, padx=self.PADX)

        self.clabel_dpassword = customtkinter.CTkLabel(self, text='Password Hint', width=self.WIDTH, height=self.HEIGHT)
        self.clabel_dpassword.grid(row=4, column=0, pady=self.PADY, padx=self.PADX)
        self.entry_dpassword = customtkinter.CTkEntry(self)
        self.entry_dpassword.grid(row=4, column=1, pady=self.PADY, padx=self.PADX)

        self.button_create = customtkinter.CTkButton(self, text='Create', width=self.WIDTH, height=self.HEIGHT, command=self.error_password)
        self.button_create.grid(row=5, column=0)
        # CRIAR DICA PASSWORD er confirmação de password

        self.mainloop()
    
    def error_password(self):
        USERNAME = self.entry_username.get()
        PASSWORD = self.entry_password.get()
        CPASSWORD = self.centry_password.get()
        DPASSWORD = self.entry_dpassword.get()
        if PASSWORD != CPASSWORD:
            self.entry_username.delete(0, customtkinter.END)
            self.entry_password.delete(0, customtkinter.END)
            self.centry_password.delete(0, customtkinter.END)
            self.entry_dpassword.delete(0, customtkinter.END)
            ErrorPassword()
        else:
            self.entry_username.delete(0, customtkinter.END)
            self.entry_password.delete(0, customtkinter.END)
            self.centry_password.delete(0, customtkinter.END)
            self.entry_dpassword.delete(0, customtkinter.END)
            resultado = bd.criar_conta(bd.cnx(), USERNAME, PASSWORD, DPASSWORD)
            AccountCreated(resultado)


# retorna que password esta incorreto
class ErrorLogin(customtkinter.CTk):
 
    def __init__(self):
        super().__init__()
        self.PADY = 5
        self.PADX = 5
        self.title('Error')
        self.resizable(width=False, height=False)
        self.label = customtkinter.CTkLabel(self, text='User or password incorrect.', font=arial15)
        self.label.grid(row=0, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.button_ok = customtkinter.CTkButton(self, text='OK', font=arial8, command=self.close)
        self.button_ok.grid(row=1, column=0, pady=self.PADY, padx= 5*self.PADX)
        self.mainloop()

    def close(self):
        self.destroy()


# tela principal de login
class MainLogin(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.USERNAME = None
        self.PASSWORD = None
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.resizable(width=False, height=False)
        # Cria Janela
        self.title(name)
        # Cria name LOGIN
        self.label1 = customtkinter.CTkLabel(self, text='LOGIN', width= self.WIDTH, height=self.HEIGHT, font=arial24)
        # label e entry username
        self.label_username = customtkinter.CTkLabel(self, text='Username', width=self.WIDTH, height=self.HEIGHT)
        self.entry_username = customtkinter.CTkEntry(self)
        # label password e entry password
        self.label_password = customtkinter.CTkLabel(self, text='Password', width=self.WIDTH, height=self.HEIGHT)
        self.entry_password = customtkinter.CTkEntry(self, show='*')
        # Botao enter
        self.button_enter = customtkinter.CTkButton(self, text='Enter', width=self.WIDTH, height=self.HEIGHT, command=self.check_login)
        # botao criar conta
        self.account_creator_button = customtkinter.CTkButton(self, text='Create account', width=self.WIDTH, height=self.HEIGHT, command=self.create_account)
        # botao lembrar senha
        self.remember_password_button = customtkinter.CTkButton(self, text='Remember password', width=self.WIDTH, height=self.HEIGHT, command=self.remember_password)
        # posiciona os widgetsge
            # login
        self.label1.grid(row=0, column=0, pady=self.PADY, padx=self.PADX, columnspan=7)
            # Username e entry
        self.label_username.grid(row=1, column=0, pady=self.PADY, padx=self.PADX)
        self.entry_username.grid(row=1, column=1, pady=self.PADY, padx=self.PADX)
            # password e entry
        self.label_password.grid(row=2, column=0, pady=self.PADY, padx=self.PADX)
        self.entry_password.grid(row=2, column=1, pady=self.PADY, padx=self.PADX)
            # buttons
        self.button_enter.grid(row=3, column=0, pady=self.PADY, padx=self.PADX)
        self.account_creator_button.grid(row=3, column=1, pady=self.PADY, padx=self.PADX)
        self.remember_password_button.grid(row=4, column=0, pady=self.PADY, padx=self.PADX)

        self.mainloop()

    def create_account(self):
        CreateAccount()
    
    def remember_password(self):
        RememberPassword()

    def check_login(self):
        # FECHA A JANELA
        # EMITE O PASSWORD E USERNAME
        username = self.entry_username.get()
        password = self.entry_password.get()
        # VERIFRICA E VALIDA AS ENTRADAS NO BANCO DE DADOS
        self.cnx = bd.cnx()
        verificacao = bd.valida_usuario(self.cnx, username, password)
        if verificacao == 0:
            # EMITE UMA MSG DE ERRO E LIMPA AS ENTRADAS
            print("Usuario não existe")
            self.entry_username.delete(0, customtkinter.END)
            self.entry_password.delete(0, customtkinter.END)
            ErrorLogin()

        if verificacao == 1:
            #APROVA A ENTRADA
            print('Login efetuado')
            self.entry_username.delete(0, customtkinter.END)
            self.entry_password.delete(0, customtkinter.END)
            self.destroy()
            App(username, password)
######################################################################################################################
######################################################################################################################
######################################################################################################################

if __name__ == '__main__':
    #tela = App('user3', 'abcdef')
    tela = MainLogin()