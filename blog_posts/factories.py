import factory
from django.contrib.auth.models import User
from faker import Faker

from . import models

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = User


class BlogPostFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=6)
    text = factory.LazyFunction(lambda: "\n\n".join(fake.texts(max_nb_chars=1000)))
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = models.BlogPost
