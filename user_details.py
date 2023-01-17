import pags as pg
import bd
import customtkinter
import widgets_principal as wp


class CriarCarteira(customtkinter.CTk):

    def __init__(self, USERNAME, PASSWORD, APP):
        super().__init__()
        # informações do usuário
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.APP = APP
        self.WIDTH = 10
        self.HEIGHT = 10
        self.PADY = 5
        self.PADX = 5
        self.title('Wallet Creator')
        self.resizable(width=False, height=False)
        # Widgets
           # LABEL SUPERIOR
        self.label_superior = customtkinter.CTkLabel(self, text = 'WALLET CREATOR', font=pg.arial24, width=self.WIDTH, height=self.HEIGHT)
        self.label_superior.grid(row=0, column=0, padx=self.PADX, pady=5*self.PADY, columnspan=3)
            # LABEL NOME
        self.label_nome = customtkinter.CTkLabel(self, text='Name', width=self.WIDTH, height=self.HEIGHT)
        self.label_nome.grid(column=0, row=1, padx=self.PADX, pady=self.PADY)
            # ENTRY NAME
        self.entry_name = customtkinter.CTkEntry(self, width=15*self.WIDTH, height=self.HEIGHT)
        self.entry_name.grid(row=1, column=1, padx=self.PADX, pady=self.PADY)
            # BUTTON CRIAR
        self.button = customtkinter.CTkButton(self, text='Creat Wallet', width=self.WIDTH, height=self.HEIGHT, command=self.criar_carteira)
        self.button.grid(row=3, column=0, columnspan=3)

        # Loo0p
        self.mainloop()
    
    def criar_carteira(self):
        self.name = self.entry_name.get()
        self.entry_name.delete(0, customtkinter.END)
        result = bd.criar_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, self.name)
        self.APP.selecionar_carteira()
        wp.MsgMovimentarSaldo(result)