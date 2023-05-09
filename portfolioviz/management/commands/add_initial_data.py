from django.core.management.base import BaseCommand
from portfolioviz.models import Portfolio
from portfolioviz.services import DataExtractor, EntityLoader


class Command(BaseCommand):
    help = 'Adds initial data to the database'
    
    def __init__(self) -> None:
        super().__init__()
        self.data_extractor = DataExtractor()
        self.entity_loader = EntityLoader()
    
    def dataExists(self):
        return Portfolio.objects.exists()
    
    def handle(self, *args, **options):
        if not self.dataExists():
            extracted_data = self.data_extractor.extract_data()
            
            self.entity_loader.populate_db(extracted_data)
        else:
            self.stdout.write('Initial data already exists')