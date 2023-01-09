INSERT INTO usuario (id, password, dica_password)
VALUES ('user1', '123456', 'nome do animal de estimação'),
       ('user2', 'qwerty', 'nome do primeiro carro'),
       ('user3', 'abcdef', 'nome do primeiro animal de estimação');

INSERT INTO carteira (usuario_id, nome, descricao, saldo)
VALUES ('user1', 'Carteira pessoal', 'Carteira para despesas pessoais', 1000.00),
       ('user2', 'Carteira de viagem', 'Carteira para despesas de viagem', 500.00),
       ('user3', 'Carteira de emergência', 'Carteira para emergências', 200.00);

INSERT INTO categoria_entrada (carteira_id, nome, descricao)
VALUES (1, 'Salário', 'Recebimento de salário'),
       (1, 'Investimentos', 'Rendimentos de investimentos'),
       (2, 'Salário', 'Recebimento de salário'),
       (2, 'Vendas', 'Recebimento de vendas'),
       (3, 'Salário', 'Recebimento de salário'),
       (3, 'Doações', 'Recebimento de doações');

INSERT INTO entradas (carteira_id, categoria_entrada_id, valor, data_entrada)
VALUES (1, 1, 3000.00, '2022-01-01'),
       (1, 2, 500.00, '2022-01-15'),
       (2, 3, 2000.00, '2022-01-01'),
       (2, 4, 1000.00, '2022-01-20'),
       (3, 5, 1500.00, '2022-01-01'),
       (3, 6, 500.00, '2022-01-10');

INSERT INTO categoria_saida (carteira_id, nome, descricao)
VALUES (1, 'Alimentação', 'Despesas com alimentação'),
       (1, 'Transporte', 'Despesas com transporte'),
       (2, 'Hospedagem', 'Despesas com hospedagem'),
       (2, 'Passeios', 'Despesas com passeios turísticos'),
       (3, 'Emergências médicas', 'Despesas com emergências médicas'),
       (3, 'Outras despesas', 'Outras despesas de emergência');
INSERT INTO saidas (carteira_id, categoria_saida_id, valor, data_saida)
VALUES (1, 1, 500.00, '2022-01-10'),
       (1, 2, 200.00, '2022-01-20'),
       (2, 3, 1000.00, '2022-01-05'),
       (2, 4, 500.00, '2022-01-15'),
       (3, 5, 200.00, '2022-01-01'),
       (3, 6, 100.00, '2022-01-10');
INSERT INTO transferencia (carteira_origem, carteira_destino, valor, data_transferencia)
VALUES (1, 3, 100.00, '2022-01-05'),
       (2, 3, 200.00, '2022-01-10'),
       (3, 1, 50.00, '2022-01-15');