from django.db import models


class Contact(models.Model):
    """
    Model representing a contact message sent via a contact form.

    **Fields:**

    - name: The name of the person sending the message.
    - email: The email of the person sending the message.
    - message: The content of the message.
    - read: A boolean flag indicating if the message has been read.
    - created_on: The date and time when the message was created.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
