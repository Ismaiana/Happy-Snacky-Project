"""Crud functions"""

from model import db, User, Badingredient, Savedsafe, Savednotsafe, connect_to_db


def create_user(email, password, fname, lname):

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user


def create_restrictions(user, dietary_restriction):
    
    restrictions= Badingredient(user_id=user, dietary_restriction=dietary_restriction)

    return restrictions


def get_restrictions(user, dietary_restriction): 
   

    return Badingredient.query.filter_by(user_id= user, dietary_restriction= dietary_restriction).all()


def get_restrictiondb(user):

    return Badingredient.query.filter_by(user_id=user).all()


def get_restriction(user, dietary_restriction):

    return Badingredient.query.filter_by(user_id= user, dietary_restriction= dietary_restriction).first()


def create_savedsafe(user, title, image):

    safe_snacks= Savedsafe(user_id=user, title=title, image=image)

    return safe_snacks


def get_safesnacks(user):

    return Savedsafe.query.filter_by(user_id=user).all()

def get_safesnack(user):

    return Savedsafe.query.filter_by(user_id=user).first()


def create_savednotsafe(user, title, image, ingredients):

    notsafe_snacks= Savednotsafe(user_id=user, title=title, image=image, ingredients=ingredients)

    return notsafe_snacks


def get_notsafesnacks(user):

    return Savednotsafe.query.filter_by(user_id=user).all()


def get_notsafesnack(user):

    return Savednotsafe.query.filter_by(user_id=user).first()


def get_users():
    

    return User.query.all()


def get_user_by_id(user_id):
    

    return User.query.get(user_id)


def get_user_by_email(email):
   

    return User.query.filter(User.email == email).first()
    



if __name__ == '__main__':
    from server import app

    connect_to_db(app)