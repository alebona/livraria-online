document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", function() {
        let loader = document.getElementById("loader");
        let progress = document.getElementById("progress");
        let status = document.getElementById("status");

        loader.style.display = "block";

        const steps = [
            "Buscando livro no Google Books...",
            "Verificando Autor...",
            "Verificando Categoria...",
            "Verificando Editora...",
            "Salvando no banco de dados...",
            "Finalizando..."
        ];

        let i = 0;
        function nextStep() {
            if (i < steps.length) {
                status.textContent = steps[i];
                progress.style.width = ((i + 1) / steps.length * 100) + "%";
                i++;
                setTimeout(nextStep, 1200);
            }
        }
        nextStep();
    });
});
