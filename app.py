from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)


# ==========================================
# CONEXÃO COM O BANCO DE DADOS
# ==========================================

def conectar_banco():
    caminho_banco = os.environ.get('DATABASE_PATH', 'database.db')
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    return conexao


# ==========================================
# CRIAÇÃO DO BANCO DE DADOS
# ==========================================

def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================
# LISTAGEM E PESQUISA DE CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():

    busca = request.args.get("busca", "").strip()

    conexao = conectar_banco()

    if busca:
        lista = conexao.execute("""
            SELECT * FROM clientes
            WHERE nome LIKE ? OR cpf_cnpj LIKE ?
            ORDER BY nome
        """, (f"%{busca}%", f"%{busca}%")).fetchall()
    else:
        lista = conexao.execute("""
            SELECT * FROM clientes
            ORDER BY nome
        """).fetchall()

    conexao.close()

    return render_template(
        "clientes.html",
        clientes=lista,
        busca=busca
    )


# ==========================================
# CADASTRAR CLIENTE
# ==========================================

@app.route("/clientes/novo", methods=["POST"])
def novo_cliente():

    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    endereco = request.form.get("endereco")

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO clientes
        (nome, cpf_cnpj, telefone, email, endereco)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, cpf, telefone, email, endereco))

    conexao.commit()
    conexao.close()

    return redirect(url_for("clientes"))


# ==========================================
# EDITAR CLIENTE
# ==========================================

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    conexao = conectar_banco()

    # SALVAR ALTERAÇÕES
    if request.method == "POST":

        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        endereco = request.form.get("endereco")

        conexao.execute("""
            UPDATE clientes
            SET nome = ?,
                cpf_cnpj = ?,
                telefone = ?,
                email = ?,
                endereco = ?
            WHERE id = ?
        """, (nome, cpf, telefone, email, endereco, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("clientes"))

    # BUSCAR CLIENTE PARA EDIÇÃO
    cliente = conexao.execute("""
        SELECT * FROM clientes WHERE id = ?
    """, (id,)).fetchone()

    conexao.close()

    if cliente is None:
        return redirect(url_for("clientes"))

    # TESTE NO TERMINAL
    print("CLIENTE ENCONTRADO:", dict(cliente))

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


# ==========================================
# EXCLUIR CLIENTE
# ==========================================

@app.route("/clientes/excluir/<int:id>", methods=["POST"])
def excluir_cliente(id):

    conexao = conectar_banco()

    conexao.execute("""
        DELETE FROM clientes WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("clientes"))


# ==========================================
# EXECUTAR SISTEMA
# ==========================================

criar_banco()

if __name__ == "__main__":
    app.run(debug=True)