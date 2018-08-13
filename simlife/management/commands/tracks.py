from demosys.management.base import BaseCommand
from ._trackconv import process_files


class Command(BaseCommand):
    help = "Convert track data from demosys to rocket"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tracks = process_files()
        tracks.save('simlife/resources/tracks.xml')
