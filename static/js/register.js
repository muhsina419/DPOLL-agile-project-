document.addEventListener("DOMContentLoaded", function() { 
    document.getElementById("registerForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        console.log("Form submission started");

        // Collect form values with null checks
        let fullNameElement = document.getElementById("fullname");
        let emailElement = document.getElementById("email");
        let phoneElement = document.getElementById("phone");
        let dobElement = document.getElementById("dob");
        let sexElement = document.querySelector('input[name="sex"]:checked');
        let addressElement = document.getElementById("address");
        let idTypeElement = document.getElementById("identificationInput");
        let idNumberElement = document.getElementById("idNumber");
        let idDocumentElement = document.getElementById("id_doc");
        let photoElement = document.getElementById("photo");
        let consentElement = document.getElementById("consent");

        if (!fullNameElement || !emailElement || !phoneElement || !dobElement || !sexElement || !addressElement || 
            !idTypeElement || !idNumberElement || !idDocumentElement || !photoElement || !consentElement) {
            alert("All form elements must be present");
            return;
        }

        let fullName = fullNameElement.value.trim();
        let email = emailElement.value.trim();
        let phone = phoneElement.value.trim();
        let dob = dobElement.value.trim();
        let sex = sexElement.value;
        let address = addressElement.value.trim();
        let idType = idTypeElement.value.trim();
        let idNumber = idNumberElement.value.trim();
        let idDocument = idDocumentElement.files[0];
        let photo = photoElement.files[0];
        let consent = consentElement.checked;

        // **Validations**
        if (!fullName || !email || !phone || !dob || !sex || !address || !idType || !idNumber || !consent || !idDocument || !photo) {
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

        // File type validations
        const validImageTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const validDocumentTypes = ['application/pdf'];

        if (!validImageTypes.includes(photo.type)) {
            alert("Photo must be in JPG, JPEG, or PNG format");
            return;
        }

        if (!validDocumentTypes.includes(idDocument.type)) {
            alert("ID Document must be in PDF format");
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
        formData.append("consent", consent);
        formData.append("id_doc", idDocument);
        formData.append("photo", photo);

        try {
            console.log("Sending registration request");
            let response = await fetch("/api/register/", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            let responseData = await response.json();
            console.log("Response Data:", responseData);
            alert(responseData.message);

            window.location.href = "http://127.0.0.1:8000/api/setpassword/";
            
        } catch (error) {
            console.error("Error during registration:", error);
            alert("Something went wrong during registration!");
        }
    });
});


function uploadFile(endpoint, uniqueId, file) {
    let formData = new FormData();
    formData.append("UniqueId", uniqueId);
    formData.append(file.name.includes("photo") ? "photo" : "id_doc", file);

    console.log(`Uploading file to ${endpoint}`);

    return fetch(endpoint, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
            return null;
        } else {
            console.log("File uploaded successfully:", result.file_url);
            return result.file_url;
        }
    })
    .catch(error => {
        console.error("Error during file upload:", error);
        alert("Something went wrong during file upload!");
        return null;
    });
}
