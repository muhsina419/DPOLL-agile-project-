document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("reset-btn").addEventListener("click", function () {
        let email = document.getElementById("email").value;
        let csrfToken = "{{ csrf_token }}";  // You might need to pass this from Django

        fetch("/forgot-password/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken
            },
            body: new URLSearchParams({ "email": email })
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById("response").innerText = "Password reset link sent to your email.";
        })
        .catch(error => {
            document.getElementById("response").innerText = "Error sending password reset email.";
        });
    });
});
