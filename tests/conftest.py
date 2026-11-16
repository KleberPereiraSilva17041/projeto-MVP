import os
import tempfile

import pytest

os.environ.setdefault("DATABASE_PATH", tempfile.mktemp(suffix=".db"))

import app as app_module


@pytest.fixture
def client():
    fd, caminho_banco = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_PATH"] = caminho_banco

    app_module.criar_banco()
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client

    os.remove(caminho_banco)
