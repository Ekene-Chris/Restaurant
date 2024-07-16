from django.core.management.base import BaseCommand
from RestaurantAPI.models import Category, MenuItem
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create categories
        categories = [
            'Appetizers',
            'Main Courses',
            'Desserts',
            'Beverages',
            'Sides'
        ]

        for cat in categories:
            Category.objects.get_or_create(title=cat, slug=cat.lower().replace(' ', '-'))

        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        # Create menu items
        menu_items = [
            ('Garlic Bread', 'Appetizers', 5.99),
            ('Caesar Salad', 'Appetizers', 8.99),
            ('Grilled Salmon', 'Main Courses', 18.99),
            ('Beef Steak', 'Main Courses', 22.99),
            ('Chocolate Cake', 'Desserts', 6.99),
            ('Ice Cream Sundae', 'Desserts', 5.99),
            ('Coca Cola', 'Beverages', 2.99),
            ('Iced Tea', 'Beverages', 2.50),
            ('French Fries', 'Sides', 3.99),
            ('Onion Rings', 'Sides', 4.99),
        ]

        for title, category, price in menu_items:
            category_obj = Category.objects.get(title=category)
            MenuItem.objects.get_or_create(
                title=title,
                price=price,
                category=category_obj,
                featured=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(menu_items)} menu items'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))