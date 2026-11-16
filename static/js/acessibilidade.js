(function () {
    const CHAVE_ARMAZENAMENTO = "gestaofacil-alto-contraste";
    const corpo = document.body;
    const botao = document.getElementById("toggle-contraste");

    function aplicarContraste(ativo) {
        corpo.classList.toggle("alto-contraste", ativo);
        if (botao) {
            botao.setAttribute("aria-pressed", String(ativo));
            botao.textContent = ativo
                ? "◐ Desativar Alto Contraste"
                : "◐ Ativar Alto Contraste";
        }
    }

    const preferenciaSalva = localStorage.getItem(CHAVE_ARMAZENAMENTO) === "true";
    aplicarContraste(preferenciaSalva);

    if (botao) {
        botao.addEventListener("click", function () {
            const novoEstado = !corpo.classList.contains("alto-contraste");
            aplicarContraste(novoEstado);
            localStorage.setItem(CHAVE_ARMAZENAMENTO, String(novoEstado));
        });
    }
})();
