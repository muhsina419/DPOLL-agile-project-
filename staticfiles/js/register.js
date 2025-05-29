document.addEventListener("DOMContentLoaded", function () { 
    document.getElementById("registerForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        console.log("Form submission started");
        // Collect form values
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

            if (responseData.unique_id) {  // Ensure unique_id is present
                alert(responseData.message);
                window.location.href = `/api/setpassword/${responseData.unique_id}/`;
            } else {
                alert("Unique ID not received. Registration failed.");
            }

        } catch (error) {
            console.error("Error during registration:", error);
            alert("Something went wrong during registration!");
        }
    });
});
