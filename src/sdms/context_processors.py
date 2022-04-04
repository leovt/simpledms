from django.db.models import Count

from .models import Document

def sdms_renderer(request):
    print('context_processor.sdms_renderer called')
    count = {'UT': 0, 'IN': 0, 'HF': 0, 'AR': 0}
    queryset = Document.objects.all().values('status').annotate(count=Count('status'))
    count.update({x['status']: x['count'] for x in queryset})

    return {
       'document_count': count,
    }
