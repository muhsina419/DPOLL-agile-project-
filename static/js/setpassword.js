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

    // Extract unique_id from the URL
    const urlParts = window.location.pathname.split("/");
    const uniqueId = urlParts[urlParts.length - 2]; // Extracts unique ID from URL
    console.log("Extracted Unique ID from js:", uniqueId );

    try {
        let response = await fetch(`/api/setpassword/${uniqueId}/`, {  // Correct URL with leading slash
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()  // Fetch CSRF token correctly
            },
            body: new URLSearchParams({ password: password })  // Safer way to send form data
        });

        console.log(response);  // Log the response status
        let result = await response.json();

        if (response.ok) {
            alert(result.message);
            window.location.href = `/api/otp/${uniqueId}/`;  // Redirect after success
        } else {
            alert(result.error || "Failed to set password.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
});

// Function to fetch CSRF token properly
function getCSRFToken() {
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfTokenInput ? csrfTokenInput.value : "";
}