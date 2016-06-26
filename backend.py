# -*- coding: utf-8 -*-
from flask import Flask
import pymongo
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from flask_admin.model import BaseModelView
from wtforms import form, fields
from requests import get
import datetime
import json
import  wtforms.widgets.core
from parsing import parsing_coursera

#configuration
json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)
uri = "mongodb://webdevcourses:1234567890@ds019882.mlab.com:19882/web-dev-courses"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'i am gonna hash my strings up'

#connect to db
conn = pymongo.MongoClient(uri)
db = conn.get_default_database()

#Textarea widget
class TextArea(wtforms.widgets.core.TextArea):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, field, **kwargs):
        for arg in self.kwargs:
            if arg not in kwargs:
                kwargs[arg] = self.kwargs[arg]
        return super(TextArea, self).__call__(field, **kwargs)

#register forms 
class CoursesForm(form.Form):   
    card = fields.TextAreaField(widget=TextArea(rows='25', cols='50'), default='{\n\t"description": "", \n\t"language": "Eng", \n\t"level": 1, \n\t"vox": {\n\t\t"votes": 0,\n\t\t "favs": 0,\n\t\t"views": 0\n\t}, \n\t"image": "images/development-bg.png", \n\t"tags": ["javascript"], \n\t"free": true, \n\t"link": "#", \n\t"author": "Author not known", \n\t"submittedBy": "System", \n\t"date": "2016-05-29T15:41:31.301000", \n\t"title": "", \n\t"type": "Video"\n}')
    
class UsersFrom(form.Form):
    github = fields.TextAreaField('User', widget=TextArea(rows='20', cols='240px'))

#register Views
class CoursesView(ModelView):  
    column_list = ('card',)   
    can_edit = True
    can_create = True 
    form = CoursesForm    
    
class UsersView(ModelView):
    column_list =  ('github',)
    can_edit = True
    can_create = True
    form = UsersFrom 

if __name__ == '__main__':
    admin = Admin(app, name='Admin panel', template_mode=None)
    admin.add_view(CoursesView(db['courses'], "Courses"))    
    admin.add_view(UsersView(db.users, 'Users'))
    # parsing_coursera()
    # with open('data.json', 'r') as f:
    #     json_coursera = json.load(f)
    #     for doc in json_coursera:
    #         db.courses.insert(doc)
    # app.run(debug=True)

