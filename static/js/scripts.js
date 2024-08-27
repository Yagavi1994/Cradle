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

// Search query

function checkSearchQuery() {
  var query = document.getElementById('searchInput').value.trim();
  if (query === "") {
    // Prevent the form from submitting if the query is empty
    return false;
  }
  return true; // Allow the form to submit if there is a query
}

// To add and remove favourites.

function toggleFavourite(element) {
  var postId = element.getAttribute('data-post-id');
  var isFavourite = element.classList.contains('fa-strong');
  var url = isFavourite ? '/remove_favourite/' : '/add_favourite/';
  var method = 'POST';

  var xhr = new XMLHttpRequest();
  xhr.open(method, url + postId + '/', true);
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        if (isFavourite) {
          element.classList.remove('fa-strong');
          element.classList.add('fa-regular');
        } else {
          element.classList.remove('fa-regular');
          element.classList.add('fa-strong');
        }
      } else {
        console.error('Error toggling favourite:', xhr.responseText);
      }
    }
  };

  xhr.send();
}

// Helper function to get CSRF token from cookies

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Delete Account

let deleteModalNew = new bootstrap.Modal(document.getElementById("deleteModal2"));
let deleteAccount = document.getElementById("delete-account");

deleteAccount.addEventListener("click", (e) => {
    deleteAccount.innerText = "Update"
    deleteModalNew.show(); 
});


// Add highlights to comments

document.addEventListener("DOMContentLoaded", function() {
  // Check if there is a hash in the URL
  var commentId = window.location.hash.substring(1);

  if (commentId) {
      var commentElement = document.getElementById(commentId);
      
      if (commentElement) {
          // Add the highlight class
          commentElement.classList.add('comment-highlight');
          setTimeout(function() {
              commentElement.classList.remove('comment-highlight');
          }, 3000); 
      }
  }
});