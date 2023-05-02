from django.core.management.base import BaseCommand
from portfolioviz.models import Portfolio
from portfolioviz.services import DataExtractor, DataLoader


class Command(BaseCommand):
    help = 'Adds initial data to the database'
    
    def __init__(self) -> None:
        super().__init__()
        self.data_extractor = DataExtractor()
        self.data_loader = DataLoader()
    
    def dataExists(self):
        return Portfolio.objects.exists()
    
    def handle(self, *args, **options):
        if not self.dataExists():
            self.data_loader.load_data(
                self.data_extractor.extract_data())
        else:
            self.stdout.write('Initial data already exists')
