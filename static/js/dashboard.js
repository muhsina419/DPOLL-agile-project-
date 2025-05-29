function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    sidebar.style.transform = sidebar.style.transform === "translateX(-100%)" ? "translateX(0)" : "translateX(-100%)";
}

function navigate(page) {
    const body = document.body;
    const urls = {
        votersList: body.dataset.votersListUrl,
        candidatesList: body.dataset.candidatesListUrl,
        castVote: body.dataset.castVoteUrl,
        result: body.dataset.resultsUrl,
        editDetails: body.dataset.editDetailsUrl
    };

    if (urls[page]) {
        window.location.href = urls[page];
    } else {
        console.error("Navigation failed: Page not found -", page);
    }
}

function logout() {
    const logoutUrl = document.body.dataset.logoutUrl;
    window.location.href = logoutUrl;
}
