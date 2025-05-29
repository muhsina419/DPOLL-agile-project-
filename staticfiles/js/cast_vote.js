document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("candidateTableBody");
    const form = document.getElementById("votingForm");
    const clearBtn = document.getElementById("clearBtn");
    let checkboxes = []; // Declare checkboxes at a broader scope

    // Fetch candidates from backend
    fetch("/api/candidates")
        .then(response => response.json())
        .then(candidates => {
            if (!Array.isArray(candidates) || candidates.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="5">No candidates available.</td></tr>`;
                return;
            }

            tableBody.innerHTML = "";
            candidates.forEach((candidate, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${candidate.name}</td>
                    <td><img src="${candidate.photo ? candidate.photo : '/static/images/default-photo.jpg'}" class="avatar" alt="Photo" /></td>
                    <td><img src="${candidate.symbol ? candidate.symbol : '/static/images/default-symbol.png'}" class="symbol-img" alt="Symbol" /></td>
                    <td><input type="checkbox" name="vote" value="${candidate._id}" class="vote-checkbox" /></td>
                `;
                tableBody.appendChild(row);
            });

            // Initialize checkboxes after candidates are loaded
            checkboxes = document.querySelectorAll(".vote-checkbox");
            console.log("checkboxes initialized",checkboxes);
            setupSingleSelection();
        })
        .catch(err => {
            console.error("Failed to load candidates:", err);
            tableBody.innerHTML = `<tr><td colspan="5">Error loading candidates.</td></tr>`;
        });

    function setupSingleSelection() {
        checkboxes.forEach(box => {
            box.addEventListener("change", () => {
                if (box.checked) {
                    console.log('Checkbox selected: ${box.value}');
                    checkboxes.forEach(cb => {
                        if (cb !== box) cb.checked = false;
                    });
                }
            });
        });

        clearBtn.addEventListener("click", () => {
            checkboxes.forEach(cb => cb.checked = false);
        });
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        console.log("Form submitted")
        const selected = [...checkboxes].find(cb => cb.checked); // Now checkboxes is accessible here

        if (!selected) {
            alert("Please select a candidate before submitting.");
            return;
        }

        const uniqueIdElement = localStorage.getItem("id")
        if (!uniqueIdElement) {
            alert("Unique ID is missing. Please log in again.");
            return;
        }
        
        const voteData = {
            unique_id: uniqueIdElement, // Fetch unique_id from the hidden input
            candidate_id: selected.value
        };

        // Store unique_id and candidate_id in local storage
        const uniqueId = uniqueIdElement;
        const candidateId = selected.value;
        console.log("storing unique id and candidate id")
        localStorage.setItem("unique_id", uniqueId);
        localStorage.setItem("candidate_id", candidateId);


        fetch("/api/submit-vote/", { // Ensure the URL matches your backend
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(voteData)
        })
            .then(res => {
                if (!res.ok) {
                    if (res.status === 403) {
                        throw new Error("You have already voted.");
                    }
                    throw new Error("Vote submission failed");
                }
                return res.json();
            })
            .then(data => {
                console.log("Vote submitted successfully:", data);
                alert("Vote submitted successfully!");
            })
            .catch(err => {
                console.error("Error submitting vote:", err);
                alert(err.message);
            });
    });
});