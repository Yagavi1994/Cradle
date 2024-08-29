// Add and remove favourites
document.addEventListener('DOMContentLoaded', function () {
    const heartIcon = document.querySelector('.heart-icon');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    heartIcon.addEventListener('click', function (event) {
        const postId = event.target.dataset.postId;

        if (!postId) {
            alert('Post ID is missing!');
            return;
        }

        // Use the URL passed from the HTML
        const url = addRemoveFavouriteUrl;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ post_id: postId }),
        })
        .then(response => response.json())
        .then(data => {
            let alertBox = document.createElement('div');
            alertBox.className = 'alert alert-dismissible fade show';
            alertBox.role = 'alert';

            if (data.success) {
                if (data.added) {
                    event.target.classList.remove('fa-regular');
                    event.target.classList.add('fa-solid');
                    alertBox.classList.add('alert-success');
                    alertBox.innerHTML = 'Post added to your favourites successfully!';
                } else {
                    event.target.classList.remove('fa-solid');
                    event.target.classList.add('fa-regular');
                    alertBox.classList.add('alert-info');
                    alertBox.innerHTML = 'Post removed from your favourites successfully!';
                }
            } else {
                alertBox.classList.add('alert-danger');
                alertBox.innerHTML = 'There was an error processing your request.';
            }

            // Append the alert box to the #alert-container div
            alertBox.classList.add('custom-alert');
            const alertContainer = document.getElementById('alert-container');
            alertContainer.appendChild(alertBox);

            // Automatically remove the alert after 2 seconds
            setTimeout(function () {
                alertBox.classList.remove('show');
                alertBox.classList.add('fade');
                alertBox.addEventListener('transitionend', function () {
                    alertBox.remove();
                });
            }, 2000);
        })
        .catch(error => console.error('Error:', error));
    });
});
