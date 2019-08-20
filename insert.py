from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#create engine
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine

#create session
DBSession = sessionmaker(bind=engine)
session=DBSession()

#add to session && commit
# myFirstRestaurant=Restaurant(name="Really Belly")
# session.add(myFirstRestaurant)
# session.commit()

#query
# session.query(Restaurant).all()


frenchfries=MenuItem(name="French Fries", restaurant = session.query(Restaurant).filter_by(name="Loving it").one())
icedtea=MenuItem(name="Iced Tea", restaurant = session.query(Restaurant).filter_by(name="Pizza Palace").one())

# session.add(icedtea)
session.commit()

# session.query(MenuItem).all()