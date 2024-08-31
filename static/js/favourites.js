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
            .then(response => {
                let alertBox = document.createElement('div');
                alertBox.className = 'alert alert-dismissible fade show';
                alertBox.role = 'alert';

                if (response.status === 401) {
                    alertBox.classList.add('alert-warning');
                    alertBox.innerHTML = 'Please login to add this post to your favourites.';
                    displayAlert(alertBox);
                    return;
                }

                if (!response.ok) {
                    alertBox.classList.add('alert-danger');
                    alertBox.innerHTML = 'There was an error processing your request.';
                    displayAlert(alertBox);
                    throw new Error('Unexpected error occurred: ' + response.statusText);
                }

                return response.json();
            })
            .then(data => {
                if (!data) return; // If the response is null due to early return

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

                displayAlert(alertBox);
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                let alertBox = document.createElement('div');
                alertBox.className = 'alert alert-dismissible fade show alert-danger';
                alertBox.role = 'alert';
                alertBox.innerHTML = 'There was an error processing your request.';
                displayAlert(alertBox);
                console.error('Error:', error);
            });
    });

    function displayAlert(alertBox) {
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
    }
});