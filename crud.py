"""Crud functions"""

from model import db, User, Badingredient, Savedsafe, Savednotsafe, connect_to_db


def create_user(email, password, fname, lname):

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user


def create__badingredient(user, ingredient):

    badingredients = Badingredient(user_id=user, ingredient=ingredient)

    return badingredients

    
def create_savedsafe(user, snack_name, snack_brand, image):

    savedsafe= Savedsafe(user_id=user,snack_brand=snack_brand, snack_name=snack_name, image=image)

    return savedsafe


def create_savednotsafe(user, snack_name, snack_brand, image, bad_ingredients):

    savednotsafe= Savednotsafe(user_id=user,snack_brand=snack_brand, snack_name=snack_name, image=image, bad_ingredients=bad_ingredients)

    return savednotsafe

def get_users():
    

    return User.query.all()

def get_user_by_id(user_id):
    

    return User.query.get(user_id)


def get_user_by_email(email):
   

    return User.query.filter(User.email == email).first()
    



if __name__ == '__main__':
    from server import app

    connect_to_db(app)