document.getElementById("passwordForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const matchMessage = document.getElementById("match-message");

    if (password !== confirmPassword) {
        matchMessage.style.color = "red";
        matchMessage.textContent = "Passwords do not match!";
        return;
    }

    matchMessage.style.color = "green";
    matchMessage.textContent = "Passwords match!";

    const uniqueId = new URLSearchParams(window.location.search).get('unique_id');
    console.log("Retrieved unique_id:", uniqueId); // Log the retrieved unique_id

    if (!uniqueId) {
        alert("Unique ID is missing from the URL.");
        return;
    }

    try {
        console.log("Sending request with unique_id:", uniqueId, "and password:", password); // Log request details

        let response = await fetch("/api/register/setpassword/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `unique_id=${uniqueId}&password=${password}`
        });

        let result = await response.json();
        console.log("Server response:", result); // Log server response

        if (response.status === 200) {
            alert(result.message);
            window.location.href = "/api/otp/"; // Redirect to OTP verification
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
});