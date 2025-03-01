document.getElementById("confirm-btn").addEventListener("click", function () {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const matchMessage = document.getElementById("match-message");

    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordPattern.test(password)) {
        matchMessage.style.color = "red";
        matchMessage.textContent = "Password does not meet criteria!";
        return;
    }

    if (password !== confirmPassword) {
        matchMessage.style.color = "red";
        matchMessage.textContent = "Passwords do not match!";
    } else {
        matchMessage.style.color = "green";
        matchMessage.textContent = "Passwords match!";
        alert("Password set successfully!");
    }
});
