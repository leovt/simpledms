import logging
import time

from django.core.management.base import BaseCommand, CommandError
from sdms.models import Document

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        while True:
            try:
                document = Document.objects.filter(status=Document.Status.UNTREATED).first()
                if document is not None:
                    try:
                        self.stdout.write(f'Preparing {document}...')
                        document.status = Document.Status.ERROR
                        document.save()
                        document.prepare()
                        self.stdout.write(f'Preparing {document} ... DONE.')
                    except Exception:
                        self.stdout.write(f'Preparing {document} ... FAIL.')
                        raise
                else:
                    time.sleep(10)
            except Exception:
                logging.exception('Error in preparedocs.Command.handle')
