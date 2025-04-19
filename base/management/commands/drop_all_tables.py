from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Drops all tables (be careful!)"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        self.stdout.write(self.style.SUCCESS("All tables dropped."))
