/* jshint esversion: 6 */

document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const imgPreview = document.getElementById('imgPreview');
    const errorMessage = document.getElementById('error-message');
    const avatars = document.querySelectorAll('.avatar');
    const radioButtons = document.querySelectorAll('input[name="selected_avatar"]');

    // Preview for uploaded image
    /**
     * Handles the change event for the file input, providing image preview functionality
     * and validating the file type.
     * 
     * - Checks if the selected file is a valid image format (JPEG, PNG, GIF, WEBP).
     * - If invalid, it shows an error message and resets the preview to the current profile picture.
     * - If valid, it clears any existing error messages and displays the uploaded image as a preview.
     */
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

            // Validate the selected file's type
            if (!validImageTypes.includes(file.type)) {
                errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, GIF, WEBP).';
                imgPreview.src = '{{ profile.profile_picture.url }}';  // Reset to current profile picture
                return;
            }

            // Clear the error message
            errorMessage.textContent = '';

            // Create a FileReader to preview the uploaded image
            const reader = new FileReader();
            reader.onload = function (e) {
                imgPreview.src = e.target.result;

                // Unselect all avatars if a custom image is uploaded
                avatars.forEach(av => av.classList.remove('selected'));
                radioButtons.forEach(rb => rb.checked = false);
            };

            // Read the uploaded file and display it as an image preview
            reader.readAsDataURL(file);
        }
    });

    // Avatar selection
    /**
     * Handles avatar selection by:
     * - Unselecting any previously selected avatar.
     * - Highlighting the clicked avatar as selected.
     * - Updating the image preview to display the selected avatar.
     * - Checking the corresponding radio button for form submission.
     * - Clearing the file input if an avatar is selected.
     */
    avatars.forEach((avatar, index) => {
        avatar.addEventListener('click', function() {
            // Unselect all avatars
            avatars.forEach(av => av.classList.remove('selected'));

            // Select the clicked avatar
            avatar.classList.add('selected');

            // Update the preview image to the selected avatar
            imgPreview.src = avatar.src;

            // Check the corresponding radio button
            radioButtons[index].checked = true;

            // Clear the file input if an avatar is selected
            fileInput.value = '';  // Clear the uploaded file
        });
    });
});
