import os
from django.db import models


class ImageCollection(models.Model):
    img_src = models.ImageField(
        upload_to='imageresources/', blank=False, null=False)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Image Collection"

    def __str__(self):
        return "img(" + str(self.pk)+"): " + os.path.basename(self.img_src.name)+"-"+str(self.uploaded)
