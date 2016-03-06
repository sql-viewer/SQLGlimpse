from sqlviewer.glimpse.services import save_imported_model
from sqlviewer.integration.mysqlwb import import_model

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'

import os

import time
from threading import Thread  # This is the right package name
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports the specified file into the database'

    def add_arguments(self, parser):
        parser.add_argument('model_path', type=str, help='path to model to import')
        parser.add_argument('name', type=str, help='name of the model')
        parser.add_argument('version', type=str, help='version of the model')

    def handle(self, *args, **options):
        path = str(options['model_path'])
        filename, file_extension = os.path.splitext(path)
        supported_extensions = ['.mwb']
        if os.path.exists(path):
            if file_extension in supported_extensions:
                start = time.perf_counter()
                self.stdout.write(self.style.SUCCESS('Starting import of model at "%s"' % path))
                model = import_model(path, options['name'], options['version'])

                status_thread = ConsoleAnimationThread()
                status_thread.start()
                save_imported_model(model['model'])
                status_thread.stop()
                message = 'Successfully imported  model from "%s" in %d ms' % (path, (time.perf_counter() - start) * 1000)
                self.stdout.write(self.style.SUCCESS(message))
            else:
                raise CommandError('Only files of type %s are supported' % ",".join(supported_extensions))
        else:
            raise CommandError('File does not exist at path %s' % path)


class ConsoleAnimationThread(Thread):
    def __init__(self):
        self.syms = ['\\', '|', '/', '-']
        self.iterations = 0
        self.stopped = False
        Thread.__init__(self)

    def run(self):
        while not self.stopped:
            cidx = self.iterations % len(self.syms)
            print('Importing model %s' % (self.syms[cidx]), end='\r')
            time.sleep(0.5)
            self.iterations += 1

    def stop(self):
        self.stopped = True
