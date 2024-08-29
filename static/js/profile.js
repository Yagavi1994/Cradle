// Delete Account

let deleteModalNew = new bootstrap.Modal(document.getElementById("deleteModal2"));
let deleteAccount = document.getElementById("delete-account");

deleteAccount.addEventListener("click", (e) => {
  deleteAccount.innerText = "Update"
  deleteModalNew.show();
});


// Add highlights to comments

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

// Preview profile pic in edit modal

document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const imgPreview = document.getElementById('imgPreview');
    const errorMessage = document.getElementById('error-message');
    
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
            if (!validImageTypes.includes(file.type)) {
                errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, GIF, WEBP).';
                imgPreview.src = '{{ profile.profile_picture.url }}';  // Reset to current profile picture
                return;
            }
            
            // Clear the error message
            errorMessage.textContent = '';
            
            // Preview the uploaded image
            const reader = new FileReader();
            reader.onload = function (e) {
                imgPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
