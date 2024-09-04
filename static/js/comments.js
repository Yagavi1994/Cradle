/* jshint esversion: 6 */
/* global bootstrap */


// Variables
const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");
const cancelButton = document.getElementById("cancelButton");
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
for (var i = 0; i < editButtons.length; i++) {
    editButtons[i].addEventListener("click", function (e) {
        var commentId = e.target.getAttribute("comment_id");
        var commentContent = document.getElementById("comment" + commentId).innerText;
        
        // Populate the form with the comment content
        commentText.value = commentContent;
        
        // Highlight the comment input/textarea
        commentText.classList.add('comment-highlight');
        setTimeout(function () {
            commentText.classList.remove('comment-highlight');
        }, 3000);
        
        // Change the submit button text to "Update"
        submitButton.innerText = "Update";
        
        // Update the form action to point to the edit endpoint
        commentForm.setAttribute("action", "edit_comment/" + commentId);
        
        // Scroll to the comment form smoothly
        commentForm.scrollIntoView({ behavior: "smooth" });
    });
}

// Cancel Edit
/**
 * Resets the comment form to its default state when the user cancels editing.
 * 
 * - Clears the comment input/textarea.
 * - Resets the submit button text back to "Submit".
 * - Optionally resets the form's action attribute to the default add comment URL.
 */
cancelButton.addEventListener("click", function () {
    // Clear the comment textarea
    commentText.value = '';
    
    // Reset the submit button text
    submitButton.innerText = "Submit";
    
    // Optionally reset the form action
    commentForm.setAttribute("action", "add_comment");
});

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
for (var i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener("click", function (e) {
        var commentId = e.target.getAttribute("comment_id");
        deleteConfirm.href = "delete_comment/" + commentId;
        deleteModal.show();
    });
}

// Add highlights to comments
/**
 * Adds a highlight effect to a comment when it is directly linked via a URL hash.
 * 
 * - Checks if the URL contains a hash (indicating a specific comment).
 * - If a comment with the matching ID exists, it adds a highlight class to the comment.
 * - The highlight effect lasts for 3 seconds.
 */
document.addEventListener("DOMContentLoaded", function () {
    // Check if there is a hash in the URL
    var commentId = window.location.hash.substring(1);

    if (commentId) {
        var commentElement = document.getElementById(commentId);

        if (commentElement) {
            // Add the highlight class
            commentElement.classList.add('comment-highlight');
            setTimeout(function () {
                commentElement.classList.remove('comment-highlight');
            }, 3000);
        }
    }
});
