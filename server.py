"""Server for happy snacky app"""


from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'ChaveSecretashh'
app.jinja_env.undefined = StrictUndefined

connect_to_db(app)
#API_KEY = os.environ['Spoonacular_KEY']

@app.route('/')
def homepage():
    """display homepage with login form."""

    return render_template('homepage.html')

# @app.route('products/search')
# def find_snack():
#     """Search snack in spoonacular"""

#     url =''
#     payload = {'apikey': API_KEY }

#     id=
#     name=
#     image=
    
# @app.route('product')
# def snack_information():
#     """Display snack ingredients"""



# @app.route('/savedsnacks')
# def show_snacks():
#     """display saved snacks"""



@app.route('/register')
def new_user():
    """Display form to create a new user"""



    return render_template('register.html')


@app.route('/register', methods=['POST'])
def user_registration():
    """Create a new user and add information to db"""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    user = crud.get_user_by_email(email)


    if user:
        flash('This email adress is already being used.')

        return redirect('/register')

    else:
        user = crud.create_user(email, password, fname, lname)
        db.session.add(user)
        db.session.commit()
        flash('Account created with sucess!')

        return redirect('/profile')

@app.route('/login', methods=['POST'])

def login_form():
    """Process user login"""

    
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
   

   
    if not user or user.password != password:

        flash('The email or password you entered was incorrect.')

        return redirect("/")
        
    else:

        session['email'] = user.email
        flash(f'Welcome back, {user.fname}!')

        return redirect('/profile')



@app.route('/profile')
def user_profile():
    """Show user profile"""

    return render_template('profile.html')

@app.route('/logout')
def process_logout():

    del session['email']
    flash('Logged out.')
    
    return redirect('/')

# @app.route('/preferences')
# def user_allergens():
#     """User choice for ingredients """




if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)