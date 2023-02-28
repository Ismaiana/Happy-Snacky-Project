# Happy Snacky 🥚

Happy Snacky is a web application that helps users discover new products based on their allergies and dietary restrictions.
With over 800,000 products in its database, Happy Snacky provides a comprehensive selection of grocery products options for users with diverse dietary needs.
The app also features a login page, new user page, reset password with email and tokens for security, profile, forum, search bar, saved page, and filters for a 
more personalized user experience.


## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [License](#license)
* [About Me](#aboutme)



## <a name="technologies"></a>Technologies


Backend: Python, Flask, PostgreSQL, SQLAlchemy.

Frontend: JavaScript, AJAX, Jinja2, HTML5, CSS, Bootstrap.

APIs: Spoonacular, SendGrid.

Authentication and Security: Python secrets module, Passlib.



## <a name="features"></a>Features


Login Page: Users can create an account or log in using their email and password. 
The login page also includes options for resetting passwords with email and tokens for added security.
New users can sign up for Happy Snacky by providing their name, email, and password.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/login-page.JPG "login page")


![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/password-reset.JPG "password reset")


Profile Page: The user profile page allows users to add and edit their dietary restrictions, and change avatars. This information is used to display 
if product is safe or not for the user.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/profile-page.JPG "profile page")

Search Bar: Happy Snacky includes a search bar that allows users to search for specific products or filter products based on specific dietary needs or allergies.
It contains filters that allow users to narrow down the product selection based on their specific dietary needs, such as gluten-free, vegan, kosher
and manny others options.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/search-bar.JPG "search bar")

Product Information: Each product in Happy Snacky's database includes a product title, brand, picture, ingredients, and nutritional information. 
Additionally, there is a message displayed that indicates whether the product is safe for the user to consume, or if it requires the user's attention due
to certain ingredients that they need to avoid.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/info-page.png "product information")

Saved Page: Users can save their favorite products to a saved page for easy access in the future.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/saved-page.JPG "saved page")

Forum: The forum feature allows users to share information and ask questions related to dietary restrictions and allergies. 
Users can create new posts and comment on existing posts.

![alt text](https://github.com/Ismaiana/Happy-Snacky-Project/blob/main/static/img/forums.JPG "forum")


## <a name="install"></a>Installation

To install Happy Snacky: 

Clone or fork this repo:

```
https://github.com/Ismaiana/Happy-Snacky-Project
```

Create and activate a virtual environment inside Happy Snacky directory.

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use [Spoonacular Api](https://spoonacular.com/food-api) and [Sendgrid Api](https://sendgrid.com/).
Copy your api key and save it in a file called secret.sh(using this format).

Source your keys from your secrets.sh file into your virtual environment:
```
source secret.sh
```

Set up the database:

```
createdb happysnacky
python3 model.py
python3 crud.py
```

Run the app:

```
python3 server.py
```


## <a name="license"></a>License

Happy Snacky License (Version 1.0)

Copyright (c) 2023 Ismaiana Lima

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use, copy, modify, and distribute the Software and any modified versions of the Software, provided that the following conditions are met:

1. The above copyright notice and this license notice shall be included in all copies or substantial portions of the Software.

2. The Software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.

3. Any product or service derived from this software or containing parts of this software must give appropriate credit to the original author of the software.

4. The Software may not be used for any illegal or unethical purposes.

By using the Software, you agree to be bound by the terms of this license. If you do not agree to the terms of this license, do not use the Software.


## <a name="aboutme"></a>About Me

Ismaiana is a software engineer originally from Brazil, and currently living in AZ. This is her first full stack project. 
Visit her on [LinkedIn](http://www.linkedin.com/in/ismaiana-lima).
