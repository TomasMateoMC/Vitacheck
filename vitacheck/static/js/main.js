// Cerrar automáticamente los mensajes flash después de 4 segundos
document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(a => {
        setTimeout(() => {
            a.classList.remove("show");
            a.classList.add("fade");
        }, 4000);
    });
});

// Confirmación universal para formularios con delete
document.querySelectorAll("form[data-confirm]").forEach(form => {
    form.addEventListener("submit", function(e) {
        const message = form.getAttribute("data-confirm");
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
});
