// Display current date and time
window.onload = function () {
  const now = new Date();
  const formatted = now.toLocaleString();
  document.getElementById("dateTime").textContent = formatted;
};

// Redirect back to voting page
function retryVote() {
  window.location.href = "/api/cast-vote/"; 
}
