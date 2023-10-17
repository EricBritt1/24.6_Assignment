from models import User, db, Feedback
from app import app

# Create all tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User.query.delete()

# Add Some Users
jake = User.register(username='kaiken832', password='atTheDragonFly78', email='jinjacool@ericmail.com', first_name='Jake', last_name='Sire')

sarah = User.register(username='cutegirl62', password='coolpqnguin92', email='sarahthecare@ericmail.com', first_name='Sarah', last_name='Supernova')

ice = User.register(username='despiteice92', password='beyondthekillgrade21', email='tryingurl2@ericmail.com', first_name='Ice', last_name='Spite')

# Add new objects to session, so they'll persist
db.session.add(jake)
db.session.add(sarah)
db.session.add(ice)

# Commit-otherwise, this never gets saved!
db.session.commit()

jake = User.query.get_or_404('kaiken832')
sarah = User.query.get_or_404('cutegirl62')
ice = User.query.get_or_404('despiteice92')

jake_feedback = Feedback(title="This app is great", content="So proud of the developers working on this app it's truly amazing!", username=jake.username)

sarah_feedback = Feedback(title="This app is alright!", content="Not the best but, will come back when developers actually start to care about their progress", username=sarah.username)

ice_feedback = Feedback(title="Leaving app", content="Absolutely DOG", username=ice.username)

db.session.add(jake_feedback)
db.session.add(sarah_feedback)
db.session.add(ice_feedback)

db.session.commit()

