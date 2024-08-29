document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const imgPreview = document.getElementById('imgPreview');
    const errorMessage = document.getElementById('error-message');
    const avatars = document.querySelectorAll('.avatar');
    const radioButtons = document.querySelectorAll('input[name="selected_avatar"]');

    // Preview for uploaded image
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

                // Unselect all avatars if a custom image is uploaded
                avatars.forEach(av => av.classList.remove('selected'));
                radioButtons.forEach(rb => rb.checked = false);
            };
            reader.readAsDataURL(file);
        }
    });

    // Avatar selection
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

            // Clear the file input
            fileInput.value = '';  // Clear the uploaded file if an avatar is selected
        });
    });
});
