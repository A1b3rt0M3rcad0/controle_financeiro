-- VERIFICA SE O USUARIO JÁ EXISTE
DELIMITER $$
CREATE PROCEDURE validaUsuario(usuario_id VARCHAR(50), senha VARCHAR(50))
	BEGIN
    IF (SELECT 1 FROM usuario WHERE usuario_Id = id AND senha = PASSWORD) THEN
		SELECT 1;
	ELSE
		SELECT 0;
	END IF;
    END 
$$
# --------------------------------------------------------------------------------
-- ADIONA SALDO A CARTEIRA DO USUARIO
DELIMITER $$
CREATE PROCEDURE adicionarSaldo(usuario_paramento_id VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, 
categoria_entrada_id_parametro INT, valor_parametro DECIMAl(12, 2))
	BEGIN
		-- VERIFICA SE O USUARIO É VALIDO SE ELE POSSUI UMA CARTEIRA E SE É O DONO DA CARTEIRA EM QUESTÂO
		IF (SELECT 1 FROM usuario WHERE id = usuario_paramento_id AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE usuario_id = usuario_paramento_id
        AND id = carteira_id_parametro) THEN
			UPDATE carteira SET saldo = saldo + valor_parametro WHERE usuario_id = usuario_paramento_id;
            INSERT INTO entradas (carteira_id, categoria_entrada_id, valor, data_entrada) VALUES (carteira_id_parametro, categoria_entrada_id_parametro, 
																									valor_parametro, CURDATE());
		ELSE
			-- O retorno "0" Significa que a operação não foi finalizada com sucesso
			SELECT 0;
		END IF;
    END
$$
# --------------------------------------------------------------------------------

-- RETIRAR SALDO DA CARTEIRA DO USUARIO
DELIMITER $$
CREATE PROCEDURE retirarSaldo(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, 
categoria_saida_id_parametro INT, valor_parametro DECIMAl(12, 2))
	BEGIN
		-- VERIFICA SE O USUARIO É VALIDO SE ELE POSSUI UMA CARTEIRA E SE É O DONO DA CARTEIRA EM QUESTÂO
		IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE usuario_id = usuario_id_parametro AND
		id = carteira_id_parametro) THEN
        -- VERIFICA SE HÁ SALDO NA CARTEIRA
			IF (SELECT saldo FROM carteira WHERE id = carteira_id_parametro) > valor_parametro THEN
				UPDATE carteira SET saldo = saldo - valor_parametro WHERE id = carteira_id_parametro;
                INSERT INTO saidas (carteira_id, categoria_saida_id, valor, data_saida) VALUES (carteira_id_parametro, categoria_saida_id_parametro,
																								valor_parametro, CURDATE());
			ELSE
				SELECT 0;
			END IF;
		ELSE
			SELECT 0;
    END IF;
    END
$$
# --------------------------------------------------------------------------------

-- TRANSFERIR SALDO PARA OUTRA CARTEIRA
DELIMITER $$
CREATE PROCEDURE transferirSaldo(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_origem_parametro INT, carteira_destino_parametro INT,
valor_parametro DECIMAl(12, 2))
BEGIN
	-- VERIFICA SE O USUARIO É VALIDO, SE ELE POSSUI UMA CARTEIRA, SE É O DONO DA CARTEIRA EM QUESTÂO E SE A CARTEIRA DESTINO EXISTE
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE usuario_id = usuario_id_parametro AND
	id = carteira_origem_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_destino_parametro) THEN
		IF (SELECT saldo FROM carteira WHERE id = carteira_origem_parametro) > valor_parametro THEN
			UPDATE carteira SET saldo = saldo - valor_parametro WHERE id = carteira_origem_parametro;
            UPDATE carteira SET saldo = saldo + valor_parametro WHERE id = carteira_destino_parametro;
            INSERT INTO transferencia (carteira_origem, carteira_destino, valor, data_transferencia) VALUES (carteira_origem_parametro, carteira_destino_parametro,
																											valor_parametro, CURDATE());
		ELSE
			SELECT 0;
        END IF;
	ELSE
		SELECT 0;
    END IF; 
END
$$
# --------------------------------------------------------------------------------

-- Criar Novo Usuario
DELIMITER $$
CREATE PROCEDURE criarUsuario(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), dica_password_parametro VARCHAR(100))
	BEGIN
		-- Verifica se o usuario ja existe
		IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro) THEN
			SELECT 0;
		ELSE
			INSERT INTO usuario (id, password, dica_password) VALUES (usuario_id_parametro, password_parametro, dica_password_parametro);
            INSERT INTO carteira (usuario_id, nome, descricao, saldo) VALUES (usuario_id_parametro, 'Carteira Principal', 'Usos Divérsos', 0);
            INSERT INTO categoria_entrada (carteira_id, nome, descricao) VALUES ((SELECT id FROM carteira WHERE usuario_id = usuario_id_parametro), 
																				'Receitas', 'Receitas Gerais');
			INSERT INTO categoria_saida (carteira_id, nome, descricao) VALUES ((SELECT id FROM carteira WHERE usuario_id = usuario_id_parametro),
																				'Gastos', 'Gastos Gerais');
		END IF;
	END
$$
# --------------------------------------------------------------------------------

-- Criar nova categoria saida
DELIMITER $$
CREATE PROCEDURE criarCategoriaSaida(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, nome_parametro VARCHAR(50), 
descricao_parametro VARCHAR(100))
	BEGIN
		-- CHECA A VALIDADE DO USUARIO
		IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
        usuario_id = usuario_id_parametro) THEN
			INSERT INTO categoria_saida(carteira_id, nome, descricao) VALUES (carteira_id_parametro, nome_parametro, descricao_parametro);
        ELSE
			SELECT 0;
		END IF;
	END
$$
# --------------------------------------------------------------------------------

-- Criar nova categoria entrada
DELIMITER $$
CREATE PROCEDURE criarCategoriaEntrada(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, nome_parametro VARCHAR(50), 
descricao_parametro VARCHAR(100))
	BEGIN
		-- CHECA A VALIDADE DO USUARIO
		IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
        usuario_id = usuario_id_parametro) THEN
			INSERT INTO categoria_entrada(carteira_id, nome, descricao) VALUES (carteira_id_parametro, nome_parametro, descricao_parametro);
        ELSE
			SELECT 0;
		END IF;
	END
$$
# --------------------------------------------------------------------------------

-- Retonar valor da carteira
DELIMITER $$
CREATE PROCEDURE verSaldo(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT)
BEGIN
	-- CHECA A VALIDADE DO USUARIO
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
    usuario_id = usuario_id_parametro) THEN
		SELECT saldo FROM carteira WHERE id = carteira_id_parametro;
    ELSE
		SELECT 0;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Consultar todas as categorias de uma carteira
DELIMITER $$
CREATE PROCEDURE consultarCategorias(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, tipo char(1))
BEGIN
	-- CHECA A VALIDADE DO USUARIO
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
    usuario_id = usuario_id_parametro) THEN
		-- RETONAR AS SAIDAS
		IF (tipo = 's') THEN
			SELECT * FROM categoria_saida WHERE carteira_id = carteira_id_parametro;
		-- RETORNA AS ENTRADAS
		ELSEIF (tipo = 'e') THEN
			SELECT * FROM categoria_entrada WHERE carteira_id = carteira_id_parametro;
		ELSE
			SELECT 0;
		END IF;
	ELSE
		SELECT 0;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Consultar saldo de todas as carteiras de um usuario
DELIMITER $$
CREATE PROCEDURE verSaldoTotal(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50))
BEGIN
	-- CHECA A VALIDADE DO USUARIO
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE usuario_id = usuario_id_parametro) THEN
		SELECT SUM(saldo) FROM carteira WHERE usuario_id = usuario_id_parametro;
	ELSE
		SELECT 'Error';
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Consultar carteiras do usuario
DELIMITER $$
CREATE PROCEDURE verCarteiras(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50))
BEGIN
	-- CHECA A VALIDADE DO USUARIO
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE usuario_id = usuario_id_parametro) THEN
		SELECT * FROM carteira WHERE usuario_id = usuario_id_parametro;
    ELSE
		SELECT 0;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Consultar todas as entradas, saidas ou transferencias por periodo de uma carteira
DELIMITER $$
CREATE PROCEDURE consultarTransacoes(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), carteira_id_parametro INT, data_inicio DATE, data_fim DATE, 
tipo VARCHAR(2))
BEGIN
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
    usuario_id = usuario_id_parametro) THEN
		IF tipo = 'e' THEN
			SELECT * FROM entradas WHERE carteira_id = carteira_id_parametro AND data_entrada BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 's' THEN
			SELECT * FROM saidas WHERE carteira_id = carteira_id_parametro AND data_saida BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 'te' THEN
			SELECT * FROM transferencia WHERE carteira_origem = carteira_id_parametro AND data_transferencia BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 'tr' THEN
			SELECT * FROM transferencia WHERE carteira_destino = carteira_id_parametro AND data_transferencia BETWEEN data_inicio AND data_fim;
		END IF;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Retorna o valor somado de todas as transações por periodo de uma carteira
DELIMITER $$
CREATE PROCEDURE consultarSomaTotalTransacoes(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), 
carteira_id_parametro INT, data_inicio DATE, data_fim DATE, tipo VARCHAR(2))
BEGIN
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
    usuario_id = usuario_id_parametro) THEN
		IF tipo = 'e' THEN
			SELECT sum(valor) FROM entradas WHERE carteira_id = carteira_id_parametro AND data_entrada BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 's' THEN
			SELECT sum(valor) FROM saidas WHERE carteira_id =  carteira_id_parametro AND data_saida BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 'te' THEN
			SELECT sum(valor) FROM transferencia WHERE carteira_origem = carteira_id_parametro AND data_transferencia BETWEEN data_inicio AND data_fim;
		ELSEIF tipo = 'tr' THEN
			SELECT sum(valor) FROM transferencia WHERE carteira_destino = carteira_id_parametro AND data_transferencia BETWEEN data_inicio AND data_fim;
		END IF;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Criar nova carteira
DELIMITER $$
CREATE PROCEDURE criarCarteira(usuario_id_parametro VARCHAR(50), password_parametro VARCHAR(50), nome_parametro VARCHAR(50), descricao_parametro VARCHAR(100))
BEGIN
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_parametro) THEN
		INSERT INTO carteira (usuario_id, nome, descricao, saldo) VALUES (usuario_id_parametro, nome_parametro, descricao_parametro, 0);
	ELSE
		SELECT 0;
	END IF;
END $$
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

-- Retorna dica de senha
DELIMITER $$
CREATE PROCEDURE verDicaPassword(usuario_id_parametro VARCHAR(50))
BEGIN
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro) THEN
		SELECT dica_password FROM usuario WHERE id = usuario_id_parametro;
	ELSE
		SELECT 0;
	END IF;
END
$$
# --------------------------------------------------------------------------------

-- Altera Senha de acesso do usuario
DELIMITER $$
CREATE PROCEDURE trocarPassword(usuario_id_parametro VARCHAR(50), senha_atual_parametro VARCHAR(50), nova_senha_parametro VARCHAR(50), 
nova_dica_password VARCHAR(100))
BEGIN
  -- Verifica se a senha atual informada está correta
  IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = senha_atual_parametro) THEN
    -- Atualiza a senha do usuário
    UPDATE usuario SET password = nova_senha_parametro WHERE id = usuario_id_parametro;
    UPDATE usuario SET dica_password = nova_dica_password WHERE id = usuario_id_parametro;
  ELSE
    -- Retorna 0 se a senha atual estiver incorreta
    SELECT 0;
  END IF;
END 
$$
# --------------------------------------------------------------------------------
-- DELETEMA UMA CATEGORIA
DROP PROCEDURE dropCategoria;
delimiter $$
CREATE PROCEDURE dropCategoria(usuario_id_parametro VARCHAR(50), password_id_parametro VARCHAR(50), carteira_id_parametro INT, 
categoria_id_parametro INT, tipo char(1))
BEGIN
	IF (SELECT 1 FROM usuario WHERE id = usuario_id_parametro AND password = password_id_parametro) AND (SELECT 1 FROM carteira WHERE id = carteira_id_parametro AND
    usuario_id = usuario_id_parametro) THEN
		IF (SELECT COUNT(*) FROM categoria_entrada WHERE carteira_id = carteira_id_parametro) >= 2 AND tipo = 'e' THEN
			IF (SELECT 1 FROM categoria_entrada WHERE id = categoria_id_parametro AND carteira_id = carteira_id_parametro) THEN
				DELETE FROM categoria_entrada WHERE id = categoria_id_parametro;
				SELECT 1;
			ELSE
				SELECT 'Categoria não pertence a carteira';
			END IF;
		ELSEIF (SELECT COUNT(*) FROM categoria_saida WHERE carteira_id = carteira_id_parametro) >= 2 AND tipo = 's' THEN
			IF (SELECT 1 FROM categoria_saida WHERE id = categoria_id_parametro AND carteira_id_parametro) THEN
				DELETE FROM categoria_saida WHERE id = categoria_id_parametro;
				SELECT 1;
			ELSE
				SELECT 'Categoria não pertence a carteira';
			END IF;
		ELSE
			SELECT 'Númeroi mínimo de categorias';
		END IF;
    ELSE
		SELECT 'Usuario ou carteira não existem';
	END IF;
END;
$$
# --------------------------------------------------------------------------------
