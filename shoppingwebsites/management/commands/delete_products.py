from django.core.management.base import BaseCommand
from shoppingwebsites.models import Products

class Command(BaseCommand):
    help = 'Deletes all products from the database'

    def handle(self, *args, **options):
        # delete all the product imformation.
        Products.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all products'))
