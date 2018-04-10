import os
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible

from techwebsite.settings import MEDIA_ROOT


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)
# Create your models here.
class author_data(models.Model):
    author_fname = models.TextField()
    author_lname = models.TextField()
    author_email = models.TextField()
    author_img = models.ImageField(null=True,upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'user')))
    author_password = models.TextField()
    author_joined = models.DateField()
    def __str__(self):
        return self.author_fname + self.author_lname

class otp_generator(models.Model):
    author_id=models.ForeignKey(author_data,on_delete=models.CASCADE)
    otp=models.CharField(max_length=8)