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
  new Choices(categoryDropdown, { // jshint ignore:line
    searchEnabled: true, // Enables search within the dropdown
    itemSelectText: '',  // Remove default 'Press to select' text
  });

  // Optional: Redirect to the selected URL on change
  categoryDropdown.addEventListener('change', function () {
    window.location.href = this.value;
  });
});


/* 
Back to Top Button
This script controls the visibility and functionality of a "Back to Top" button.
* - The button becomes visible when the user scrolls down more than 100px from the top.
* - When clicked, it smoothly scrolls the page back to the top.

**Details:**
* - The window's `onscroll` event is used to show/hide the button based on the scroll position.
* - The button click event triggers a smooth scroll animation to the top of the page.
*/

// Get the "Back to Top" button element by its ID
const backToTopBtn = document.getElementById("backToTopBtn");

// Show or hide the button when the user scrolls 100px from the top
window.onscroll = function() {
  // Check the vertical scroll position for both the body and HTML document
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    backToTopBtn.style.display = "block"; // Show the button
  } else {
    backToTopBtn.style.display = "none"; // Hide the button
  }
};

// Smooth scroll to the top of the page when the "Back to Top" button is clicked
backToTopBtn.addEventListener('click', function() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});
