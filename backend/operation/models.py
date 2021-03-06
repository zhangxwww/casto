from django.db import models

# Create your models here.
class Operation(models.Model):
    raw_image = models.CharField(max_length=128)
    raw_image_name = models.CharField(max_length=128, default='image.jpg')
    crop = models.CharField(max_length=128, default='')
    gender = models.CharField(max_length=128, default='')
    emotion = models.CharField(max_length=128, default='')
    type = models.CharField(max_length=128, default='')
    upload_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True)

