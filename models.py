# The LoginManager class is a
# class that provides the Flask-Login extension with the necessary hooks to
# authenticate users.
# 
# The UserMixin class is a class that provides the Flask-Login extension with
# the necessary hooks to store user data.
# 
# The User class is a class that provides the Flask-Login extension with the
# necessary hooks to store user data.
# 
# The get_id() method is a method that returns the user's unique identifier.
# 
# The __repr__() method is a method that returns a string representation of the
# user.

from flask_login import LoginManager, login_user, UserMixin, current_user

class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn
