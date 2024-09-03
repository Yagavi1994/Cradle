// Animate Header

window.addEventListener('load', function () {
    // Add the 'fade-in' class to trigger animations
    document.querySelectorAll('.fade-in').forEach(function (element) {
        element.classList.add('fade-in');
    });
});


/* Animate post */

// Add this script in your HTML or an external JavaScript file
document.addEventListener('DOMContentLoaded', function () {
    const posts = document.querySelectorAll('.post-animate');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Optional: Stop observing once the animation has been triggered
            }
        });
    }, {
        threshold: 0.1 // Adjust this value to determine when the animation should trigger
    });

    posts.forEach(post => {
        observer.observe(post);
    });
});


// Stop dropdown-menu from flickering

document.querySelector('.dropdown').addEventListener('show.bs.dropdown', function () {
    document.body.classList.add('paused-animation');
});

document.querySelector('.dropdown').addEventListener('hide.bs.dropdown', function () {
    document.body.classList.remove('paused-animation');
});
