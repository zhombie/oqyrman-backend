from django.db import models
from django.urls import reverse


def upload_location(instance, filename):
    return "%s/%s" % (instance, filename)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    epub_cyrillic = models.FileField(upload_to="epub_cyrillic/", null=True, blank=True)
    epub_latin = models.FileField(upload_to="epub_latin/", null=True, blank=True)
    description = models.TextField()
    section_id = models.IntegerField(default=0)
    section_name = models.CharField(max_length=200, default="null")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]