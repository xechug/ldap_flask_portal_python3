import datetime
from lib2to3.pytree import Base
from sqlalchemy import Boolean, Column, ForeignKey, Table
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app import db

db.metadata.clear()

class User(db.Model):
	"""users ldap sync"""
	__tablename__ = 'app_user'
	id = Column(Integer, primary_key=True)
	userdn = Column(String(100),unique=True)
	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Permission(db.Model):
	"""users ldap sync"""
	__tablename__ = 'app_permission'
	id = Column(Integer, primary_key=True)
	app = Column(String(100), unique=True)
	alias = Column(String(100))
	active = Column(Boolean, default=True)
	url = Column(String(100))
	maintenance = Column(Boolean)
	external_app = Column(Boolean)
	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class UserPermission(db.Model):
	__tablename__ = 'app_userpermission'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('app_user.id'))
	permission_id = Column(Integer, ForeignKey('app_permission.id'))
	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Notification(db.Model):
	__tablename__ = 'app_notificacions'
	id = Column(Integer, primary_key=True)
	author = Column(String(100))
	datatime_start = Column(DateTime)
	datatime_end = Column(DateTime)
	type = Column(String(100))
	message = Column(String(250))
	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


