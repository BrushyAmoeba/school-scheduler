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
import time
from datetime import datetime


def index():
    """
    Index: shows user schedules
    """
    redirect(URL('manager', 'manage'))
    return locals()

@auth.requires_login()
def manage():
    """
    Network: create network
    """
    networks = []
    for network in db(db.network.user_id==auth.user.id).select():
        networks.append({
            "network_id": str(network.id),
            "title": network.title,
            })
    return locals()

@auth.requires_login()
def createNetwork():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    if db(db.network.title==post.title).select():
        return 'error'
    network = db.network.insert(title = post.title, user_id = post.user_id)
    response = {
        'title': post.title,
        'network_id': network.id, 
    }
    return json.dumps(response)

@auth.requires_login()
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

@auth.requires_login()
def removeNetwork():
    if request.env.request_method!='DELETE': raise HTTP(400)
    post = request.vars
    network_select = db(db.network.id==post.id)
    network = network_select.select().first()
    network_term = db(db.network_term.network_id==network.id).select()
    for t in network_term:
        term_select = db(db.term.id==t.term_id)
        term = term_select.select().first()
        class_term = db(db.class_term.term_id==term.id).select()
        for k in class_term:
            klass_select = db(db.klass.id==k.klass_id)
            klass = klass_select.select().first()
            class_timeslot = db(db.class_timeslot.klass_id==klass.id).select()
            for t in class_timeslot:
                timeslot_select = db(db.timeslot.id==t.timeslot_id)
                timeslot = timeslot_select.select().first()
                timeslot_select.delete()
            klass_select.delete()
        term_select.delete()
    network_select.delete()
    return

@auth.requires_login()
def createTerm():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    term = db.term.insert(title = post.title)
    db.network_term.insert(network_id = post.network_id, term_id = term.id)
    response = {
        'network_id': str(post.network_id),
        'title': post.title,
        'term_id': term.id,
    }
    return json.dumps(response)

@auth.requires_login()
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

@auth.requires_login()
def removeTerm():
    if request.env.request_method!='DELETE': raise HTTP(400)
    post = request.vars
    term_select = db(db.term.id==post.id)
    term = term_select.select().first()
    class_term = db(db.class_term.term_id==term.id).select()
    for k in class_term:
        klass_select = db(db.klass.id==k.klass_id)
        klass = klass_select.select().first()
        class_timeslot = db(db.class_timeslot.klass_id==klass.id).select()
        for t in class_timeslot:
            timeslot_select = db(db.timeslot.id==t.timeslot_id)
            timeslot = timeslot_select.select().first()
            timeslot_select.delete()
        klass_select.delete()
    term_select.delete()
    return

@auth.requires_login()
def createKlass():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    #Teacher Stuff first
    teacher_id = db(db.teacher.name==post.teacher).update(name = post.teacher) or db.teacher.insert(name = post.teacher)
    print(teacher_id)
    klass_id = db.klass.insert(title = post.title, teacher_id = teacher_id)
    db.class_term.insert(klass_id = klass_id, term_id = post.term_id)
    response = {
        'term_id': str(post.term_id),
        'title': post.title,
        'teacher': post.teacher,
        'klass_id': klass_id,
    }
    return json.dumps(response)

@auth.requires_login()
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
            "start_time":timeslot.start_time.strftime('%I:%M %p'),
            "end_time":timeslot.end_time.strftime('%I:%M %p'),
        })
    return json.dumps(timeslotList)

@auth.requires_login()
def removeKlass():
    if request.env.request_method!='DELETE': raise HTTP(400)
    post = request.vars
    klass_select = db(db.klass.id==post.id)
    klass = klass_select.select().first()
    class_timeslot = db(db.class_timeslot.klass_id==klass.id).select()
    for t in class_timeslot:
        timeslot_select = db(db.timeslot.id==t.timeslot_id)
        timeslot = timeslot_select.select().first()
        timeslot_select.delete()
    klass_select.delete()
    return

@auth.requires_login()
def createTimeslot():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    start_time = datetime.strptime(post.start, '%H:%M:%S').time()
    end_time = datetime.strptime(post.end, '%H:%M:%S').time()
    timeslot_id = db.timeslot.insert(meet_day = post.meet_day, start_time = start_time, end_time = end_time)
    db.class_timeslot.insert(timeslot_id = timeslot_id, klass_id = post.klass_id)
    response = {
        'timeslot_id': str(timeslot_id),
        'meet_day': post.meet_day,
        'start_time': start_time.strftime('%I:%M %p'),
        'end_time': end_time.strftime('%I:%M %p'),
        'klass_id': str(post.klass_id),     
    }
    return json.dumps(response)

@auth.requires_login()
def removeTimeslot():
    if request.env.request_method!='DELETE': raise HTTP(400)
    post = request.vars
    timeslot_select = db(db.timeslot.id==post.id)
    timeslot = timeslot_select.select().first()
    timeslot_select.delete()
    return
