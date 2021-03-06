# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

import datetime
def index():
	form=SQLFORM.factory(
			Field('From',requires=IS_IN_DB(db,db.places.body)),
			Field('To',requires=IS_IN_DB(db,db.places.body)),
			Field('d','date',label='Departure(Date)',requires=IS_DATE()),
			Field('d1','date',label='Arrival(Date)',readable=False),
			Field('Class',requires=IS_IN_SET(['Business','Economy'])),
			Field('seats',label='Number of passengers',requires=IS_IN_SET((1,2,3,4,5,6))))
	if form.accepts(request.vars,session):
		if form.vars.From == form.vars.To:
			session.flash="Source and Destination should not be the same!"
			redirect(URL('index'))
		elif form.vars.d<datetime.date.today():
			session.flash="Enter a valid date!"
			redirect(URL('index'))
		elif form.vars.d1:
			session.seats=request.vars.seats
			session.date=request.vars.d
			session.date2=request.vars.d1
		 	redirect(URL('round_search',args=(request.vars.From,request.vars.To,request.vars.d,request.vars.seats,request.vars.Class,request.vars.d1)))
		else:
			session.seats=request.vars.seats
			session.date=request.vars.d
			redirect(URL('search',args=(request.vars.From,request.vars.To,request.vars.d,request.vars.seats,request.vars.Class)))
	session.var=1
	return dict(form=form)

def round_search():
	src=db((db.trips.src==request.args(0))&(db.trips.d==request.args(2))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(1))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Flight Found! :( "
        	redirect(URL('index'))
	lis=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis.append(que)
	if len(lis)==0:
	  	session.flash="No Flight found!"
	  	redirect(URL('index'))
	seats=[]
	price=[]
	logo=[]
	dtime=[]
	atime=[]
	n=[]
	company=[]
	for i in range(len(lis)):
		send=[]
		some=db((db.trips.name==lis[i])&(db.trips.src==request.args(0))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime.append(some[0].departure)
			while desti!=request.args(1):
				some=db((db.trips.name==lis[i])&(db.trips.src==desti)).select()
				if len(some):	
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No Flight Found!"
#					redirect(URL('index'))
			atime.append(some[0].arrival)
			n.append(send)
			logo.append(some[0].logo)
			company.append(some[0].company)
			seats.append(m)
			price.append(p)
		else:
			session.flash="No Flight found!"
#			redirect(URL('index'))
	l=len(lis)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats[i])
			price.remove(price[i])
			logo.remove(logo[i])
			atime.remove(atime[i])
			dtime.remove(dtime[i])
			lis.remove(lis[i])
	new=[]
	for i in n:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new.append(st[0:-1])

	src=db((db.trips.src==request.args(1))&(db.trips.d==request.args(5))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(0))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Flight Found! :( "
        	redirect(URL('index'))
	lis1=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis1.append(que)
	if len(lis1)==0:
	  	session.flash="No Flight found!"
	  	redirect(URL('index'))
	seats1=[]
	price1=[]
	logo1=[]
	dtime1=[]
	atime1=[]
	n1=[]
	company1=[]
	for i in range(len(lis1)):
		send=[]
		some=db((db.trips.name==lis1[i])&(db.trips.src==request.args(1))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime1.append(some[0].departure)
			while desti!=request.args(0):
				some=db((db.trips.name==lis1[i])&(db.trips.src==desti)).select()
				if len(some):
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No Flight Found!"
#					redirect(URL('index'))
			atime1.append(some[0].arrival)
			n1.append(send)
			logo1.append(some[0].logo)
			company1.append(some[0].company)
			seats1.append(m)
			price1.append(p)
		else:
			session.flash="No Flight found!"
#			redirect(URL('index'))
	l=len(lis1)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats1[i])
			price.remove(price1[i])
			logo.remove(logo1[i])
			atime.remove(atime1[i])
			dtime.remove(dtime1[i])
			lis.remove(lis1[i])
	new1=[]
	for i in n1:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new1.append(st[0:-1])
	return dict(lis=lis,seats=seats,new=new,price=price,dtime=dtime,atime=atime,logo=logo,company=company,lis1=lis1,seats1=seats1,new1=new1,price1=price1,dtime1=dtime1,atime1=atime1,logo1=logo1,company1=company1)

def search():
	session.date=request.args(2)
	src=db((db.trips.src==request.args(0))&(db.trips.d==request.args(2))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(1))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Flight Found! :( "
        	redirect(URL('index'))
	lis=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis.append(que)
	if len(lis)==0:
	  	session.flash="No Flight found!"
	  	redirect(URL('index'))
	seats=[]
	price=[]
	logo=[]
	dtime=[]
	atime=[]
	n=[]
	company=[]
	for i in range(len(lis)):
		send=[]
		some=db((db.trips.name==lis[i])&(db.trips.src==request.args(0))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime.append(some[0].departure)
			while desti!=request.args(1):
				some=db((db.trips.name==lis[i])&(db.trips.src==desti)).select()
				if len(some):
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No Flight Found!"
					redirect(URL('index'))
			atime.append(some[0].arrival)
			n.append(send)
			logo.append(some[0].logo)
			company.append(some[0].company)
			seats.append(m)
			price.append(p)
		else:
			session.flash="No Flight found!"
			redirect(URL('index'))
	l=len(lis)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats[i])
			price.remove(price[i])
			logo.remove(logo[i])
			atime.remove(atime[i])
			dtime.remove(dtime[i])
			lis.remove(lis[i])
	new=[]
	for i in n:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new.append(st[0:-1])
	return dict(lis=lis,seats=seats,new=new,price=price,dtime=dtime,atime=atime,logo=logo,company=company)

import datetime
@auth.requires_login()
def passengers_details():
    form1=SQLFORM.factory(
            Field('Title1',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name1',requires=IS_NOT_EMPTY()),
            Field('Gender1',requires=IS_IN_SET(['Male','Female'])),
			Field('age1',requires=IS_NOT_EMPTY()),
			Field('dob1','date',requires=IS_DATE()),
            Field('Address1',requires=IS_NOT_EMPTY()))
    form2=SQLFORM.factory(
            Field('Title2',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name2',requires=IS_NOT_EMPTY()),
            Field('Gender2',requires=IS_IN_SET(['Male','Female'])),
			Field('age2',requires=IS_NOT_EMPTY()),
			Field('dob2','date',requires=IS_DATE()),
            Field('Address2',requires=IS_NOT_EMPTY())
        )
    form3=SQLFORM.factory(
            Field('Title3',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name3',requires=IS_NOT_EMPTY()),
            Field('Gender3',requires=IS_IN_SET(['Male','Female'])),
			Field('age3',requires=IS_NOT_EMPTY()),
			Field('dob3','date',requires=IS_DATE()),
            Field('Address3',requires=IS_NOT_EMPTY())
        )
    form4=SQLFORM.factory(
            Field('Title4',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name4',requires=IS_NOT_EMPTY()),
            Field('Gender4',requires=IS_IN_SET(['Male','Female'])),
			Field('age4',requires=IS_NOT_EMPTY()),
			Field('dob4','date',requires=IS_DATE()),
            Field('Address4',requires=IS_NOT_EMPTY())
        )
    form5=SQLFORM.factory(
            Field('Title5',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name5',requires=IS_NOT_EMPTY()),
            Field('Gender5',requires=IS_IN_SET(['Male','Female'])),
			Field('age5',requires=IS_NOT_EMPTY()),
			Field('dob5','date',requires=IS_DATE()),
            Field('Address5',requires=IS_NOT_EMPTY())
        )
    form6=SQLFORM.factory(
            Field('Title6',requires=IS_IN_SET(['Mr','Ms'])),
			Field('Name6',requires=IS_NOT_EMPTY()),
            Field('Gender6',requires=IS_IN_SET(['Male','Female'])),
			Field('age6',requires=IS_NOT_EMPTY()),
			Field('dob6','date',requires=IS_DATE()),
            Field('Address6',requires=IS_NOT_EMPTY())
        )
    if form1.accepts(request.vars,session):
        if form1.vars.dob1>datetime.date.today():
            session.flash="Date of Birth cannot be a future date!!"
            redirect(URL('default','passengers_details'))
        #if form1.accepted:
        else:                       redirect(URL('confirm',vars=dict(lis=request.vars.lis,dtime=request.vars.dtime,atime=request.vars.atime,seats=request.vars.seats,price=request.vars.price,send=request.vars.send,src=request.vars.src,dest=request.vars.dest,cl=request.vars.cl)))
    session.var=1
    return dict(form1=form1,form2=form2,form3=form3,form4=form4,form5=form5,form6=form6)

import time
@auth.requires_login()
def confirm():
	return dict()

@auth.requires_login()
def pay():
	return dict()

@auth.requires_login()
def credit():
    form=SQLFORM.factory(
            Field('CardNumber',requires=IS_NOT_EMPTY()),
            Field('CardHolderName',requires=IS_NOT_EMPTY()),
            Field('Month',requires=IS_IN_SET(['1','2','3','4','5','6','7','8','9','10','11','12'])), Field('Year',requires=IS_IN_SET(['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033'])),
            Field('cvv',requires=IS_NOT_EMPTY())
            )
    return dict(form=form)

@auth.requires_login()
def debit():
    form=SQLFORM.factory(
            Field('Bank',requires=IS_IN_SET(['Canara Bank','SBI','HDFC bank','Punjab Bank','ICICI','Axis Bank','Bank of India'])),
            Field('CardNumber',requires=IS_NOT_EMPTY()),
            Field('CardHolderName',requires=IS_NOT_EMPTY()),
            Field('Month',requires=IS_IN_SET(['1','2','3','4','5','6','7','8','9','10','11','12'])), Field('Year',requires=IS_IN_SET(['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033'])),
            Field('cvv',requires=IS_NOT_EMPTY())
            )
    return dict(form=form)

@auth.requires_login()
def wallet():
    return locals()

@auth.requires_login()
def help():
    return locals()

@auth.requires_login()
def round_confirm():
	flight1=request.vars.flight1.split('^')
	flight2=request.vars.flight2.split('^')
	return dict(flight1=flight1,flight2=flight2)

def round_ticket():
#	print session.date
#	print session.date2
#	print session.seats

	flight1=request.vars.flight1.split('^')
	n1=flight1[len(flight1)-1].split('_') 
	flight2=request.vars.flight2.split('^')
	n2=flight2[len(flight2)-1].split('_')
	for i in range(len(n1)):
		seats=db(db.trips.id==n1[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n1[i]).update(seats=seat-int(session.seats))
	for i in range(len(n2)):
		seats=db(db.trips.id==n2[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n2[i]).update(seats=seat-int(session.seats))
	date=datetime.datetime.strptime(session.date,"%Y-%m-%d").date()
	arrival=datetime.datetime.strptime(flight1[2],"%H:%M:%S").time()
	depart=datetime.datetime.strptime(flight1[3],"%H:%M:%S").time()
	print date, arrival, depart
	db.flight_bookings.insert(user_id=auth.user.id,d=date,arrival=arrival,depart=depart,lis=flight1[6],price=flight1[5],booked_in=flight1[0],src=request.args(0),dest=request.args(1),cl=request.args(2),num=int(session.seats))
	date=datetime.datetime.strptime(session.date2,"%Y-%m-%d").date()
	arrival=datetime.datetime.strptime(flight2[2],"%H:%M:%S").time()
	depart=datetime.datetime.strptime(flight2[3],"%H:%M:%S").time()
	print date, arrival, depart
	db.flight_bookings.insert(user_id=auth.user.id,d=date,arrival=arrival,depart=depart,lis=flight2[6],price=flight2[5],booked_in=flight2[0],src=request.args(1),dest=request.args(0),cl=request.args(2),num=int(session.seats))
	redirect(URL('index'))
    
#from gluon.tools import Mail
#mail = Mail()
#mail.settings.server = 'smtp.gmail.com:587'
#mail.settings.sender = 'Travel India With us'
#mail.settings.login = 'anupriyabiet@gmail.com'

def book():
	n=request.vars.send
	n=request.vars.send.split('_')
	red=db((db.trips.name==request.vars.lis)&(db.trips.cl==request.vars.cl)).select()
	for i in range(len(n)):
		seats=db(db.trips.id==n[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n[i]).update(seats=seat-int(request.vars.seats))
	db.flight_bookings.insert(user_id=auth.user.id,num=request.vars.seats,d=session.date,arrival=request.vars.atime,depart=request.vars.dtime,lis=request.vars.send,price=request.vars.price,booked_in=request.vars.lis,src=request.vars.src,dest=request.vars.dest,cl=request.vars.cl)
	email=auth.user.email
	mail.send(to=['anupriyabiet@gmail.com'],
			subject='Ticket booked!',
			message='Flight id :'+request.vars.lis+'\nDeparture time : '+request.vars.dtime+'\nArrival time : '+request.vars.atime+'\nNumber of seats : '+request.vars.seats+'\n')
	session.flash="Your ticket has been booked!"
	redirect(URL('index'))

@auth.requires_login()
def profile():
	rec=db(auth.user.id==db.auth_user.id).select()
	form=crud.update(db.auth_user,auth.user.id)
	crud.settings.update_deletable = False
	if (form.process().accepted):
		redirect(URL('profile'))
	return locals()

@auth.requires_login()
def viewbookings():
        print auth.user.id
        ctr1=0
        ctr2=0
        c1=0
        c2=0
        import datetime
        d1=datetime.date.today()
        rec=db(db.hotels.user_id==auth.user.id).select(db.hotels.ALL,orderby=db.hotels.checkin)
        flag1=0
        flag2=0
        f1=0
        f2=0
        print len(rec),
        for i in range(len(rec)):
                print 'i m hrer'
                if ((rec[i]['checkin']-d1)<datetime.timedelta(0)):
                        ctr1=ctr1+1 
                elif ((rec[i]['checkin']-d1)>=datetime.timedelta(0)):
                        c1=c1+1
        if (ctr1==0):
                flag1=1
        if (c1==0):
                f1=1
        print flag1
        flight=db(db.flight_bookings.user_id==auth.user.id).select(db.flight_bookings.ALL,orderby=db.flight_bookings.d)
        for i in range(len(flight)):
                if ((flight[i]['d']-d1)<datetime.timedelta(0)):
                        ctr2=ctr2+1 
                if ((flight[i]['d']-d1)>=datetime.timedelta(0)):
                        c2=c2+1
        if (ctr2==len(flight)):
                flag2=1
        if (c2==len(flight)):
                f2=1
        return locals()

@auth.requires_membership('managers')
def add_flight():
    cities=db(db.places.id>0).select(db.places.body)
    form=SQLFORM(db.places).process()
    if form.accepted: redirect(URL('add_flight'))
    return dict(form=form,cities=cities)


@auth.requires_membership('managers')
def add_new():
    tripDetails=db(db.trips.id>0).select(db.trips.ALL)
    form=SQLFORM(db.trips).process()
    if form.accepted: redirect(URL('add_new'))
    return dict(form=form,tripDetails=tripDetails)

@auth.requires_membership('managers')
def view_feedbacks():
    feeds=db(db.feedback.id>0).select(db.feedback.ALL)
    form=SQLFORM(db.feedback).process()
    if form.accepted: redirect(URL('view_feedbacks'))
    return dict(form=form, feeds=feeds)

def dum():
        print "id=",
        print int(request.args[1])
        if (int(request.args[0])==0):
                q=db((db.flight_bookings.id==int(request.args[1]))).select()
                a=q[0]['lis'].split('_')
                for i in range(len(a)):
                        s= db(db.trips.id==int(a[i])).select(db.trips.seats)
                        db(db.trips.id==int(a[i])).update(seats=s[0]['seats']+int(request.args[3]))
                db(db.flight_bookings.id==int(request.args[1])).delete()
                email=auth.user.email
	        mail.send(to=[email],
			        subject='Flight Cancellation',
			        message='Your flight booking for '+q[0]['booked_in']+' from '+q[0]['src']+' to '+q[0]['dest']+' on '+str(q[0]['d'])+' has been cancelled.'   
                        )

        redirect(URL('viewbookings'))
        
        return locals()

def feedback():
    form=SQLFORM(db.feedback).process()
    if form.accepted: redirect(URL('viewbookings'))
    return dict(form=form)


@auth.requires_login()
def profile():
	rec=db(auth.user.id==db.auth_user.id).select()
	form=crud.update(db.auth_user,auth.user.id)
	crud.settings.update_deletable = False
	if (form.process().accepted):
		redirect(URL('profile'))
	return locals()
def review():
    return locals()
def SpiceJet():
    return locals()
def Indigo():
    return locals()
def AirIndia():
    return locals()



@auth.requires_login()
def viewbookings():
        #print auth.user.id
        ctr1=0
        ctr2=0
        c1=0
        c2=0
        import datetime
        d1=datetime.date.today()
        flag1=0
        flag2=0
        f1=0
        f2=0
        if (ctr1==0):
                flag1=1
        if (c1==0):
                f1=1
        print flag1
        flight=db(db.flight_bookings.user_id==auth.user.id).select(db.flight_bookings.ALL,orderby=db.flight_bookings.d)
        for i in range(len(flight)):
                if ((flight[i]['d']-d1)<datetime.timedelta(0)):
                        ctr2=ctr2+1 
                if ((flight[i]['d']-d1)>=datetime.timedelta(0)):
                        c2=c2+1
        if (ctr2==len(flight)):
                flag2=1
        if (c2==len(flight)):
                f2=1
        return locals()
