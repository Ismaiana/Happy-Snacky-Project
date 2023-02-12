"""Server for happy snacky app"""


from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import os
import crud
import requests
import random
import json

from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = os.environ["secret_key"]
app.Spoonacular_KEY = os.environ["Spoonacular_KEY"]
app.Host_KEY = os.environ["Host_KEY"]
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

  
        
    if 'user_email' in session:

        
        email = session['user_email']
 
        crud.get_user_by_email(email)

        products = request.form.get('product')

        restriction_filters = request.form.getlist('restrictions-search')

        print(restriction_filters)
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/search"

        parameters = {
            "query": products,
            "addProductInformation": 'true'
            
            }

        headers = {
            "X-RapidAPI-Key": app.Spoonacular_KEY,
            "X-RapidAPI-Host": app.Host_KEY
        }

        response = requests.request("GET", url, headers=headers, params=parameters)

      
        response.raise_for_status()

        data = response.json()


        product_data = data['products']
        
        filtered_product_data = []
        # ????????
        for product_index in range(len(product_data)):
            if(set(restriction_filters).issubset(set(product_data[product_index]['importantBadges']))):
                filtered_product_data.append(product_data[product_index])

        if filtered_product_data == []:
            flash('Your search parameters had no match results.')

        data['products'] = filtered_product_data

        return render_template('search.html', data=data, id=id)


    else:

        flash('Login required to use search feature.')

        return redirect('/')


@app.route('/info/<id>')
def snack_info(id):
    """Display info of searched snacks"""


    parameters2 = {
    "id": id,
    
    }

    
    headers = {
        "X-RapidAPI-Key": app.Spoonacular_KEY,
        "X-RapidAPI-Host": app.Host_KEY
    }

    response = requests.get(f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/{id}", params=parameters2, headers=headers)

    data2 = response.json()
    
    return render_template('info.html', data=data2, id=id)


@app.route('/nutrition-info/<id>')
def data_json(id):
    """Display info of searched snacks"""


    parameters2 = {
    "id": id,
    
    }

    
    headers = {
        "X-RapidAPI-Key": app.Spoonacular_KEY,
        "X-RapidAPI-Host": app.Host_KEY
    }

    response = requests.get(f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/{id}", params=parameters2, headers=headers)

    nutrition = response.json()
    
    return jsonify({'data': nutrition})


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


@app.route('/random', methods=['GET', 'POST'])
def random_snack():
    """Generate random snack via button and ingredients filter"""


    filters= request.form.getlist('restrictions2')
    print(filters)

    parameters = {
    'apiKey': app.Spoonacular_KEY,
    'query': filters
    }

    headers = {
     "X-RapidAPI-Key": app.Spoonacular_KEY,
     "X-RapidAPI-Host": app.Host_KEY
    }

    response = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/search', params=parameters, headers=headers)

    response.raise_for_status()

    data3 = response.json()

    random_snack = random.choices(data3['products'])
    random_snack = random_snack[0]
 

    return render_template('homepage.html', data=random_snack)

   

@app.route('/addrestrictions', methods=['GET','POST'])
def add_restrictions():
    """Allow user to add dietary restrictions"""

   
    email= session['user_email']
    user = crud.get_user_by_email(email)
   
        
    if request.method == 'POST':
        dietary_restrictions = request.form.getlist('restrictions')
        for dietary_restriction in dietary_restrictions:
            get_restriction = crud.get_restrictions(user.user_id, dietary_restriction)
            if get_restriction == []:
                restrictions = crud.create_restrictions(user.user_id, dietary_restriction)
                db.session.add(restrictions)
                db.session.commit()
        return redirect('/profile')
  

    return render_template('/addrestrictions.html')


@app.route('/restrictions')
def restrictions():
    """Jsonified data base restrictions"""

    email = session['user_email']
 
    user = crud.get_user_by_email(email)
        
    restriction = crud.get_restrictiondb(user.user_id)


    restriction_data = []
    for r in restriction:

        d = {'dietary restriction': r.dietary_restriction}

        restriction_data.append(d['dietary restriction'])

    
    return jsonify(restriction_data)

@app.route('/removerestrictions', methods=['POST'])
def remove_restriction():
    """remove restriction from data base and user profile"""

    email = session['user_email']
 
    user = crud.get_user_by_email(email)


   
    checked_restriction= request.form.getlist('remove-restrictions')
  
    for restriction in checked_restriction:

        remove_restriction= crud.get_restriction(user.user_id, restriction)
        db.session.delete(remove_restriction)
        db.session.commit()


    return redirect('/profile')
   



@app.route('/profile')
def user_profile():
    """Show user profile"""


    if 'user_email' in session:

        email = session['user_email']
 
        user = crud.get_user_by_email(email)
        
        restriction = crud.get_restrictiondb(user.user_id)
    
        
        return render_template('profile.html', email= user.email, fname= user.fname, lname= user.lname, restriction=restriction)

    else:


        return redirect('/')


@app.route('/savedsnacks')
def show_snacks():
    """display saved snacks"""

    email= session['user_email']
    user = crud.get_user_by_email(email)
    saved_snacks = crud.get_safesnacks(user.user_id)
    not_safe = crud.get_notsafesnacks(user.user_id)
    

    return render_template('savedsnacks.html', saved_snacks=saved_snacks, not_safe=not_safe)


@app.route('/safesnacks', methods=['GET','POST'])
def saved_snacks():
    """Save snacks process for save for later snacks button"""

    email = session['user_email']
    user = crud.get_user_by_email(email)


   
    title = request.form.get('title')
    image = request.form.get('image')
    save = crud.create_savedsafe(user.user_id, title, image)
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
    

@app.route('/remove_safesnacks', methods=['POST'])
def remove_not_safe():
    """Delete saved snack from safe list and db"""

    email = session['user_email']
 
    user = crud.get_user_by_email(email)


   
    safe_snacks= request.form.getlist('safe-delete')
  
    for snack in  safe_snacks:

        remove_snack= crud.get_safesnack(user.user_id)
        db.session.delete(remove_snack)
        db.session.commit()


    return redirect('/savedsnacks')


@app.route('/remove_notsafesnacks', methods=['POST'])
def remove_safe():
    """Delete saved snack from not safe list and db"""

    email = session['user_email']
 
    user = crud.get_user_by_email(email)


   
    notsafe_snacks = request.form.getlist('not-safe-delete')
  
    for snack in notsafe_snacks:

        remove_snack = crud.get_notsafesnack(user.user_id)
        db.session.delete(remove_snack)
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


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)