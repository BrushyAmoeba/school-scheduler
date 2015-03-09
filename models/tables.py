db.define_table('teacher',
    Field('name'),
    )

db.define_table('klass',
    Field('title'),
    Field('teacher_id', 'reference teacher'),
    )

db.define_table('teacher_class', 
    Field('teacher_id', 'reference teacher'),
    Field('klass_id', 'reference klass'),
    )

db.define_table('timeslot',
    Field('meet_day', 'integer'),
    Field('start_time', 'time'),
    Field('end_time', 'time'),
    )
 

db.define_table('class_timeslot', 
    Field('timeslot_id', 'reference timeslot'),
    Field('klass_id', 'reference klass'),
    )


db.define_table('class_student',
    Field('student', db.auth_user),
    Field('klass_id', 'reference klass'),
    )

