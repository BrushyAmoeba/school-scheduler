def index():
    """
    Index: shows user schedules
    """
    classList = []
    for c in db(db.klass).select():
        classList.append(c.title) 

    return locals()