document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("findUniqueIdBtn");
    const phoneInput = document.getElementById("phoneInput");
    const resultDiv = document.getElementById("uniqueIdResult");

    btn.addEventListener("click", function () {
        const phone = phoneInput.value.trim();
        resultDiv.style.color = "#2d862d";
        if (!phone) {
            resultDiv.textContent = "Please enter your phone number.";
            resultDiv.style.color = "red";
            return;
        }
        fetch(`/api/get-unique-id/?phone=${encodeURIComponent(phone)}`)
            .then(res => res.json())
            .then(data => {
                if (data.unique_id) {
                    resultDiv.textContent = `Your Unique ID is: ${data.unique_id}`;
                    resultDiv.style.color = "#2d862d";
                } else {
                    resultDiv.textContent = data.error || "No user found with this phone number.";
                    resultDiv.style.color = "red";
                }
            })
            .catch(() => {
                resultDiv.textContent = "Error fetching unique ID.";
                resultDiv.style.color = "red";
            });
    });
});