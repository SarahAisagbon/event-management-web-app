from webapp import db, Attendees

a1 = Attendees(id=1, first_name="Sarah", last_name="Galenda", email='sgalenda@gmail.com', phone='07393906455', event_id=1)
a2 = Attendees(id=2, first_name="Sarah", last_name="Aisagbon", email='saisagbon@yahoo.com', phone='07393906456', event_id=1)
a3 = Attendees(id=3, first_name="Justin", last_name="Bieber", email='jbieber@gmail.com', phone='07757720249', event_id=2)
a4 = Attendees(id=4, first_name="Anita", last_name="Victor", email='avictor@yahoo.co.uk', phone='07523186400', event_id=2)
a5 = Attendees(id=5, first_name="Assana", last_name="Mahmoud", email='assana@gmail.com', phone='07986341975', event_id=2)
a6 = Attendees(id=6, first_name="Rachel", last_name="Smith", email='rachelsmith@yahoo.co.uk', phone='07747734509', event_id=1)

db.session.add_all([a1, a2, a3, a4, a5, a6])

db.session.commit()