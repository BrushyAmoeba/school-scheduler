# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import json


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    return locals()

def getTimeslots():
  if request.env.request_method!='GET': raise HTTP(400)
  klass_timeslots = db(db.class_timeslot).select()
  timeslotList = []
  for k in klass_timeslots:
    t_id = k.timeslot_id
    k_id = k.klass_id
    timeslot = db(db.timeslot.id == t_id).select().first()
    klass = db(db.klass.id == k_id).select().first()
    teacher_id = db(db.teacher_class.klass_id == k_id).select().first().teacher_id
    teacher = db(db.teacher.id == teacher_id).select().first().name
    timeslotDict = {
      "title":klass.title,
      "teacher":teacher,
      "meet_day":timeslot.meet_day,
      "start_time":timeslot.start_time.isoformat(),
      "end_time":timeslot.end_time.isoformat(),
    }
    timeslotList.append(timeslotDict)   
    print(timeslotList)
  return json.dumps(timeslotList)

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


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
