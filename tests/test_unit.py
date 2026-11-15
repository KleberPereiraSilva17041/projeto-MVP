import os
import sqlite3
import tempfile

import app as app_module


def test_conectar_banco_retorna_conexao_com_row_factory():
    fd, caminho_banco = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_PATH"] = caminho_banco

    conexao = app_module.conectar_banco()

    assert isinstance(conexao, sqlite3.Connection)
    assert conexao.row_factory == sqlite3.Row

    conexao.close()
    os.remove(caminho_banco)


def test_criar_banco_cria_tabela_clientes():
    fd, caminho_banco = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_PATH"] = caminho_banco

    app_module.criar_banco()

    conexao = app_module.conectar_banco()
    tabelas = conexao.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'"
    ).fetchall()
    conexao.close()

    os.remove(caminho_banco)

    assert len(tabelas) == 1


def test_criar_banco_e_idempotente():
    fd, caminho_banco = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_PATH"] = caminho_banco

    app_module.criar_banco()
    app_module.criar_banco()

    conexao = app_module.conectar_banco()
    tabelas = conexao.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'"
    ).fetchall()
    conexao.close()

    os.remove(caminho_banco)

    assert len(tabelas) == 1
