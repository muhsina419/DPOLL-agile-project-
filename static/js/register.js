document.getElementById("registerForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Collect form values
    let fullName = document.getElementById("fullName").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let dob = document.getElementById("dob").value.trim();
    let sex = document.querySelector('input[name="sex"]:checked')?.value;
    let address = document.getElementById("address").value.trim();
    let idType = document.getElementById("idType").value.trim();
    let idNumber = document.getElementById("idNumber").value.trim();
    let idDocument = document.getElementById("idDocument").files[0];
    let photo = document.getElementById("photo").files[0];
    let password = document.getElementById("password").value.trim();
    let consent = document.getElementById("consent").checked;

    // **Validations**
    if (!fullName || !email || !phone || !dob || !sex || !address || !idType || !idNumber || !password) {
        alert("All fields are required");
        return;
    }

    if (phone.length !== 10 || isNaN(phone)) {
        alert("Phone number must be 10 digits");
        return;
    }

    if (new Date(dob).getFullYear() > 2006) {
        alert("You must be at least 18 years old");
        return;
    }

    if (!["Aadhar Card", "Voter Id"].includes(idType)) {
        alert("Identification type must be 'Aadhar Card' or 'Voter Id'");
        return;
    }

    if (idType === "Aadhar Card" && !/^\d{12}$/.test(idNumber)) {
        alert("Aadhar Card must have 12 digits");
        return;
    }

    if (idType === "Voter Id" && !/^[A-Z]{3}[0-9]{7}$/.test(idNumber)) {
        alert("Voter ID must start with 3 uppercase letters followed by 7 digits");
        return;
    }

    if (!consent) {
        alert("You must consent to the terms");
        return;
    }

    let formData = new FormData();
    formData.append("fullName", fullName);
    formData.append("email", email);
    formData.append("phone", phone);
    formData.append("dateOfBirth", dob);
    formData.append("sex", sex);
    formData.append("address", address);
    formData.append("identificationType", idType);
    formData.append("identificationNumber", idNumber);
    formData.append("password", password);
    formData.append("consent", consent);

    // Add files if present
    if (idDocument) formData.append("idDocument", idDocument);
    if (photo) formData.append("photo", photo);

    try {
        // Register Voter
        let response = await fetch("/api/voters/register", {
            method: "POST",
            body: formData,
        });

        let result = await response.json();
        if (response.status === 201) {
            alert(result.message);
            let uniqueId = result.UniqueId;

            // Upload files separately
            if (photo) await uploadFile("/api/voters/upload-photo", uniqueId, photo);
            if (idDocument) await uploadFile("/api/voters/upload-id", uniqueId, idDocument);

            alert("Registration & file uploads completed successfully!");
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
});

// Function to upload files (photo & ID document)
async function uploadFile(endpoint, uniqueId, file) {
    let formData = new FormData();
    formData.append("UniqueId", uniqueId);
    formData.append(file.name.includes("photo") ? "photo" : "idDocument", file);

    let response = await fetch(endpoint, {
        method: "POST",
        body: formData,
    });

    let result = await response.json();
    if (response.status !== 200) {
        alert(result.error);
    }
}
