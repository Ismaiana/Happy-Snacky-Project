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
    
    badingredients = db.relationship('Badingredient', back_populates='user')
    savedsafe = db.relationship('Savedsafe', back_populates='user')
    savednotsafe = db.relationship('Savednotsafe', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Badingredient(db.Model):

    __tablename__ = 'bad_ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ingredient = db.Column(db.String)
    
    user = db.relationship('User', back_populates='badingredients')

    def __repr__(self): 
        return f'<Badingredient ingredient_id={self.ingredient_id} ingredient={self.ingredient}>'


class Savedsafe(db.Model):

    __tablename__ = 'safe_snacks'

    snack_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    snack_name = db.Column(db.String, nullable=False)
    snack_brand = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    
    user = db.relationship('User', back_populates='savedsafe')

    def __repr__(self): 
        return f'<Savedsafe snack_id={self.snack_id} snack_name={self.snack_name}>'


class Savednotsafe(db.Model):
    
    __tablename__ = 'notsafe_snacks'

    nsnack_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    snack_name = db.Column(db.String, nullable=False)
    snack_brand = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    bad_ingredients= db.Column(db.String)

    user = db.relationship('User', back_populates='savednotsafe')

    def __repr__(self): 
        return f'<Savednotsafe nsnack_id={self.nsnack_id} snack_name={self.snack_name}>'




def connect_to_db(flask_app, db_uri="postgresql:///snacks", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    db.create_all()