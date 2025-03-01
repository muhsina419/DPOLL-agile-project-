function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    sidebar.style.transform = sidebar.style.transform === "translateX(-100%)" ? "translateX(0)" : "translateX(-100%)";
}

function navigate(page) {
    alert("Navigating to " + page);
}

function logout() {
    alert("Logging out...");
    window.location.href = "login.html";
}
