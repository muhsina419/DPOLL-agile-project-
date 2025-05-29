document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".otp-input");

    inputs.forEach((input, index) => {
        input.addEventListener("input", (e) => {
            input.classList.remove("active");
            if (e.target.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].classList.add("active");
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && index > 0 && e.target.value === "") {
                inputs[index - 1].classList.add("active");
                inputs[index - 1].focus();
            }
        });
    });

    document.getElementById("verify-btn").addEventListener("click", async () => {
        let otp = "";
        inputs.forEach(input => otp += input.value);

        if (otp.length === 6) {
            try {
                const response = await fetch("/api/verify-otp/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ otp: otp }),
                });

                const result = await response.json();
                if (response.ok) {
                    alert(result.message || "OTP Verified Successfully!");
                    window.location.href = "/api/dashboard/"; // Redirect on success
                } else {
                    alert(result.error || "Invalid OTP. Please try again.");
                }
            } catch (error) {
                console.error("Error verifying OTP:", error);
                alert("Something went wrong. Please try again later.");
            }
        } else {
            alert("Please enter a valid 6-digit OTP.");
        }
    });
});