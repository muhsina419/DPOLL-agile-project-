document.addEventListener("DOMContentLoaded", function () {
    const uniqueId = localStorage.getItem('id'); // Retrieve unique_id from local storage
    if (uniqueId) {
        fetch(`api/get_user_photo/?unique_id=${uniqueId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    // Update the profile image
                    const userImage = document.getElementById('userImage');
                    if (userImage) {
                        userImage.src = data.photo;
                    }
                }
            })
            .catch(error => console.error('Error fetching user photo:', error));
    } else {
        console.error('Unique ID not found in local storage.');
    }

    // Sidebar toggle
    const sidebar = document.getElementById('sidebar');
    const menu = document.getElementById('menu-icon');

    menu.addEventListener("click", () => {
        // Toggle the sidebar's transform property
        const isHidden = sidebar.style.transform === "translateX(-100%)" || !sidebar.style.transform;
        sidebar.style.transform = isHidden ? "translateX(0)" : "translateX(-100%)";
    });

    // Sidebar Navigation
    document.querySelectorAll(".sidebar li").forEach(item => {
        item.addEventListener("click", () => {
            const link = item.getAttribute("data-link");
            if (link) window.location.href = link;
        });
    });

    // User profile dropdown
    const userImage = document.getElementById("userImage");
    const userDetails = document.getElementById("userDetails");

    if (userImage && userDetails) {
        userImage.addEventListener("click", (e) => {
            e.stopPropagation();
            userDetails.classList.toggle("hidden");
        });

        document.addEventListener("click", (e) => {
            if (!userDetails.contains(e.target) && e.target !== userImage) {
                userDetails.classList.add("hidden");
            }
        });
    }
});