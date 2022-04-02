from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count

from .models import Document, Tag
from .forms import DocumentForm

import pdf2image
import dateparser.search

# Create your views here.
def index(request):
    count = {'UT': 0, 'IN': 0, 'HF': 0, 'AR': 0}
    queryset = Document.objects.all().values('status').annotate(count=Count('status'))
    count.update({x['status']: x['count'] for x in queryset})

    print(count)

    return render(request, 'sdms/index.html', count)

def guess_date(text):
    dates = set(dt.date() for x, dt in dateparser.search.search_dates(text, ['de']))
    dates = [ x for x in dates if 1900 <= x.year <= 2100 ]
    dates.sort()
    return dates


def document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            pass
            # return HttpResponseRedirect()
    else:
        form = DocumentForm(initial={
            'tags': list(document.tags.all().values_list("id", flat=True)),
            'subject': document.subject,
            'document_date': document.document_date,
            'document_amount': document.document_amount,
            })
    date_suggestions = guess_date(document.pdf_text + '\n\n' + document.ocr_text)
    tags = Tag.objects.all()
    return render(request, 'sdms/document.html', locals())

def preview(request, document_id, page):
    document = get_object_or_404(Document, id=document_id)
    image = pdf2image.convert_from_path(document.file.path, first_page=page, last_page=page, dpi=100)[0]
    response = HttpResponse()
    response.headers['Content-Type']="image/png"
    image.save(response, "PNG")
    return response
