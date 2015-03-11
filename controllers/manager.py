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
            "network_id": str(network.id),
            "title": network.title,
            })
    return locals()

def createNetwork():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    db.network.insert(title = post.title)
    response = {
        'title': post.title, 
    }
    return json.dumps(response)

def viewNetwork():
    if request.env.request_method!='GET': raise HTTP(400)
    network_id =request.vars.id
    terms = db(db.network_term.network_id==network_id).select()
    termList = []
    for t in terms:
        term = db(db.term.id==t.term_id).select().first()
        termList.append({
            "term_id": str(term.id),
            "title":term.title,
        })
    return json.dumps(termList)

def createTerm():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    term = db.term.insert(title = post.title)
    db.network_term.insert(network_id = post.network_id, term_id = term.id)
    response = {
        'network_id': str(post.network_id),
        'title': post.title,
    }
    return json.dumps(response)

def viewTerm():
    if request.env.request_method!='GET': raise HTTP(400)
    term_id =request.vars.id
    klasses = db(db.class_term.term_id==term_id).select()
    klassList = []
    for k in klasses:
        klass = db(db.klass.id==k.klass_id).select().first()
        klassList.append({
            "klass_id": str(klass.id),
            "title":klass.title,
        })
    return json.dumps(klassList)

def createKlass():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    #Teacher Stuff first
    teacher_id = db(db.teacher.name==post.teacher).update(name = post.teacher) or db.teacher.insert(name = post.teacher)
    klass_id = db.klass.insert(title = post.title, teacher_id = teacher_id)
    db.class_term.insert(klass_id = klass_id, term_id = post.term_id)
    response = {
        'term_id': str(post.term_id),
        'title': post.title,
        'teacher': post.teacher,
    }
    return json.dumps(response)

def viewKlass():
    if request.env.request_method!='GET': raise HTTP(400)
    klass_id =request.vars.id
    timeslots = db(db.class_timeslot.klass_id==klass_id).select()
    timeslotList = []
    for t in timeslots:
        timeslot = db(db.timeslot.id==t.timeslot_id).select().first()
        timeslotList.append({
            "timeslot_id": str(timeslot.id),
            "meet_day":timeslot.meet_day,
            "start_time":timeslot.start_time,
            "end_time":timeslot.end_time,
        })
    return json.dumps(timeslotList)
