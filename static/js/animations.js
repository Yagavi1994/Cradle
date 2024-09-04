/* jshint esversion: 6 */


/* 
Animate Header
Adds the 'fade-in' class to all elements with the class 'fade-in' when the 
page is fully loaded, triggering a CSS animation.

**Details:**
- The window's 'load' event is used to ensure all resources (e.g., images, 
  stylesheets) are fully loaded before running the animation.
- The querySelectorAll method selects all elements with the 'fade-in' class.
- For each selected element, the 'fade-in' class is added again (if necessary) 
  to trigger the CSS fade-in animation.
*/
window.addEventListener('load', function () {
    document.querySelectorAll('.fade-in').forEach(function (element) {
        // Add the 'fade-in' class to each selected element
        element.classList.add('fade-in');
    });
});


/* 
Animate Post
Adds a 'visible' class to post elements with the class 'post-animate' 
as they come into view while scrolling.

**Details:**
- Uses the Intersection Observer API to detect when the posts become visible 
  in the viewport.
- An observer is created with a threshold of 0.1, meaning 10% of the element 
  must be visible for it to trigger the visibility change.
- Each post with the class 'post-animate' is observed. When it becomes 
  visible, the 'visible' class is added to trigger the animation.
- Once a post becomes visible, the observer stops observing it to prevent 
  unnecessary re-triggering.
*/
document.addEventListener('DOMContentLoaded', function () {
    const posts = document.querySelectorAll('.post-animate');

    // Create an Intersection Observer to observe when elements come into view
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            // If the post is visible in the viewport, add 'visible' class
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Stop observing the post once it's been made visible
                observer.unobserve(entry.target);
            }
        });
    }, {
        // Set the threshold to 0.1, meaning 10% of the element must be visible
        threshold: 0.1
    });

    // Observe each post element
    posts.forEach(function (post) {
        observer.observe(post);
    });
});
