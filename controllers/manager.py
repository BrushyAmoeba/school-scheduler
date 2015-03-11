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
    Index: shows user schedules
    """
    classList = []
    for c in db(db.klass).select():
        classList.append(c.title) 

    return locals()

def manage():
    """
    Network: create network
    """
    networks = []
    for network in db(db.network).select():
        networks.append({
            "id": str(network.id),
            "title": network.title,
            })
    return locals()

def viewNetwork():
    if request.env.request_method!='GET': raise HTTP(400)
    network_id =request.vars.id
    terms = db(db.network_term.network_id==network_id).select()
    termList = []
    for t in terms:
        term = db(db.term.id==t.term_id).select().first()
        termList.append({
            "id": str(term.id),
            "title":term.title,
        })
    return json.dumps(termList)

def createNetwork():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    db.network.insert(title = post.title)
    response = {
        'id': str(post.id),
        'title': post.title, 
    }
    return json.dumps(response)

def createTerm():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    term = db.term.insert(title = post.title)
    db.network_term.insert(network_id = post.network_id, term_id = term.id)
    response = {
        'id': str(post.id),
        'title': post.title,
    }
    return json.dumps(response)


def getTimeslots():
  if request.env.request_method!='GET': raise HTTP(400)
  me = auth.user_id
  student_classes = db(db.class_student.student == auth.user).select()
  timeslotList = []
  for c in student_classes:
      klass_timeslots = db(db.class_timeslot.klass_id == c.klass_id).select()
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
  return json.dumps(timeslotList)

