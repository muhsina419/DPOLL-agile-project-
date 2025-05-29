function filterVoters() {
  const searchInput = document.querySelector('.search-box').value.toLowerCase();
  const voterRows = document.querySelectorAll('.table-row:not(.header)');

  voterRows.forEach(row => {
    const voterName = row.querySelector('.name').textContent.toLowerCase();
    const voterId = row.querySelector('.uid').textContent.toLowerCase();

    if (voterName.includes(searchInput) || voterId.includes(searchInput)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Attach the search functionality
document.querySelector('.search-box').addEventListener('keyup', filterVoters);