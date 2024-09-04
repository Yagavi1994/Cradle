// Search query

function checkSearchQuery() {
  var query = document.getElementById('searchInput').value.trim();
  if (query === "") {
    // Prevent the form from submitting if the query is empty
    return false;
  }
  return true; // Allow the form to submit if there is a query
}

// Back to top

document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('click', function (event) {
    if (event.target && event.target.id === 'backToTopBtn') {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  });
});


// Choices Dropdown Menu

document.addEventListener('DOMContentLoaded', function () {
  var categoryDropdown = document.getElementById('categoryDropdown');
  const choices = new Choices(categoryDropdown, {
    searchEnabled: true, // Enables search within the dropdown
    itemSelectText: '',  // Remove default 'Press to select' text
  });

  // Optional: Redirect to the selected URL on change
  categoryDropdown.addEventListener('change', function () {
    window.location.href = this.value;
  });
});