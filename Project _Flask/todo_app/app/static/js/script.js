document.addEventListener("DOMContentLoaded", () => {

    // Auto-hide flash messages
    const messages = document.querySelectorAll(".flash");

    messages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";

            setTimeout(() => {
                message.remove();
            }, 300);

        }, 3000);
    });


    // Confirm delete buttons
    const deleteForms = document.querySelectorAll(
        "form[action*='/delete']"
    );

    deleteForms.forEach((form) => {

        form.addEventListener("submit", (event) => {

            const confirmed = confirm(
                "Are you sure you want to delete this task?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});