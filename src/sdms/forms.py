from django.forms import ModelForm, CheckboxSelectMultiple, DateInput, RadioSelect, TextInput

from .models import Document, Tag


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'subject', 'counterparty', 'tags', 'document_date', 'document_amount']
        widgets = {
            'tags': CheckboxSelectMultiple,
            'document_date': DateInput(attrs={'type': 'date'}),
            'status': RadioSelect,
            }

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'subtag', 'fill_color', 'text_color']
        widgets = {
            'name': TextInput(attrs={'size': '12'}),
            'subtag': TextInput(attrs={'size': '12'}),
            'text_color': TextInput(attrs={'type': 'color'}),
            'fill_color': TextInput(attrs={'type': 'color'}),
        }
