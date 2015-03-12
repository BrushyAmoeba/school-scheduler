import json

def index():
    """
    Index: shows user schedules
    """
    classList = []
    for c in db(db.klass).select():
        classList.append(c.title) 

    return locals()

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

