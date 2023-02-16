"""Crud functions"""

from model import db, User, Badingredient, Savedsafe, Savednotsafe, ForumDiscussions, ForumRecommendations, ForumReports, Avatar, connect_to_db


def create_user(email, password, fname, lname):

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user


def add_avatar(user, avatar):

    avatar = Avatar(user_id=user, avatar=avatar)

    return avatar


def get_avatardb(user):

    return Avatar.query.filter_by(user_id=user).first()


def get_all_avatars():

    return Avatar.query.all()


def get_all_discussions():

    return ForumDiscussions.query.join(User).join(Avatar).all()


def create_comment_discussions(user, comments):

    discussions = ForumDiscussions(user_id=user, comments=comments)


    return discussions


def create_comment_recommendations(user, comments):

    recommendations = ForumRecommendations(user_id=user, comments=comments)


    return recommendations


def get_comments_recommendations(user):

    return ForumRecommendations.query.filter_by(user_id= user).all()


def get_all_recommendations():

    return ForumRecommendations.query.join(User).join(Avatar).all()


def create_comment_reports(user, comments):

    reports = ForumReports(user_id=user, comments=comments)


    return reports


def get_all_reports():

    return ForumReports.query.join(User).join(Avatar).all()


def create_comment_reports(user, comments):

    reports = ForumReports(user_id=user, comments=comments)


    return reports


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