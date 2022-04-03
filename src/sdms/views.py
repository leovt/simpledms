from http import HTTPStatus
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Count
from django.urls import reverse

from .models import Document, Tag
from .forms import DocumentForm, TagForm

import pdf2image
import dateparser.search

# Create your views here.
def index(request):
    count = {'UT': 0, 'IN': 0, 'HF': 0, 'AR': 0}
    queryset = Document.objects.all().values('status').annotate(count=Count('status'))
    count.update({x['status']: x['count'] for x in queryset})

    print(count)

    return render(request, 'sdms/index.html', count)

def addtag(request):
    form = TagForm(request.POST)
    if form.is_valid():
        tag = Tag(**form.cleaned_data)
        tag.save()
        return JsonResponse({'tag_id': tag.id,
            'label': str(tag),
            'text_color': tag.text_color,
            'fill_color': tag.fill_color,
            'border_color': tag.border_color,
        })
    else:
        return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

def guess_date(text):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    dates = set(dt.date() for x, dt in dateparser.search.search_dates(text, ['de']))
    dates = [ x for x in dates if 1900 <= x.year and x <= tomorrow ]
    dates.sort()
    return dates[-5:]


def document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document.subject = form.cleaned_data['subject']
            document.document_date = form.cleaned_data['document_date']
            document.document_amount = form.cleaned_data['document_amount']
            document.status = form.cleaned_data['status']
            document.tags.clear()
            for tag in form.cleaned_data['tags']:
                document.tags.add(tag)
            document.save()
            print(form.cleaned_data)
            next_document_id = Document.objects.filter(status=Document.Status.INBOX).values_list('id').first()
            if next_document_id:
                return HttpResponseRedirect(reverse('document', args=(next_document_id[0],)))
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = DocumentForm(initial={
            'tags': list(document.tags.all().values_list("id", flat=True)),
            'subject': document.subject,
            'document_date': document.document_date,
            'document_amount': document.document_amount,
            })
    date_suggestions = guess_date(document.pdf_text + '\n\n' + document.ocr_text)
    tags = Tag.objects.all()
    tag_form = TagForm()
    page_range = range(1, 1+document.pages)
    return render(request, 'sdms/document.html', locals())

def page_image(dpi):
    def view(request, document_id, page):
        document = get_object_or_404(Document, id=document_id)
        image = pdf2image.convert_from_path(document.file.path, first_page=page, last_page=page, dpi=dpi)[0]
        response = HttpResponse()
        response.headers['Content-Type']="image/png"
        image.save(response, "PNG")
        return response
    return view
