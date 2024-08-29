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