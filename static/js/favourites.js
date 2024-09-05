/* jshint esversion: 6 */
/* global addRemoveFavouriteUrl */

/* 
Add and Remove Favourites
Handles the logic for adding and removing a post from the user's favourites 
when the heart icon is clicked.

**Details:**
- The heart icon click event is captured to trigger a fetch request to add or 
  remove the post from favourites.
- The CSRF token is included in the headers to ensure the request is secure.
- The server response determines whether the post is added or removed from 
  the user's favourites, and the heart icon's style changes accordingly.
- Alerts are dynamically generated to provide feedback to the user about 
  the success or failure of the action.
*/

document.addEventListener('DOMContentLoaded', function () {
    const heartIcon = document.querySelector('.heart-icon');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Event listener for the heart icon click event
    heartIcon.addEventListener('click', function (event) {
        // Retrieve the post ID from the clicked heart icon
        const postId = event.target.dataset.postId;

        // If postId is missing, show an alert and return
        if (!postId) {
            alert('Post ID is missing!');
            return;
        }

        // Use the URL passed from the HTML
        const url = addRemoveFavouriteUrl;

        // Send a POST request to add or remove the post from favourites
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

                // If the user is not logged in, show a warning alert
                if (response.status === 401) {
                    alertBox.classList.add('alert-warning');
                    alertBox.innerHTML = 'Please login or signup to add post to your favourites.';
                    displayAlert(alertBox);
                    return;
                }

                // If the request fails, show an error alert
                if (!response.ok) {
                    alertBox.classList.add('alert-danger');
                    alertBox.innerHTML = 'There was an error processing your request.';
                    displayAlert(alertBox);
                    throw new Error('Unexpected error occurred: ' + response.statusText);
                }

                // Return the JSON response
                return response.json();
            })
            .then(data => {
                if (!data) return; // If the response is null due to early return

                let alertBox = document.createElement('div');
                alertBox.className = 'alert alert-dismissible fade show';
                alertBox.role = 'alert';

                // Check if the request was successful
                if (data.success) {
                    if (data.added) {
                        // If the post was added, change the heart icon to solid
                        event.target.classList.remove('fa-regular');
                        event.target.classList.add('fa-solid');
                        alertBox.classList.add('alert-success');
                        alertBox.innerHTML = 'Post added to your favourites successfully!';
                    } else {
                        // If the post was removed, change the heart icon to regular
                        event.target.classList.remove('fa-solid');
                        event.target.classList.add('fa-regular');
                        alertBox.classList.add('alert-info');
                        alertBox.innerHTML = 'Post removed from your favourites successfully!';
                    }
                } else {
                    // If the request failed, show an error alert
                    alertBox.classList.add('alert-danger');
                    alertBox.innerHTML = 'There was an error processing your request.';
                }

                // Display the alert
                displayAlert(alertBox);
            })
            .catch(error => {
                // If there was an error during the fetch request, show an error alert
                console.error('Error during fetch:', error);
                let alertBox = document.createElement('div');
                alertBox.className = 'alert alert-dismissible fade show alert-danger';
                alertBox.role = 'alert';
                alertBox.innerHTML = 'There was an error processing your request.';
                displayAlert(alertBox);
                console.error('Error:', error);
            });
    });

    // Function to display alerts
    /**
     * Dynamically adds an alert to the page and removes it after 2 seconds.
     * 
     * @param {HTMLElement} alertBox - The alert element to display.
     */
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
        }, 3000);
    }
});
