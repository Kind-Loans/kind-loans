from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker
from datetime import timedelta

from core import models


# TODO:
# + fake data for transaction
class Command(BaseCommand):
    help = "Generate fake data for User, LoanProfile, and Transaction Model."

    def handle(self, *args, **kwargs):
        fake = Faker()

        LENDER_COUNT = 2
        BORROWER_COUNT = 5
        LOAN_PERIOD = timedelta(days=500)

        # fake-lenders
        for _ in range(LENDER_COUNT):
            name = fake.name()
            first, last = list(map(str.lower, name.split()))

            user = get_user_model().objects.create_user(
                name=name,
                email=f"{first}.{last}@example.com",
                password=fake.name(),
                role=models.UserRole.LENDER,
            )

        self.stdout.write(self.style.SUCCESS(f"{LENDER_COUNT} lender(s) created."))

        # fake-borrowers & loan-profiles
        for _ in range(BORROWER_COUNT):
            name = fake.name()
            first, last = list(map(str.lower, name.split()))

            user = get_user_model().objects.create_user(
                name=name,
                email=f"{first}.{last}@example.com",
                password=fake.name(),
            ) 
            loan_profile = models.LoanProfile.objects.create(
                user=user,
                photoURL=fake.image_url(width=640, height=480),
                title=fake.company(),
                description=fake.paragraph(nb_sentences=4),
                business_type="",
                loan_duration_months=fake.random_number(digits=2),
                total_amount_required=fake.pydecimal(
                    left_digits=4,
                    right_digits=2,
                    positive=True
                ),
                deadline_to_receive_loan=fake.date_between(
                    start_date="today",
                    end_date=LOAN_PERIOD
                ),
            )

        self.stdout.write(self.style.SUCCESS(f"{BORROWER_COUNT} borrower(s) with loan profiles created."))

        self.stdout.write(self.style.SUCCESS("Successfully generated samples."))


