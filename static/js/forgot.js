document.addEventListener("DOMContentLoaded", function () {
    const step1 = document.getElementById("step1");
    const step2 = document.getElementById("step2");
    const step3 = document.getElementById("step3");
    const uniqueIdInput = document.getElementById("uniqueId");
    const otpInput = document.getElementById("otp");
    const newPasswordInput = document.getElementById("newPassword");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const responseDiv = document.getElementById("response");

    // Step 1: Send OTP
    document.getElementById("send-otp-btn").addEventListener("click", function () {
        const uniqueId = uniqueIdInput.value.trim();
        if (!uniqueId) {
            responseDiv.innerText = "Please enter your Unique ID.";
            return;
        }
        fetch("/api/get-phone/?unique_id=" + encodeURIComponent(uniqueId))
            .then(res => res.json())
            .then(data => {
                if (data.phone) {
                    // Send OTP to phone
                    fetch("/api/send-otp/", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ phone: data.phone })
                    })
                    .then(res => res.json())
                    .then(data => {
                        step1.style.display = "none";
                        step2.style.display = "block";
                        responseDiv.innerText = "OTP sent to your registered phone number.";
                    })
                    .catch(() => responseDiv.innerText = "Error sending OTP.");
                } else {
                    responseDiv.innerText = "Unique ID not found.";
                }
            })
            .catch(() => responseDiv.innerText = "Error fetching phone number.");
    });

    // Step 2: Verify OTP
    document.getElementById("verify-otp-btn").addEventListener("click", function () {
        const otp = otpInput.value.trim();
        if (!otp) {
            responseDiv.innerText = "Please enter the OTP.";
            return;
        }
        fetch("/api/verify-otp/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ otp: otp })
        })
        .then(res => res.json())
        .then(data => {
            if (data.redirect) {
                step2.style.display = "none";
                step3.style.display = "block";
                responseDiv.innerText = "OTP verified. Please enter your new password.";
            } else {
                responseDiv.innerText = data.error || "Invalid OTP.";
            }
        })
        .catch(() => responseDiv.innerText = "Error verifying OTP.");
    });

    // Step 3: Set New Password
    document.getElementById("reset-password-btn").addEventListener("click", function () {
        const newPassword = newPasswordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        if (!newPassword || !confirmPassword) {
            responseDiv.innerText = "Please fill in both password fields.";
            return;
        }
        if (newPassword !== confirmPassword) {
            responseDiv.innerText = "Passwords do not match.";
            return;
        }
        fetch("/api/setpassword/" + encodeURIComponent(uniqueIdInput.value.trim()) + "/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: newPassword, confirm_password: confirmPassword })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                responseDiv.innerText = "Password reset successful. You can now log in.";
                step3.style.display = "none";
            } else {
                responseDiv.innerText = data.error || "Error resetting password.";
            }
        })
        .catch(() => responseDiv.innerText = "Error resetting password.");
    });
});