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
