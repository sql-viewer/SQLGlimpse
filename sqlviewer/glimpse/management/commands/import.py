__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('model_path', type=str, help='path to model to import')

    def handle(self, *args, **options):
        path = str(options['model_path'])
        print(path)
