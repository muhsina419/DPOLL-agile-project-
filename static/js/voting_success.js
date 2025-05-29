function returnToDashboard() {
    // Replace with actual route
    window.location.href = "/api/dashboard/";
  }
  
  window.onload = () => {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString();
    const formattedDate = now.toLocaleDateString();
    document.getElementById("dateTime").textContent = `${formattedTime}  ${formattedDate}`;
  };
  