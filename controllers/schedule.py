import json

@auth.requires_login()
def index():
    """
    Index: shows user schedules
    """
    classList = []
    schedList = []
    for c in db(db.klass).select():
        classList.append(c.title)
    networks = db(db.network).select()
    sched_ids = db(db.schedule_user.user_id==auth.user_id).select()
    for s in sched_ids:
        sched = db(db.schedule.id==s.schedule_id).select().first()
        print(sched)
        schedList.append({
            'title': sched.title,
            'id': str(sched.id),
        })
    return locals()

@auth.requires_login()
def friends():
    """
    Friends: shows users friends and friend requests
    """
    userList = []
    requestList = []
    friendList = []
    for u in db(db.auth_user).select():
        userList.append(u.first_name + " " + u.last_name)
    for r in db(db.friends.user_id2 == auth.user).select():
        if r.status == 0:
          friend = db(db.auth_user.id==r.user_id1).select().first()
          requestList.append({
            'name':friend.first_name + " " + friend.last_name,
            'id':str(friend.id),
          })
    for f in db(db.friends).select():
        if f.user_id1 == auth.user.id or f.user_id2 == auth.user.id:
          if f.user_id1 == auth.user.id and f.status==1:
            friend = db(db.auth_user.id==f.user_id2).select().first()
            friendList.append({
              'name':friend.first_name + " " + friend.last_name,
              'id':str(friend.id),
            })
          if f.user_id2 == auth.user.id and f.status==1:
            friend = db(db.auth_user.id==f.user_id1).select().first()
            friendList.append({
              'name':friend.first_name + " " + friend.last_name,
              'id':str(friend.id),
            })
    return locals()

@auth.requires_login()
def newSched():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    defalt = post.defalt
    if db(db.schedule_user.user_id==auth.user_id).select():
      if defalt==True:
        sched_user = db(db.schedule_user.user_id==auth.user_id).select()
        for s in sched_user:
          curr_sched = db(db.schedule.id==s.schedule_id).select().first()
          if curr_sched.defalt==True:
            db(db.schedule.id==s.schedule_id).update(defalt=False)
    else:
      defalt = True
    sched = db.schedule.insert(title = post.title, defalt = defalt)
    db.schedule_user.insert(schedule_id = sched.id, user_id = auth.user_id)
    return sched.id

@auth.requires_login()
def addClassToSched():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    term_id = post.term_id
    sched_id = post.sched_id
    if sched_id == -1:
      schedule_user = db(db.schedule_user.user_id==auth.user_id).select()
      for s in schedule_user:
        sched = db(db.schedule.id==s.id).select().first()
        print(sched_id)
        if sched.defalt==True:
          sched_id = sched.id
          break
    title = post.title
    class_term = db(db.class_term.term_id==term_id).select()
    for c in class_term:
      klass = db(db.klass.id==c.klass_id).select().first()
      if klass.title == title:
        db.schedule_class.insert(schedule_id = sched_id, klass_id = klass.id)
        return

@auth.requires_login()
def loadSched():
    if request.env.request_method!='GET': raise HTTP(400)
    sched_id = request.vars.id
    if int(request.vars.id)==-1:
      sched_user = db(db.schedule_user.user_id==auth.user_id).select()
      for s in sched_user:
        sched = db(db.schedule.id==s.id).select().first()
        if sched.defalt==True:
          sched_id = sched.id
    klasses = db(db.schedule_class.schedule_id==sched_id).select()
    klassesList = []
    for k in klasses:
        klass = db(db.klass.id==k.klass_id).select().first()
        timeslots = db(db.class_timeslot.klass_id==klass.id).select()
        for t in timeslots:
          timeslot = db(db.timeslot.id==t.id).select().first()
          #teacher_id = db(db.teacher_class.klass_id == klass.id).select().first().teacher_id
          teacher_id = 1
          teacher = db(db.teacher.id == teacher_id).select().first().name
          klassesList.append({
            "title":klass.title,
            "description":teacher,
            "meet_day":timeslot.meet_day,
            "start_time":timeslot.start_time.isoformat(),
            "end_time":timeslot.end_time.isoformat(),
          })
    print(klassesList)
    return json.dumps(klassesList)

@auth.requires_login()
def getTerms():
    if request.env.request_method!='GET': raise HTTP(400)
    network_id =request.vars.id
    print(network_id)
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
def getKlasses():
    if request.env.request_method!='GET': raise HTTP(400)
    term_id =request.vars.id
    klasses = db(db.class_term.term_id==term_id).select()
    klassList = []
    klassTitleList = []
    for k in klasses:
        klass = db(db.klass.id==k.klass_id).select().first()
        klassTitleList.append(klass.title)
        klassList.append({
            "klass_id": str(klass.id),
            "title":klass.title,
        })
    return json.dumps(klassTitleList)

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

def findUsers():
  if request.env.request_method!='GET': raise HTTP(400)
  query = reduce(lambda a,b:a&b,
                        [db.auth_user.first_name.contains(k)|db.auth_user.last_name.contains(k) \
                             for k in request.vars.str.split()])
  people = db(query).select(orderby=db.auth_user.first_name|db.auth_user.last_name)
  peopleList = []
  for person in people:
    are_friends = False
    if person.id == auth.user.id:
      are_friends = True
    if db(db.friends.user_id1==person.id).select():
      friend = db(db.friends.user_id1==person.id).select().first()
      if friend.user_id2 == auth.user.id:
        are_friends = True
    if db(db.friends.user_id2==person.id).select():
      friend = db(db.friends.user_id2==person.id).select().first()
      if friend.user_id1 == auth.user.id:
        are_friends = True
    peopleDict = {
      "name":person.first_name + " " + person.last_name,
      "id":person.id,
      "are_friends": are_friends,
    }
    peopleList.append(peopleDict)   
  return json.dumps(peopleList)

@auth.requires_login()
def addFriend():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    user_id2 = post.user_id
    db.friends.insert(user_id1 = auth.user, user_id2 = user_id2, status=0)
    return

@auth.requires_login()
def acceptFriend():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    user_id1 = post.user_id
    db(db.friends.user_id1==user_id1).update(status=1)
    return

@auth.requires_login()
def denyFriend():
    if request.env.request_method!='POST': raise HTTP(400)
    post = request.post_vars
    user_id1 = post.user_id
    db(db.friends.user_id1==user_id1).delete()
    return