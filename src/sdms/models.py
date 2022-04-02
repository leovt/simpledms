import uuid
import colorsys

from django.db import models

import pdftotext
import pytesseract
import pdf2image

# Create your models here.
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    subtag = models.CharField(max_length=30, blank=True)
    fill_color = models.CharField(max_length=7, default="#AFD9F3")
    text_color = models.CharField(max_length=7, default="#233038")

    def __str__(self):
        if self.subtag:
            return f'{self.name}: {self.subtag}'
        return self.name

    @property
    def border_color(self):
        col = str(self.fill_color)
        rgb = [int(col[i:i+2], 16) / 255.0 for i in (1,3,5)]
        h,l,s = colorsys.rgb_to_hls(*rgb)
        r,g,b = colorsys.hls_to_rgb(h, max(0, l-0.2), s)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        UNTREATED = 'UT', 'Untreated'
        INBOX = 'IN', 'Inbox'
        HOLDFILE = 'HF', 'Hold File'
        ARCHIVE = 'AR', 'Archive'

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNTREATED)

    subject = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, related_name='documents', blank=True)
    document_date = models.DateField(null=True, blank=True)
    document_amount = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)

    pdf_text = models.TextField(blank=True, editable=False)
    ocr_text = models.TextField(blank=True, editable=False)
    pages = models.IntegerField(null=True, editable=False)

    def prepare(self):
        if self.status != Document.Status.UNTREATED:
            return

        with open(self.file.path, "rb") as f:
            pdf = pdftotext.PDF(f)
            self.pages = len(pdf)
            self.pdf_text = '\n\n'.join(pdf)

        images = pdf2image.convert_from_path(self.file.path, dpi=300)
        print(images)
        self.ocr_text = '\n\n'.join(pytesseract.image_to_string(image, 'deu') for image in images)

        self.status = Document.Status.INBOX
        self.save()
