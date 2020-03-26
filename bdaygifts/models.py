from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms

# Create your models here.

GIFTEE_CHOICES=[
    ('Tim', 'Tim'),
    ('Karen', 'Karen')
]

class Gift(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    recipient=models.CharField(max_length=20, default='None',choices=GIFTEE_CHOICES)
    img=models.ImageField(default='corey.jpg', upload_to="bdaygifts-pics")
    hover=models.CharField(max_length=100, default='')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gift-detail', kwargs={'pk': self.pk})


