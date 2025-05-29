document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".otp-input");

    // Fetch phone number using uniqueId and send OTP automatically
    if (typeof uniqueId !== "undefined" && uniqueId) {
        fetch(`/api/get-phone/?unique_id=${encodeURIComponent(uniqueId)}`)
            .then(res => res.json())
            .then(data => {
                if (data.phone) {
                    fetch("/api/send-otp/", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ phone: data.phone }),
                    });
                }
            });
    }

    // OTP input navigation
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
            const response = await fetch("/api/verify-otp/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ otp: otp }),
            });
            const result = await response.json();
            if (response.ok) {
                //window.location.href = `/api/reg_success/${uniqueId}/`;
                window.location.href = result.redirect;
            } else {
                window.location.href = "/api/reg_failure/"; // Failure page
            }
        } else {
            alert("Please enter a valid 6-digit OTP.");
        }
    });
});