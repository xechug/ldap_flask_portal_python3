# The code above is a function that will create a new database and populate it with the tables and
# data from the `app/home/models.py` file.

from app import db
from app.home.models import User, Permission, UserPermission, Notification
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect


#This function queries the database for all notifications and orders them by the datetime_start
#   column.
#    :return: A list of notifications ordered by datetime_start


def view_notifications():
    notifications = db.session.query(Notification).order_by(Notification.datatime_start.desc()).all()
    return notifications




def save_user_db(user):

 # Create a user in the database if they don't exist, and return the user id.
    db.create_all()
    # This is a query to the database to see if the user is in the database.
    check_user = User.query.filter_by(userdn=user).first()
     # Create a user in the database if they don't exist.
    if check_user is None:
       # Creating a user object and assigning the userdn attribute to the user object.
        user_add = User(userdn=user)
       # The code above is adding a new user to our database. We are using the ORM (Object Relational
       # Mapping) provided by SQLAlchemy to do so.
        db.session.add(user_add)
    db.session.flush()
    db.session.commit()
    # This is a query to the database to see if the user is in the database.
    check_user = User.query.filter_by(userdn=user).first()
    # The above code is a function that takes in a user and returns the user's id.
    return check_user.id


def save_all_permissions(allowed):
# 1. Create a list of all the apps that we want to add to the database.
#     2. Create a list of all the permissions that we want to add to the database.
#     3. Create a for loop that iterates through the list of apps and adds each app to the database.
#     4. Create a for loop that iterates through the list of permissions and adds each permission to
# the database.
    for x in allowed:
        insert = Permission(app=x)
        db.session.add(insert)
    db.session.commit()


def relationship_permissions(userid, allowed):
    allpermission = Permission.query.all()
    UserPermission.query.filter_by(user_id=userid).delete()
    for i in allpermission:
        for x in allowed:
            if x in i.app:
                # print(i.app+ ' coincide con '+x)
                insert = UserPermission(user_id=userid, permission_id=i.id)
                db.session.add(insert)
    db.session.commit()


def only_allow(userid):

        sql = text('SELECT DISTINCT * FROM APP_ALLOW_USER WHERE USER_ID = '+str(userid))

        result = db.engine.execute(sql)

        return result

# def search_db_dn (user):
