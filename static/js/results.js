// Fetch voting statistics from the backend
async function fetchStats() {
  try {
    const response = await fetch("/api/vote-stats/");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log("Fetched data:", data); // Debugging: Log the fetched data
    return data;
  } catch (error) {
    console.error("Failed to fetch data:", error);
    return {
      totalVotes: 0,
      candidates: [],
      trend: [0, 0, 0, 0, 0, 0, 0], // Default trend data
    };
  }
}

// Submit a vote and refresh stats
async function castVote(candidateId) {
  try {
    const response = await fetch("/vote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidateId }),
    });
    if (!response.ok) {
      throw new Error("Failed to cast vote");
    }
    console.log("Vote cast successfully");
    await renderStats(); // Refresh stats after casting vote
  } catch (error) {
    console.error("Error casting vote:", error);
  }
}

// Create a statistics card
function createStatCard(title, value, change) {
  // Create the card container
  const card = document.createElement("div");
  card.className = "stat-card";

  // Create the title element
  const titleElement = document.createElement("h3");
  titleElement.textContent = title;

  // Create the value element
  const valueElement = document.createElement("p");
  valueElement.textContent = value;

  // Create the change element (optional)
  if (change) {
    const changeElement = document.createElement("span");
    changeElement.textContent = change;
    card.appendChild(changeElement);
  }

  // Append elements to the card
  card.appendChild(titleElement);
  card.appendChild(valueElement);

  return card;
}

// Render the chart using Chart.js
function renderChart(graphData) {
  const ctx = document.getElementById("votesChart").getContext("2d");
  new Chart(ctx, {
    type: "bar", // Bar chart for votes vs. candidates
    data: {
      labels: graphData.labels, // Candidate names
      datasets: [
        {
          data: graphData.data, // Corresponding votes
          backgroundColor: "#4d90fe",
          borderColor: "rgb(75, 124, 192)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins:{
        legend:{
          display:false
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      interaction:{
        mode:false
      },
    },
  });
}


// Render all statistics and the chart
async function renderStats() {
  const data = await fetchStats();
  console.log(data); // Debugging: Log the fetched data
  const container = document.getElementById("stats-container");
  container.innerHTML = "";

  // Total Votes Card (no percentage)
  const totalVotesCard = createStatCard("Total Votes", data.totalVotes);
  container.appendChild(totalVotesCard);

  // Candidate Cards
  data.candidates.forEach((candidate) => {
    // Calculate the percentage of total votes for each candidate
    const percentage = data.totalVotes > 0 
      ? ((candidate.votes / data.totalVotes) * 100).toFixed(2) + "%" 
      : "0%";

    const card = createStatCard(`${candidate.name} Votes`, candidate.votes, percentage);
    card.addEventListener("click", () => castVote(candidate.id)); // Add click event to cast vote
    container.appendChild(card);
  });

  // Render the chart
  renderChart(data.graphData); // Use graphData from the API response
}

// Initialize the stats rendering on page load
document.addEventListener("DOMContentLoaded", renderStats);