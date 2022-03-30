from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Document, Tag

import pdf2image

# Create your views here.
def index(request):
    return HttpResponse("Hello, this is the sdms index.")

def document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'sdms/document.html', {'document': document, 'tags': Tag.objects.all()})

def preview(request, document_id, page):
    document = get_object_or_404(Document, id=document_id)
    image = pdf2image.convert_from_path(document.file.path, first_page=page, last_page=page, dpi=100)[0]
    response = HttpResponse()
    response.headers['Content-Type']="image/png"
    image.save(response, "PNG")
    return response
