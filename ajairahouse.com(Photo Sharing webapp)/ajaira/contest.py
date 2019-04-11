from models import db,Fighter
# Create all the tables


# create fighters
rahi= Fighter(name='Rahi')
sharuk = Fighter(name='Sharuk')

# add fighters to session
db.session.add(rahi)
db.session.add(sharuk)

# commit the fighters to database
db.session.commit()
