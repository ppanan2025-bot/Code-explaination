document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".mode-button");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            buttons.forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
        });
    });
});
