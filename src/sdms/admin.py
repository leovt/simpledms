from django.contrib import admin
from django.forms.widgets import TextInput

# Register your models here.
from .models import Tag, Document

admin.site.register(Document)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        print(kwargs)
        kwargs['widgets'] = {
            'text_color': TextInput(attrs={'type': 'color'}),
            'fill_color': TextInput(attrs={'type': 'color'}),
        }
        return super().get_form(request, obj, **kwargs)
