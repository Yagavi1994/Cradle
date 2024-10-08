from django import forms
from .models import Comment, Profile
from cloudinary.forms import CloudinaryFileField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    """
    Form for submitting a comment on a blog post.
    """
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3,
            }),
        }


class ProfilePictureForm(forms.ModelForm):
    """
    Form for updating profile pictures or selecting predefined avatars.
    """
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
                {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'auto'},  # noqa
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
            raise forms.ValidationError(
                'You must select an avatar or upload a profile picture.'
            )

        return cleaned_data


class DeletePictureForm(forms.Form):
    """
    Form to confirm deletion of the profile picture.
    """
    confirm = forms.BooleanField(label="Confirm Deletion")


class CustomSignUpForm(UserCreationForm):
    """
    Custom sign-up form that extends the UserCreationForm to include
    email and apply Bootstrap styles to form fields.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
