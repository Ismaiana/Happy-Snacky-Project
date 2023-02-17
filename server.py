"""Server for happy snacky app"""


from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
from passlib.hash import argon2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from model import connect_to_db, db
import secrets
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
app.SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
app.Host_KEY = os.environ["Host_KEY"]
connect_to_db(app)

reset_tokens = {}

@app.route('/')
def homepage():
    """display homepage with login form."""


    return render_template('homepage.html')


@app.route('/about')
def about():
    """display about page"""


    return render_template('about.html')


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

        url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/search'

        parameters = {
            'query': products,
            'addProductInformation': 'true',
            'number': '25'
            
            }

        headers = {
            'X-RapidAPI-Key': app.Spoonacular_KEY,
            'X-RapidAPI-Host': app.Host_KEY
        }

        response = requests.request('GET', url, headers=headers, params=parameters)

      
        response.raise_for_status()

        data = response.json()


        product_data = data['products']
        
        filtered_product_data = []
     
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

    exceptions = ['menu item type','non food item', 'snack', 'topping']

    parameters2 = {
    'id': id,
    
    }

    
    headers = {
        'X-RapidAPI-Key': app.Spoonacular_KEY,
        'X-RapidAPI-Host': app.Host_KEY
    }

    response = requests.get(f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/{id}', params=parameters2, headers=headers)
    

    product_info_data = response.json()
    
    
    cleaner_product_info_data = []
    
    for ingredient_index in range(len(product_info_data['ingredients'])):
        if product_info_data['ingredients'][ingredient_index]['name'] in exceptions:
           
            pass
        else:
            cleaner_product_info_data.append(product_info_data['ingredients'][ingredient_index])

    product_info_data['ingredients'] = cleaner_product_info_data

    return render_template('info.html', data=product_info_data, id=id)


@app.route('/nutrition-info/<id>')
def data_json(id):
    """Display info of searched snacks"""


    parameters2 = {
    'id': id,
    
    }

    
    headers = {
        'X-RapidAPI-Key': app.Spoonacular_KEY,
        'X-RapidAPI-Host': app.Host_KEY
    }

    response = requests.get(f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/{id}', params=parameters2, headers=headers)

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

    hashed = argon2.hash(password)
    print(password)
    print(hashed)

    if user:
        flash('This email adress is already being used.')

        return redirect('/register')

    else:
        user = crud.create_user(email, hashed, fname, lname)
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
    
   
    if not user or not argon2.verify(password, user.password):

        flash('The email or password you entered was incorrect.')

        return redirect('/')
        
    else:

        session['user_email'] = user.email
        flash(f'Welcome {user.fname}!')

        return redirect('/profile')
    

@app.route('/reset_password')
def reset_form():
    """Form reset password request"""



    return render_template('reset_password.html')


@app.route('/reset_password', methods=['POST'])
def reset_request():
    """Send email with password request"""

    email = request.form.get('email_db')
    print(email)
    user = crud.get_user_by_email(email)

    if not user:
        flash('Email did not match our records, try again')
        return redirect('/reset_password')

    else:
        
        token = secrets.token_urlsafe(32)
        
        reset_tokens[email] = token
        flash('Link to reset password sent to your email')
        message = Mail(
        from_email='no-reply_happysnacky@hotmail.com',
        to_emails= email,
        subject='Reset your Password',
        html_content=f'<strong>Hello,<br> We just received a request for a new password from your account. To reset your password, just click the link below.</strong> \
        <a href="{url_for("password_request_form", email=email, token=token, _external=True)}"><br>Reset Password</a>')
        try:
            sg = SendGridAPIClient(os.environ.get(app.SENDGRID_API_KEY))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return redirect('/')


@app.route('/process_request_password')
def password_request_form():
    """Display form for password change"""

    email = request.args.get('email')
    token = request.args.get('token')
  
    if email in reset_tokens and reset_tokens[email] == token:
        session['user_email'] = email
        return render_template('new_password.html')
    else:
        flash('Invalid or expired password reset link')
        return redirect('/')


@app.route('/process_request_password', methods=['POST'])
def new_password():
    email = session['user_email']
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    user = crud.get_user_by_email(email)

    hashed = argon2.hash(confirm_password)

    if new_password == confirm_password:
        new_password_db = crud.reset_password(user.user_id, hashed)
        db.session.add(new_password_db)
        db.session.commit()

       
        del reset_tokens[email]

    return redirect('/')


@app.route('/random', methods=['GET', 'POST'])
def random_snack():
    """Generate random snack via button and ingredients filter"""


    filters= request.form.getlist('restrictions2')

    parameters = {
    'apiKey': app.Spoonacular_KEY,
    'query': filters
    }

    headers = {
     'X-RapidAPI-Key': app.Spoonacular_KEY,
     'X-RapidAPI-Host': app.Host_KEY
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

   
    email = session['user_email']
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
    """Jsonified data from table restrictions"""

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


   
    checked_restriction = request.form.getlist('remove-restrictions')
  
    for restriction in checked_restriction:

        remove_restriction = crud.get_restriction(user.user_id, restriction)
        db.session.delete(remove_restriction)
        db.session.commit()


    return redirect('/profile')
   
@app.route('/forum')
def forum():
    """Display forum page"""

    return render_template('forum.html')

@app.route('/forum_rules')
def forum_rules():
    """Display forum rules"""

    return render_template('forum_rules.html')


@app.route('/discussions')
def discussions_forum():
    """Display discussions forum"""


    comments = crud.get_all_discussions()
   

    return render_template('discussions.html', comments=comments)


@app.route('/forum_comments_discussions')
def comment_discussions():
    """Create comments for forum discussions"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    comments = request.args.get('comment_dis')
                                
    comment = crud.create_comment_discussions(user.user_id, comments)
    db.session.add(comment)
    db.session.commit()


    return redirect('/discussions')


@app.route('/delete_comments_dis')
def delete_comments_dis():
    """Button to delete comment in forum discussions"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    delete_button = request.args.get('comment-delete')
    
    remove_comment = crud.get_comment_discussion(user.user_id, delete_button)

    db.session.delete(remove_comment)
    db.session.commit()

    return redirect('/discussions')


@app.route('/recommendations')
def recommendations_forum():
    """Display recommendations forum"""


    comments = crud.get_all_recommendations()
   

    return render_template('recommendations.html',comments=comments)


@app.route('/forum_comments_recommendations')
def comment_recommendations():
    """Create comments for forum recommendations"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    comments = request.args.get('comment_rec')

    comment = crud.create_comment_recommendations(user.user_id, comments)
    db.session.add(comment)
    db.session.commit()


    return redirect('/recommendations')


@app.route('/delete_comments_rec')
def delete_comments_rec():
    """Button to delete comment in forum recommendations"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    delete_button = request.args.get('comment-delete')
    
    remove_comment = crud.get_comment_recommendation(user.user_id, delete_button)

    db.session.delete(remove_comment)
    db.session.commit()

    return redirect('/recommendations')


@app.route('/reports')
def reports_forum():
    """Display reports forum"""

    

    comments = crud.get_all_reports()
   

    return render_template('reports.html', comments=comments)


@app.route('/forum_comments_reports')
def comment_reports_rec():
    """Create comments for forum reports"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    comments = request.args.get('comment_rep')
                                
    comment = crud.create_comment_reports(user.user_id, comments)
    db.session.add(comment)
    db.session.commit()


    return redirect('/reports')


@app.route('/delete_comments_rep')
def delete_comments_rep():
    """Button to delete comment in forum reports"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    delete_button = request.args.get('comment-delete')
    
    remove_comment = crud.get_comment_report(user.user_id, delete_button)


    db.session.delete(remove_comment)
    db.session.commit()

    return redirect('/reports')


@app.route('/avatars')
def show_avatars():
    """Allows user to select avatar"""


    return render_template('avatars.html')


@app.route('/avatars_db', methods=['GET', 'POST'])
def create_avatars():
    """Send selected avatar to db"""

    email = session['user_email']

    user = crud.get_user_by_email(email)
    

       
    selected_avatar = request.form.get('avatars')

    avatar = crud.get_avatardb(user.user_id)
    if avatar is None:

        added_avatar = crud.add_avatar(user.user_id, selected_avatar)

        db.session.add(added_avatar)
        db.session.commit()
    else: 
        upsert_row = crud.get_avatardb(user.user_id)
        upsert_row.avatar = selected_avatar
        
        db.session.commit()


    return redirect('/profile')
     

@app.route('/profile')
def user_profile():
    """Show user profile"""


    if 'user_email' in session:

        email = session['user_email']
 
        user = crud.get_user_by_email(email)
        
        restriction = crud.get_restrictiondb(user.user_id)

        avatar = crud.get_avatardb(user.user_id)
    
        
        return render_template('profile.html',email= user.email, fname= user.fname, lname= user.lname, restriction=restriction, avatar=avatar)

    else:


        return redirect('/')


@app.route('/savedsnacks')
def show_snacks():
    """Display saved snacks"""

    email= session['user_email']
    user = crud.get_user_by_email(email)
    saved_snacks = crud.get_safesnacks(user.user_id)
   
    

    return render_template('savedsnacks.html', saved_snacks=saved_snacks)


@app.route('/savesnacks', methods=['GET','POST'])
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
    
    

@app.route('/remove_safesnacks', methods=['POST'])
def remove_not_safe():
    """Delete saved snack from safe list and db"""

    email = session['user_email']
 
    user = crud.get_user_by_email(email)


   
    safe_snack = request.form.get('safe-delete')
  
 

    remove_snack = crud.get_safesnack(user.user_id, safe_snack)
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