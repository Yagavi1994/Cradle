// Animate Header

window.addEventListener('load', function () {
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
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 
    });

    posts.forEach(post => {
        observer.observe(post);
    });
});

