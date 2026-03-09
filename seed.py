import os
import django
import random
from datetime import date, timedelta

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_rental.settings')
django.setup()

# 2. Import models after django.setup()
from faker import Faker
from accounts.models import CustomUser
from advertisements.models import Advertisement
from rent_requests.models import RentRequest
from reviews.models import Review

fake = Faker()

def populate(n_users=5, n_ads=10):
    print(f"Cleaning database...")
    Review.objects.all().delete()
    RentRequest.objects.all().delete()
    Advertisement.objects.all().delete()
    # Be careful deleting users if you have a superuser you want to keep
    CustomUser.objects.filter(is_superuser=False).delete()

    print(f"Creating {n_users} users...")
    users = []
    for _ in range(n_users):
        user = CustomUser.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password="password123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='user',
            is_email_verified=True
        )
        users.append(user)

    print(f"Creating {n_ads} advertisements...")
    categories = ['studio', 'one_bedroom', 'two_bedroom', 'three_bedroom', 'four_plus']

    for _ in range(n_ads):
        owner = random.choice(users)
        cat = random.choice(categories)

        # Logic to make bedrooms match category
        bed_count = {'studio': 0, 'one_bedroom': 1, 'two_bedroom': 2, 'three_bedroom': 3, 'four_plus': 5}

        ad = Advertisement.objects.create(
            owner=owner,
            title=f"Beautiful {cat.replace('_', ' ')} in {fake.city()}",
            description=fake.paragraph(),
            category=cat,
            price=random.randint(1000, 10000),
            location=fake.address(),
            bedrooms=bed_count[cat],
            bathrooms=random.randint(1, 3),
            area_sqft=random.randint(500, 3500),
            amenities="AC, WiFi, Parking",
            status='approved'
        )

        # Create 1-2 Rent Requests for this ad
        potential_renters = [u for u in users if u != owner]
        renters = random.sample(potential_renters, k=random.randint(1, 2))

        for renter in renters:
            RentRequest.objects.create(
                advertisement=ad,
                requester=renter,
                message=f"Hi, I am interested in {ad.title}",
                move_in_date=date.today() + timedelta(days=random.randint(7, 30)),
                duration_months=random.randint(6, 12)
            )

            # Create a Review
            Review.objects.create(
                advertisement=ad,
                reviewer=renter,
                rating=random.randint(3, 5),
                title="Great place!",
                comment=fake.sentence()
            )

    print("Done! Database populated successfully.")

if __name__ == "__main__":
    populate()