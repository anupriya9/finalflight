# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
auth.settings.extra_fields['auth_user']= [
	Field('Member_Type',requires=IS_IN_SET(('admin','user')),default='user',writable=False,readable=False),
	Field('Username','string'),
	Field('Phone','integer'),
	Field('City','string'),
	Field('Country','string'),
	]
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'rashi.1234chauhan11@gmail.com'
mail.settings.login = 'rashi.1234chauhan11@gmail.com:siwkqptxmdyyugjw'
#if mail.send(to=['subash.k3110@gmail.com'],subject='test',message='hello'):
    #response.flash = 'email sent'
#else:
    #response.flash = 'sent failed'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
crud.settings.update_deletable = False

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
auth.settings.create_user_groups=None

db.define_table('places',
		Field('body','string',requires=IS_NOT_IN_DB(db,"places.body")))

db.define_table('trips',
		Field('src',requires=IS_IN_DB(db,db.places.body)),
		Field('dest',requires=IS_IN_DB(db,db.places.body)),
		Field('d','date',label="Date",requires=IS_NOT_EMPTY()),
		Field('price','integer',requires=IS_NOT_EMPTY()),
		Field('departure','time',requires=IS_NOT_EMPTY()),
		Field('arrival','time',requires=IS_NOT_EMPTY()),
		Field('cl','string',requires=IS_IN_SET(['Business','Economy'])),
		Field('seats','integer',requires=IS_NOT_EMPTY()),
		Field('logo','upload',requires=IS_NOT_EMPTY()),
		Field('company','string'),
		Field('name','string'))

db.define_table('flight_bookings',
		Field('user_id',"reference auth_user",default=auth.user_id),
		Field('num','integer',requires=IS_NOT_EMPTY()),
		Field('d','date'),
		Field('arrival','time'),
		Field('depart','time'),
		Field('lis','string'),
		Field('price','string'),
		Field('cl','string'),
		Field('booked_in','string'),
		Field('src','string'),
		Field('passengers','string'),
		Field('dest','string'))
db.define_table('category',
    Field('name', 'string', notnull=True, unique=True),
    Field('description', 'text')
)


db.define_table('feedback',
                Field('flight_name','string'),
               Field('comments', 'string', widget=SQLFORM.widgets.text.widget))
