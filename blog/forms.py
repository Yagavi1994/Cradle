from django import forms
from .models import Comment, Profile
from cloudinary.forms import CloudinaryFileField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ProfilePictureForm(forms.ModelForm):
    AVATAR_CHOICES = [
        ('selected_avatar', 'Avatar 1'),
        ('selected_avatar1', 'Avatar 2'),
        ('selected_avatar2', 'Avatar 3'),
        ('selected_avatar3', 'Avatar 4'),
    ]

    avatar_choice = forms.ChoiceField(
        choices=AVATAR_CHOICES,
        required=False,
        label="Select a predefined avatar"
    )

    profile_picture = CloudinaryFileField(
        options={
            'folder': 'profile_pictures',
            'tags': ['profile_pic'],
            'format': 'jpg',
            'transformation': [
                {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'auto'},
                {'quality': 'auto:best'}
            ]
        },
        required=False,
        label="Or upload a custom profile picture"
    )

    class Meta:
        model = Profile
        fields = ['profile_picture', 'avatar_choice']

    def clean(self):
        cleaned_data = super().clean()
        avatar_choice = cleaned_data.get('avatar_choice')
        profile_picture = cleaned_data.get('profile_picture')

        if not avatar_choice and not profile_picture:
            raise forms.ValidationError('You must select an avatar or upload a profile picture.')

        return cleaned_data


class DeletePictureForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm Deletion")