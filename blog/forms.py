from django import forms
from .models import Comment, Profile
from cloudinary.forms import CloudinaryFileField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
    profile_picture = CloudinaryFileField(
        options = {
            'folder': 'profile_pictures',
            'tags': ['profile_pic'],
            'format': 'jpg',
            'crop': 'limit', 'width': 200, 'height': 200, 
            'folder': 'profile_pictures',
        }
    )

class DeletePictureForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm Deletion")