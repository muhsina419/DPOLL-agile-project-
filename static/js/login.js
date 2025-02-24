<script>
    document.querySelector('.submit-btn').addEventListener('click', function() {
        const username = document.getElementById('unique-id').value;
        const password = document.getElementById('password').value;

        fetch('/myprojectdpoll/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else {
                alert('Error: ' + JSON.stringify(data));
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
    document.querySelector('.submit-btn').addEventListener('click', function() {
        const username = document.getElementById('unique-id').value;
        const password = document.getElementById('password').value;

        if (!username || !password) {
            alert('Please fill in all fields.');
            return;
        }

        // Proceed with fetch request...
    });
</script>