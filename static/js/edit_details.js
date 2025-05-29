document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('updateForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        // Retrieve the unique ID from local storage
        const uniqueId = localStorage.getItem('id');
        if (!uniqueId) {
            alert('User ID not found. Please log in again.');
            return;
        }

        // Collect form data
        const form = e.target;
        const formData = {
            unique_id: uniqueId,
            fullName: form.fullName.value.trim(),
            email: form.email.value.trim(),
            phone: form.phone.value.trim(),
            dob: form.dob.value.trim(),
            address: form.address.value.trim(),
        };

        // Validate form data before sending
        if (!formData.fullName || !formData.email || !formData.phone || !formData.dob || !formData.address) {
            alert('All fields are required.');
            return;
        }

        const messageElement = document.getElementById('responseMessage');
        if (!messageElement) {
            console.error("Element with ID 'responseMessage' not found.");
            return; // Exit early
        }

        messageElement.textContent = "Updating...";
        messageElement.style.color = 'black';

        try {
            const response = await fetch('/api/edit-details/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const result = await response.json();
                messageElement.textContent = result.message || "Details updated successfully!";
                messageElement.style.color = 'green';
            } else {
                const error = await response.json();
                messageElement.textContent = error.error || "Error updating details.";
                messageElement.style.color = 'red';
            }
        } catch (error) {
            console.error(error);
            messageElement.textContent = "Network error. Please try again.";
            messageElement.style.color = 'red';
        }
    });

    document.getElementById('resetForm').addEventListener('click', function () {
        document.getElementById('updateForm').reset();
        const messageElement = document.getElementById('responseMessage');
        if (messageElement) {
            messageElement.textContent = "";
        }
    });
});