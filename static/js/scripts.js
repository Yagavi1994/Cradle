/* jshint esversion: 6 */
/* global Choices */


// Choices Dropdown Menu
/**
 * Initializes a searchable dropdown menu using the Choices.js library for a category dropdown.
 * 
 * - The dropdown allows the user to search within the options.
 * - The default "Press to select" text is removed for better UX.
 * - When the user selects an option, the page redirects to the URL associated with that option.
 */
document.addEventListener('DOMContentLoaded', function () {
  var categoryDropdown = document.getElementById('categoryDropdown');
  
  // Initialize Choices.js for the dropdown with search enabled
  const choices = new Choices(categoryDropdown, {
    searchEnabled: true, // Enables search within the dropdown
    itemSelectText: '',  // Remove default 'Press to select' text
  });

  // Optional: Redirect to the selected URL on change
  categoryDropdown.addEventListener('change', function () {
    window.location.href = this.value;
  });
});