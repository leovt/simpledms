from django.forms import ModelForm, CheckboxSelectMultiple, DateInput, RadioSelect

from .models import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'subject', 'tags', 'document_date', 'document_amount']
        widgets = {
            'tags': CheckboxSelectMultiple,
            'document_date': DateInput(attrs={'type': 'date'}),
            'status': RadioSelect,
            }
