        # ATUALIZA O NOME DA CARTEIRA
        self.nome_carteira_label = bd.ver_nome_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.nome_carteira.destroy()
        self.nome_carteira = customtkinter.CTkLabel(self.informacoes_usuario, text=self.nome_carteira_label)
        self.nome_carteira.grid(column=0, row=4, padx=self.PADX, pady=self.PADY)
         # ATUALIZA O SALDO DA CARTEIRA
        self.saldo_carteira_label = bd.ver_saldo_carteira(bd.cnx(), self.USERNAME, self.PASSWORD, int(self.CARTEIRA_SELECIONADA))
        self.saldo_carteira.destroy()
        self.saldo_carteira = customtkinter.CTkLabel(self.informacoes_usuario, text=f'Saldo: {self.saldo_carteira_label}', width=8*self.WIDTH, height=self.HEIGHT)
        self.saldo_carteira.grid(column=0, row=5, padx=self.PADX, pady=self.PADY)
        # ATUALIZA o ADICIONAR SALDO
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
        self.update_idletasks()
        self.update()