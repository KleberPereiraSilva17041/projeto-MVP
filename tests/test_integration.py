import app as app_module


def test_dashboard_carrega(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Gestão Fácil".encode("utf-8") in resposta.data


def test_lista_clientes_vazia(client):
    resposta = client.get("/clientes")
    assert resposta.status_code == 200
    assert "Nenhum cliente cadastrado".encode("utf-8") in resposta.data


def test_cadastrar_cliente(client):
    resposta = client.post(
        "/clientes/novo",
        data={
            "nome": "Maria Silva",
            "cpf": "123.456.789-00",
            "telefone": "11999999999",
            "email": "maria@example.com",
            "endereco": "Rua A, 123",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "Maria Silva".encode("utf-8") in resposta.data


def test_pesquisar_cliente_por_nome(client):
    client.post("/clientes/novo", data={"nome": "João Souza", "cpf": "", "telefone": "", "email": "", "endereco": ""})
    client.post("/clientes/novo", data={"nome": "Pedro Lima", "cpf": "", "telefone": "", "email": "", "endereco": ""})

    resposta = client.get("/clientes?busca=João")

    assert "João Souza".encode("utf-8") in resposta.data
    assert "Pedro Lima".encode("utf-8") not in resposta.data


def test_editar_cliente_atualiza_dados(client):
    client.post("/clientes/novo", data={"nome": "Carlos", "cpf": "", "telefone": "", "email": "", "endereco": ""})

    conexao = app_module.conectar_banco()
    cliente = conexao.execute("SELECT id FROM clientes WHERE nome = 'Carlos'").fetchone()
    conexao.close()

    resposta = client.post(
        f"/clientes/editar/{cliente['id']}",
        data={
            "nome": "Carlos Souza",
            "cpf": "",
            "telefone": "",
            "email": "",
            "endereco": "",
        },
        follow_redirects=True,
    )

    assert "Carlos Souza".encode("utf-8") in resposta.data


def test_editar_cliente_inexistente_redireciona_para_lista(client):
    resposta = client.get("/clientes/editar/9999", follow_redirects=True)

    assert resposta.status_code == 200
    assert "Nenhum cliente cadastrado".encode("utf-8") in resposta.data


def test_excluir_cliente_remove_da_lista(client):
    client.post("/clientes/novo", data={"nome": "Ana", "cpf": "", "telefone": "", "email": "", "endereco": ""})

    conexao = app_module.conectar_banco()
    cliente = conexao.execute("SELECT id FROM clientes WHERE nome = 'Ana'").fetchone()
    conexao.close()

    resposta = client.post(f"/clientes/excluir/{cliente['id']}", follow_redirects=True)

    assert "Nenhum cliente cadastrado".encode("utf-8") in resposta.data
