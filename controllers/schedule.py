import json

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
        schedList.append({
            'title': sched.title,
            'id': sched.id,
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
    return

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

def getNetId():
  if request.env.request_method!='GET': raise HTTP(400)
  network_title = request.vars.str
  network_id = db(db.network.title==network_title).select().first().id
  return network_id

def getTermId():
  if request.env.request_method!='GET': raise HTTP(400)
  term_title = request.vars.str
  network_id = request.vars.id
  networks = db(db.network_term.network_id==network_id).select()
  for n in networks:
    term = db(db.term.id==n.term_id).select().first()
    if term.title == term_title:
      return term.id

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

