import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

# --- IMPORTANT: Update these import paths to match your app names ---
# Format: from <app_name>.models import <ModelName>
from user.models import Users
from resources.models import Resource
from event.models import Events
from registration.models import Registration

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Generates 50 students and related college data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Cleaning old data..."))
        Registration.objects.all().delete()
        Events.objects.all().delete()
        Resource.objects.all().delete()

        depts = ['MCA', 'BCA', 'BSc CS', 'MSc DS']


        faculty_list = []
        for i in range(5):
            f = User.objects.create_user(
                username=f"faculty_{i}_{fake.last_name().lower()}",
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role="Faculty",
                department=random.choice(depts)
            )
            faculty_list.append(f)

        # 2. Create EXACTLY 50 Student Instances
        self.stdout.write("Creating 50 Students...")
        student_list = []
        for i in range(50):
            s = User.objects.create_user(
                username=f"student_{i}_{fake.last_name().lower()}",
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role="Student",
                department=random.choice(depts)
            )
            student_list.append(s)

        # 3. Create Resources
        self.stdout.write("Creating Resources...")
        res_cats = ['Notes', 'Assignment', 'Syllabus', 'Previous_paper', 'Reference']
        for _ in range(20):
            Resource.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(),
                subject=fake.word().capitalize(),
                category=random.choice(res_cats),
                department=random.choice(depts),
                uploaded_by=random.choice(faculty_list),
                download_count=random.randint(0, 50)
            )

        # 4. Create Events
        self.stdout.write("Creating Events...")
        event_types = ['Seminar', 'Workshop', 'Placement', 'Cultural', 'Sports']
        event_status = ['Upcoming', 'Ongoing', 'Complete']
        events = []
        for i in range(10):
            e = Events.objects.create(
                title=f"{random.choice(event_types)} on {fake.word().capitalize()}",
                description=fake.text(),
                status=random.choice(event_status),
                type=random.choice(event_types),
                date=fake.future_datetime(end_date="+30d", tzinfo=timezone.get_current_timezone()),
                venue=f"Hall {random.randint(1, 10)}",
                capacity=random.randint(30, 60),
                department=random.choice(depts),
                created_by=random.choice(faculty_list)
            )
            events.append(e)

        # 5. Create Event Registrations
        self.stdout.write("Linking Students to Events...")
        for student in student_list:
            # Each student registers for 2 random events
            selected_events = random.sample(events, 2)
            for ev in selected_events:
                Registration.objects.get_or_create(
                    student=student,
                    event=ev,
                    defaults={'attended': random.choice([True, False])}
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully generated 50 students and associated records!"))