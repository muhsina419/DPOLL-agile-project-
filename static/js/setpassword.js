document.getElementById("passwordForm").addEventListener("submit", async function (event) {
    event.preventDefault();

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
        return;
    }

    matchMessage.style.color = "green";
    matchMessage.textContent = "Passwords match!";

    const uniqueId = new URLSearchParams(window.location.search).get('unique_id');

    try {
        let response = await fetch("/setpassword/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `unique_id=${uniqueId}&password=${password}`
        });

        let result = await response.json();
        if (response.status === 200) {
            alert(result.message);
            window.location.href = "/setpassword.html"; // Redirect to setpassword.html
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
});