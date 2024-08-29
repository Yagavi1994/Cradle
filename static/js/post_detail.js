// Variables

const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");


// Edit Comment
/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    let commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    commentText.classList.add('comment-highlight');
    setTimeout(function () {
      commentText.classList.remove('comment-highlight');
    }, 3000);
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}

// Delete Comment
/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    deleteConfirm.href = `delete_comment/${commentId}`;
    deleteModal.show();
  });
}

// // Add and Remove Favourites

// document.addEventListener('DOMContentLoaded', function () {
//     const heartIcon = document.querySelector('.heart-icon');
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     heartIcon.addEventListener('click', function (event) {
//         const postId = event.target.dataset.postId;

//         if (!postId) {
//             alert('Post ID is missing!');
//             return;
//         }

//         // Use the URL passed from the HTML
//         const url = addRemoveFavouriteUrl;

//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrfToken,
//             },
//             body: JSON.stringify({ post_id: postId }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             let alertBox = document.createElement('div');
//             alertBox.className = 'alert alert-dismissible fade show';
//             alertBox.role = 'alert';

//             if (data.success) {
//                 if (data.added) {
//                     event.target.classList.remove('fa-regular');
//                     event.target.classList.add('fa-solid');
//                     alertBox.classList.add('alert-success');
//                     alertBox.innerHTML = 'Post added to your favourites successfully!';
//                 } else {
//                     event.target.classList.remove('fa-solid');
//                     event.target.classList.add('fa-regular');
//                     alertBox.classList.add('alert-info');
//                     alertBox.innerHTML = 'Post removed from your favourites successfully!';
//                 }
//             } else {
//                 alertBox.classList.add('alert-danger');
//                 alertBox.innerHTML = 'There was an error processing your request.';
//             }

//             // Append the alert box to the #alert-container div
//             alertBox.classList.add('custom-alert');
//             const alertContainer = document.getElementById('alert-container');
//             alertContainer.appendChild(alertBox);

//             // Automatically remove the alert after 2 seconds
//             setTimeout(function () {
//                 alertBox.classList.remove('show');
//                 alertBox.classList.add('fade');
//                 alertBox.addEventListener('transitionend', function () {
//                     alertBox.remove();
//                 });
//             }, 2000);
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });
