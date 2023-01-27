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

    
    id = int(data['products'][0]['id'])

    return render_template('search.html', data=data, id=id)




@app.route('/info')
def snack_info():

    return render_template('info.html', id=None)


@app.route('/info')
def display_snacks():
    
    headers = {
    "Content-Type": "application/json"
    
    }

    id =  request.form.get("id")
    parameters2 = {
    "id": id,
    "apiKey": app.Spoonacular_KEY 

    }

    response = requests.get(f"https://api.spoonacular.com/food/products/{id}", params=parameters2, headers = headers)

    data2 = response.json()

    
    # print(data3["id"], data3["title"], data3["ingredientList"], data3["ingredients"])

    return render_template('info.html', data=data2, id=id)


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