document.addEventListener("DOMContentLoaded", function () {
    const loginButton = document.querySelector(".btn-outline-primary");
    const registerButton = document.querySelector(".btn-primary");

    loginButton.addEventListener("click", function () {
        window.location.href = "login.html"; // Update with actual login page
    });

    registerButton.addEventListener("click", function () {
        window.location.href = "register.html"; // Update with actual registration page
    });
});
