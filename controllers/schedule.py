import json

def index():
    """
    Index: shows user schedules
    """
    classList = []
    for c in db(db.klass).select():
        classList.append(c.title)
    networks = db(db.network).select()
    return locals()

def getTerms():
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

