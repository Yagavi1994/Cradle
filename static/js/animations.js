// Animate Header

window.addEventListener('load', function () {
    // Add the 'fade-in' class to trigger animations
    document.querySelectorAll('.fade-in').forEach(function (element) {
        element.classList.add('fade-in');
    });
});


/* Animate post */

document.addEventListener('DOMContentLoaded', function () {
    const posts = document.querySelectorAll('.post-animate');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    posts.forEach(post => {
        observer.observe(post);
    });
});

