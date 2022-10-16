import random

from django.core.management import BaseCommand

from blog_posts.factories import BlogPostFactory, UserFactory


class Command(BaseCommand):
    """Populate the database with sample data"""

    def handle(self, *args, **options):
        users = tuple(UserFactory.create_batch(3))
        for _ in range(30):
            BlogPostFactory(author=random.choice(users))
