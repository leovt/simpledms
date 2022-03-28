import uuid

from django.db import models

# Create your models here.
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    subtag = models.CharField(max_length=30)
    fill_color = models.CharField(max_length=7, default="#AFD9F3")
    text_color = models.CharField(max_length=7, default="#233038")

    def __str__(self):
        if self.subtag:
            return f'{self.name}: {self.subtag}'
        return self.name

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField()
    subject = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='documents')
