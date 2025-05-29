// Filter candidates by search
const searchInput = document.getElementById('search-input');
const candidateRows = document.querySelectorAll('#candidate-body tr');

 
searchInput.addEventListener('input', function () {
  const value = this.value.toLowerCase();
  candidateRows.forEach(row => {
    const name = row.cells[1].textContent.toLowerCase();
    row.style.display = name.includes(value) ? '' : 'none';
  });
});


