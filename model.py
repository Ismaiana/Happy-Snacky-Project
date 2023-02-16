"""Model for Happy Snacky app"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    
    
    restrictions = db.relationship('Badingredient', back_populates='user')
    savedsafe = db.relationship('Savedsafe', back_populates='user')
    savednotsafe = db.relationship('Savednotsafe', back_populates='user')
    forumdiscussions = db.relationship('ForumDiscussions', back_populates='user')
    forumrecommendations = db.relationship('ForumRecommendations', back_populates='user')
    forumreports = db.relationship('ForumReports', back_populates='user')
    avatars = db.relationship('Avatar', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} fname={self.fname}>'
    

class Avatar(db.Model):

    __tablename__ = 'avatars'

    avatar_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    avatar = db.Column(db.String)


    user = db.relationship('User', back_populates='avatars')

    def __repr__(self):
        return f'<Avatar avatar_id={self.avatar_id} avatar={self.avatar}>'


class Badingredient(db.Model):

    __tablename__ = 'restrictions'

    restriction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    dietary_restriction = db.Column(db.String, nullable=False)

    
    user = db.relationship('User', back_populates='restrictions')

    def __repr__(self): 
        return f'<Badingredient restriction_id={self.restriction_id} dietary_restriction={self.dietary_restriction}>'


class Savedsafe(db.Model):

    __tablename__ = 'safe_snacks'

    snack_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    
    user = db.relationship('User', back_populates='savedsafe')

    def __repr__(self): 
        return f'<Savedsafe snack_id={self.snack_id} title={self.title}>'


class Savednotsafe(db.Model):
    
    __tablename__ = 'notsafe_snacks'

    snack_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    ingredients= db.Column(db.String)

    user = db.relationship('User', back_populates='savednotsafe')

    def __repr__(self): 
        return f'<Savednotsafe nsnack_id={self.snack_id} title={self.title}>'

class ForumDiscussions(db.Model):
    
    __tablename__ = 'discussions'

    discussion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comments= db.Column(db.String(250))

    user = db.relationship('User', back_populates='forumdiscussions')


    def __repr__(self): 
        return f'<forumDiscussions discussion_id={self.discussion_id} comments{self.comments}>'


class ForumRecommendations(db.Model):

    __tablename__ = 'recommendations'

    discussion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comments = db.Column(db.String(250))

    user = db.relationship('User', back_populates='forumrecommendations')


    def __repr__(self): 
        return f'<forumRecommendations discussion_id={self.discussion_id} comments{self.comments}>'


class ForumReports(db.Model):

    __tablename__ = 'reports'

    discussion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comments= db.Column(db.String(250))

    user = db.relationship('User', back_populates='forumreports')


    def __repr__(self): 
        return f'<forumReport discussion_id={self.discussion_id} comments{self.comments}>'



def connect_to_db(flask_app, db_uri="postgresql:///snacks", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    app.app_context().push()
    db.create_all()