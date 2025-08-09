from django.core.management.base import BaseCommand
from faker import Faker
from apps.accounts.models import User
from apps.tasks.models import Task
from apps.core.models import Category
import random

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **options):
        fake = Faker('fa_IR')  # برای داده‌های فارسی
        
        # حذف داده‌های موجود
        User.objects.exclude(is_superuser=True).delete()
        Task.objects.all().delete()
        Category.objects.all().delete()

        # ایجاد ۲ کاربر
        users = []
        for _ in range(2):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # ایجاد ۵ دسته‌بندی
        categories = []
        colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3']
        for i in range(5):
            cat = Category.objects.create(
                name=fake.word(),
                color=colors[i],
                owner=random.choice(users))
            categories.append(cat)
            self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        # ایجاد ۱۰ تسک
        statuses = [True, False]
        for _ in range(10):
            Task.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=3),
                is_completed=random.choice(statuses),
                owner=random.choice(users),
                priority=random.choice(['H', 'M', 'L']),
            ).categories.set(random.sample(categories, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data!'))