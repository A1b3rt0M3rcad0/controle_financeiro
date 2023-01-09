-- Criar o usuario do banco de dados
CREATE USER 'usuario'@'localhost' IDENTIFIED BY 'usuario';
GRANT EXECUTE ON financa_pessoal.* TO 'usuario'@'localhost';
ALTER USER 'usuario'@'localhost' PASSWORD EXPIRE NEVER;