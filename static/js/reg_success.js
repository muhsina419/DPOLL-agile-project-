// Example: Automatically copy the unique ID on click
document.getElementById('uniqueId').addEventListener('click', function () {
  this.select();
  document.execCommand('copy');
  alert('Unique ID copied to clipboard!');
});

document.getElementById('gotoDashboard').addEventListener('click', function () {
    window.location.href = "/api/login/";
});

// Optional: Auto-redirect after 5 seconds
// setTimeout(function() {
//     window.location.href = "/api/dashboard/";
// }, 5000);