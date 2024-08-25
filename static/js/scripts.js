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

function checkSearchQuery() {
  var query = document.getElementById('searchInput').value.trim();
  if (query === "") {
    // Prevent the form from submitting if the query is empty
    return false;
  }
  return true; // Allow the form to submit if there is a query
}


function toggleFavourite(element) {
  var postId = element.getAttribute('data-post-id');
  var isFavourite = element.classList.contains('fa-strong');

  if (isFavourite) {
    // If it is already a favourite, remove from favourites
    $.ajax({
      url: '/remove_favourite/' + postId + '/',
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
      },
      success: function (response) {
        element.classList.remove('fa-strong');
        element.classList.add('fa-regular');
      },
      error: function (xhr, status, error) {
        console.log('Error:', error);
      }
    });
  } else {
    // If it's not a favourite, add to favourites
    $.ajax({
      url: '/add_favourite/' + postId + '/',
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
      },
      success: function (response) {
        element.classList.remove('fa-regular');
        element.classList.add('fa-strong');
      },
      error: function (xhr, status, error) {
        console.log('Error:', error);
      }
    });
  }
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
