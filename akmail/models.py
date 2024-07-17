from django.db import models
from django.contrib.auth.models import User

class Email(models.Model):
    FOLDER_CHOICES = [
        ('inbox', 'Inbox'),
        ('starred', 'Starred'),
        ('drafts', 'Drafts'),
        ('outbox', 'Outbox'),
        ('important', 'Important'),
        ('bin', 'Bin'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    from_email = models.EmailField()
    receiver_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    folder = models.CharField(max_length=10, choices=FOLDER_CHOICES, default='inbox')
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class Attachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.file.name
