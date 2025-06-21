from faker import Faker
import random
from app import app
from models import db, Guests, Episodes, Appearances

fake = Faker()

with app.app_context():
    print("🌱 Seeding database...")

    # Clear existing data
    Appearances.query.delete()
    Guests.query.delete()
    Episodes.query.delete()

    # Create Episodes
    episodes = []
    for i in range(1, 51):
        episode = Episodes(
            date=fake.date_between(start_date='-30y', end_date='today'),
            number=i
        )
        db.session.add(episode)
        episodes.append(episode)

    # Create Guests
    guests = []
    for _ in range(100):
        guest = Guests(
            name=fake.name(),
            occupation=fake.job()
        )
        db.session.add(guest)
        guests.append(guest)

    db.session.commit()

    # Create Appearances
    for _ in range(60):
        appearance = Appearances(
            rating=random.randint(1, 5),
            guest_id=random.choice(guests).id,
            episode_id=random.choice(episodes).id
        )
        db.session.add(appearance)

    db.session.commit()
    print("✅ Done seeding!")
