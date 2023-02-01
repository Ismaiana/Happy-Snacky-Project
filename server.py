"""Server for happy snacky app"""


from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import os
import crud
import requests
import json

from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = os.environ["secret_key"]
app.Spoonacular_KEY = os.environ["Spoonacular_KEY"]
connect_to_db(app)


@app.route('/')
def homepage():
    """display homepage with login form."""


    return render_template('homepage.html')


@app.route('/search')
def search_bar():
    """Display search bar"""


    return render_template('search.html', data=None)


@app.route('/search', methods=['POST'])
def find_snack():
    """Return user search"""

    products = request.form.get('product')

    parameters = {
    'apiKey': app.Spoonacular_KEY,
    'query': products
    }

    headers = {
    'Content-Type': 'application/json'
    }


    response = requests.get('https://api.spoonacular.com/food/products/search', params=parameters, headers=headers)

    response.raise_for_status()

    data = response.json()


    return render_template('search.html', data=data, id=id)


@app.route('/info/<id>')
def snack_info(id):
    """Display info of searched snacks"""
    
    headers = {
    "Content-Type": "application/json"
 
    }

    parameters2 = {
    "id": id,
    "apiKey": app.Spoonacular_KEY 

    }

    response = requests.get(f"https://api.spoonacular.com/food/products/{id}", params=parameters2, headers=headers)

    data2 = response.json()

    
    return render_template('info.html', data=data2)


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
        flash('Account created with sucess! Please log in to your account.')

        return redirect('/')


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

        session['user_email'] = user.email
        flash(f'Welcome {user.fname}!')

        return redirect('/profile')


@app.route('/addrestrictions', methods=['GET','POST'])
def add_restrictions():
    """Allow user to add dietary restrictions"""

   
    email= session['user_email']
    user = crud.get_user_by_email(email)
   
        
    if request.method == 'POST':
        dietary_restrictions = request.form.getlist('restrictions')
        for dietary_restriction in dietary_restrictions:
            get_restriction = crud.get_restriction(user.user_id, dietary_restriction)
            if get_restriction == []:
                restrictions = crud.create_restrictions(user.user_id, dietary_restriction)
                db.session.add(restrictions)
                db.session.commit()
        return redirect('/profile')
  

    return render_template('/addrestrictions.html')

@app.route('/profile')
def user_profile():
    """Show user profile"""

    if 'user_email' in session:

        email = session['user_email']

 
        user = crud.get_user_by_email(email)
      

        return render_template('profile.html', email= user.email, fname= user.fname, lname= user.lname)

    else:


        return redirect('/')


@app.route('/savedsnacks')
def show_snacks():
    """display saved snacks"""

    email= session['user_email']
    user = crud.get_user_by_email(email)
    saved_snacks = crud.get_safesnack(user.user_id)
    not_safe= crud.get_notsafesnack(user.user_id)
    



    return render_template('savedsnacks.html', saved_snacks=saved_snacks, not_safe=not_safe)


@app.route('/safesnacks', methods=['GET','POST'])
def saved_snacks():
    """Save snacks process for save for later snacks button"""

    email= session['user_email']
    user = crud.get_user_by_email(email)


   
    title= request.form.get('title')
    image= request.form.get('image')
    save= crud.create_savedsafe(user.user_id, title, image)
    db.session.add(save)
    db.session.commit()


    return redirect('/savedsnacks')
    
@app.route('/notsafesnacks', methods=['GET', 'POST'])
def not_safe():
    """Save snacks process for not safe snacks button"""

    email= session['user_email']
    user = crud.get_user_by_email(email)


   
    title= request.form.get('title')
    image= request.form.get('image')
    ingredients= request.form.get('ingredients')
    save_notsafe= crud.create_savednotsafe(user.user_id, title, image, ingredients)
    db.session.add(save_notsafe)
    db.session.commit()

    return redirect('/savedsnacks')
    

@app.route('/logout')
def process_logout():
    """Log out user in session"""

    request.form.get('logout')

    session['user_email']

    session.pop('user_email', None)
    flash('Logged out.')
    
    return redirect('/')

# @app.route('/settings')
# def user_settings():
#     """Display settings options"""




if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)