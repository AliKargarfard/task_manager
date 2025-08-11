from django.core.files import File
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker
from apps.accounts.models import User
from apps.tasks.models import Task
from apps.core.models import Category
import random
from slugify import slugify

class Command(BaseCommand):
    help = 'Generate fake data with new fields (slug, URLs)'

    def handle(self, *args, **options):
        fake = Faker('fa_IR')  # برای داده‌های فارسی
        
        # مسیرهای نمونه برای تصاویر
        SAMPLE_IMAGES = [
            'sample_images/task1.jpg',
            'sample_images/task2.png',
            'sample_images/task3.jpg'
        ]
        
        SAMPLE_ICONS = [
            'sample_icons/cat1.svg',
            'sample_icons/cat2.png',
            'sample_icons/cat3.svg'
        ]

        # ایجاد پوشه‌های مورد نیاز
        os.makedirs('media/tasks/images', exist_ok=True)
        os.makedirs('media/categories/icons', exist_ok=True)

        # حذف داده‌های موجود (به جز سوپر یوزر)
        User.objects.exclude(is_superuser=True).delete()
        Task.objects.all().delete()
        Category.objects.all().delete()

        # ایجاد ۲ کاربر جدید با slug
        users = []
        for _ in range(2):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # ایجاد ۵ دسته‌بندی با slug
        categories = []
        colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3']
        for i in range(5):
            name = fake.word()
            cat = Category.objects.create(
                name=name,
                slug=slugify(name),
                color=colors[i],
                owner=random.choice(users)
            )
            # افزودن آیکون تصادفی
            icon_path = os.path.join(settings.BASE_DIR, random.choice(SAMPLE_ICONS))
            if os.path.exists(icon_path):
                cat.icon.save(
                    os.path.basename(icon_path),
                    File(open(icon_path, 'rb'))
                    )
            categories.append(cat)
            self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name} (slug: {cat.slug})'))

        # ایجاد ۱۰ تسک با slug و URLها
        statuses = [True, False]
        priorities = ['H', 'M', 'L']
        for i in range(10):
            title = fake.sentence(nb_words=4)
            # slug = slugify(title)[:200]  # اطمینان از عدم خالی بودن
            # if not slug:  # اگر slug خالی شد
            #     slug = f"task-{fake.random_number(digits=4)}"
            task = Task.objects.create(
                title=title,
                slug = slugify(
                            title,
                            max_length=200,
                            allow_unicode=True,
                            word_boundary=True
                        ),
                description=fake.paragraph(nb_sentences=3),
                is_completed=random.choice(statuses),
                owner=random.choice(users),
                priority=random.choice(priorities),
                deadline=fake.future_date() if i % 3 == 0 else None
            )
            # افزودن تصویر تصادفی
            img_path = os.path.join(settings.BASE_DIR, random.choice(SAMPLE_IMAGES))
            if os.path.exists(img_path):
                task.image.save(
                    os.path.basename(img_path),
                    File(open(img_path, 'rb')))
            # اختصاص دسته‌بندی‌های تصادفی
            task.categories.set(random.sample(categories, k=random.randint(1, 3)))
            
            # نمایش URLهای تولید شده
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created task: {task.title}\n'
                    f'- Absolute URL: {task.get_absolute_url()}\n'
                    f'- Relative URL: {task.get_relative_url()}\n'
                    f'- API URL: /api/tasks/{task.slug}/'
                )
            )

        self.stdout.write(self.style.SUCCESS('\nSuccessfully generated new fake data with slugs and URLs!'))