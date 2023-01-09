CREATE SCHEMA iF NOT EXISTS financa_pessoal;
USE financa_pessoal;

CREATE TABLE iF NOT EXISTS usuario (
  id VARCHAR(50) PRIMARY KEY NOT NULL,
  password VARCHAR(50) NOT NULL,
  dica_password VARCHAR(100) NOT NULL
);

CREATE TABLE iF NOT EXISTS carteira (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  usuario_id VARCHAR(50)  NOT NULL,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  saldo DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE iF NOT EXISTS categoria_entrada (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  carteira_id INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  FOREIGN KEY (carteira_id) REFERENCES carteira(id) ON DELETE CASCADE
);

CREATE TABLE iF NOT EXISTS entradas (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  carteira_id INT NOT NULL,
  categoria_entrada_id INT NOT NULL,
  valor DECIMAL(12,2) NOT NULL,
  data_entrada DATE NOT NULL,
  FOREIGN KEY (carteira_id) REFERENCES carteira(id) ON DELETE CASCADE,
  FOREIGN KEY (categoria_entrada_id) REFERENCES categoria_entrada(id) ON DELETE CASCADE
);

CREATE TABLE iF NOT EXISTS categoria_saida (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  carteira_id INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  FOREIGN KEY (carteira_id) REFERENCES carteira(id) ON DELETE CASCADE
);

CREATE TABLE iF NOT EXISTS saidas (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  carteira_id INT NOT NULL,
  categoria_saida_id INT NOT NULL,
  valor DECIMAL(12,2) NOT NULL,
  data_saida DATE NOT NULL,
  FOREIGN KEY (carteira_id) REFERENCES carteira(id) ON DELETE CASCADE,
  FOREIGN KEY (categoria_saida_id) REFERENCES categoria_saida(id) ON DELETE CASCADE
);

CREATE TABLE iF NOT EXISTS transferencia (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  carteira_origem INT NOT NULL,
  carteira_destino INT NOT NULL,
  valor DECIMAL(12, 2) NOT NULL,
  data_transferencia DATE NOT NULL,
  FOREIGN KEY (carteira_origem) REFERENCES carteira(id) ON DELETE CASCADE,
  FOREIGN KEY (carteira_destino) REFERENCES carteira(id) ON DELETE CASCADE
);