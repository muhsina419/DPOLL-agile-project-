document.querySelector('.submit-btn').addEventListener('click', function() {
    const unique_id = document.getElementById('unique-id').value;
    const password = document.getElementById('password').value;

    if (!unique_id || !password) {
        alert('Please fill in all fields.');
        return;
    }

    fetch('api/login_voter/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ unique_id, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = '/api/otp/';  // Redirect to dashboard
        } else {
            alert('Error: ' + JSON.stringify(data));
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
