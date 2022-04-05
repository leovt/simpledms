from http import HTTPStatus
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

import django_tables2 as tables
from django_sendfile import sendfile

from .models import Document, Tag
from .forms import DocumentForm, TagForm

import pdf2image
import dateparser.search

# Create your views here.
@login_required
def index(request):
    return render(request, 'sdms/index.html')

@login_required
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
    dates = dateparser.search.search_dates(text, ['de']) or []
    dates = set(dt.date() for x, dt in dates)
    dates = [ x for x in dates if 1900 <= x.year and x <= tomorrow ]
    dates.sort()
    return dates[-5:]


@login_required
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
    page_range = range(1, 1+(document.pages or 0))
    return render(request, 'sdms/document.html', locals())

def page_image(dpi):
    @login_required
    def view(request, document_id, page):
        document = get_object_or_404(Document, id=document_id)
        image = pdf2image.convert_from_path(document.file.path, first_page=page, last_page=page, dpi=dpi)[0]
        response = HttpResponse()
        response.headers['Content-Type']="image/png"
        image.save(response, "PNG")
        return response
    return view


from django.utils.html import format_html

class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<img src="{url}" height="50px" alt="Thumbnail for document id {value}"></img>',
            url=reverse('thumbnail', args=(value, 1)),
            value=value
        )

class DocumentTable(tables.Table):
    #id = tables.Column(linkify=True)
    id = ImageColumn(linkify=True)
    class Meta:
        model = Document
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "status", "subject", "file", "pages", "document_date", "document_amount", "tags")

class DocumentListView(LoginRequiredMixin, tables.SingleTableView):
    model = Document
    table_class = DocumentTable
    template_name = 'sdms/document_list.html'

class InboxListView(DocumentListView):
    def get_queryset(self):
        return super().get_queryset().filter(status="IN")

class HoldfileListView(DocumentListView):
    def get_queryset(self):
        return super().get_queryset().filter(status="HF")

class ArchiveListView(DocumentListView):
    def get_queryset(self):
        return super().get_queryset().filter(status="AR")

class SearchListView(DocumentListView):
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return super().get_queryset().filter(Q(pdf_text__icontains=query) | Q(ocr_text__icontains=query))

@login_required
def upload(request):
    if request.method == "POST":
        for file in request.FILES.getlist("documents"):
            doc = Document(file=file)
            doc.save()
            # TODO: prepare in background task in order to have faster response
            doc.prepare()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

@login_required
def media(request, path):
    return sendfile(request, settings.MEDIA_ROOT / path)
