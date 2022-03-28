from django.contrib import admin

# Register your models here.
from .models import Tag, Document

admin.site.register(Tag)
admin.site.register(Document)
