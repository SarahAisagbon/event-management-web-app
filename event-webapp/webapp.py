from flask import Flask, request, redirect, url_for, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Models
class Events(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    start_time = db.Column(db.String(100), unique=False, nullable=False)
    end_time = db.Column(db.String(100), unique=False, nullable=False)
    location = db.Column(db.String(100), unique=False, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    attendees = db.relationship('Attendees', backref='events')

class Attendees(db.Model):
    __tablename__ = 'attendees'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

@app.route("/")
def index():
    return render_template('base.html')
  
@app.route("/events/list", methods=["GET"])
def all_events():
    try:
        events = Events.query.all()
        return render_template('event_index.html', events=events)
    except:
        return render_template('event_index.html')

@app.route('/events/attendees/list')
def find_all_attendees():
    return render_template('select_event.html', data='/events/attendees/list')

@app.route('/events/attendees/list', methods=["POST"])
def find_all_event_attendees():
    id = request.form.get("id")
    return redirect(url_for('all_attendees', event_id=id))

@app.route("/events/<int:event_id>/attendees", methods=["GET"])
def all_attendees(event_id):
    try:
        attendees = Attendees.query.filter_by(event_id = event_id).all()
        event = Events.query.get_or_404(event_id)
        return render_template('attendees_index.html', event=event_id, event_name=event.name, attendees= attendees)
    except:
        return redirect('/')
        
@app.route('/events/add')
def add_event():
    return render_template('add_event.html')

@app.route('/events/add', methods= ['POST'])
def event():
    # In this function we will input data from the
    # form page and store it in our database. Remember
    # that inside the get the name should exactly be the same
    # as that in the html input fields
    try:
        name = request.form.get("name")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        location = request.form.get("location")
        budget = request.form.get("budget")
        
        # create an object of the Profile class of models and
        # store data as a row in our datatable
        event = Events(name=name, start_time = start_time, end_time = end_time, location = location, budget = budget)
        db.session.add(event)
        db.session.commit()
        print('Record was successfully added')
        
    except Exception as e:
        print("Failed to add event")
        
    return redirect(url_for('all_events'))

@app.route('/events/<int:id>', methods=["GET"])
def view_event(id):
    # view the data on the basis of unique id and
    # directs to home page
    event = Events.query.get_or_404(id)
    return render_template('event.html', event=event)

@app.route('/events/attendees/add')
def find_event_attendee_add():
    return render_template('select_event.html', data='/events/attendees/add')

@app.route('/events/attendees/add', methods=["POST"])
def find_event_attendee_to_add():
    id = request.form.get("id")
    return redirect(url_for('add_attendee', id=id))

@app.route('/events/<int:id>/attendees/add')
def add_attendee(id):
    event = Events.query.get_or_404(id)
    return render_template('add_attendee.html', event=event)

@app.route('/events/<int:id>/attendees/add', methods=['POST'])
def attendee(id):
    # In this function we will input data from the
    # form page and store it in our database. Remember
    # that inside the get the name should exactly be the same
    # as that in the html input fields
    try:
        event = Events.query.get_or_404(id)
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone_number")
        print('Form Completed')
        
        # create an object of the Profile class of models and
        # store data as a row in our datatable
        #attendee = Attendees(first_name=first_name, last_name=last_name, email=email, phone=phone, events=event)
        attendee = Attendees(first_name=first_name, last_name=last_name, email=email, phone=phone, event_id=event.id)
        db.session.add(attendee)
        print('Added')
        db.session.commit()
        print('Record was successfully added')
            
    except Exception as e:
        print(e)
        print("Failed to add attendee")
    
    return redirect(url_for('all_attendees', event_id = id))

@app.route('/events/edit')
def find_event_edit():
    return render_template('select_event.html', data = '/events/edit')

@app.route('/events/edit', methods=["POST"])
def find_event_to_edit():
    id = request.form.get("id")
    return redirect(url_for('edit_event', id=id))

@app.route('/events/<int:id>/edit')
def edit_event(id):
    return render_template('edit_event.html', data=id)

@app.route('/events/<int:id>/edit', methods=["POST"])
def edit(id):
    # edit the data on the basis of unique id and
    # directs to home page
    event = Events.query.filter_by(id=id).first()
    #User.query.filter_by(role='admin').update(dict(permission='add_user'))
    event_feature = request.form.get("event_feature")
    if event_feature == 'name':
        event.name = request.form.get("new_value")
    elif event_feature == 'start_time':
        event.start_time = request.form.get("new_value")
    elif event_feature == 'end_time':
        event.end_time = request.form.get("new_value")
    elif event_feature == 'location':
        event.location = request.form.get("new_value")
    else:
        event.budget = request.form.get("new_value")
    db.session.commit()
    return redirect('/')

@app.route('/events/delete')
def find_event_delete():
    return render_template('select_event.html', data='/events/delete')

@app.route('/events/delete')
def find_event_to_delete():
    id = request.form.get("id")
    return redirect(url_for('erase_event', id=id))

@app.route('/events/<int:id>/delete', methods=["GET"])
def erase_event(id):
    # deletes the data on the basis of unique id and
    # directs to home page
    #data = Events.query.get_or_404(id)
    event = Events.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    return redirect('/')

@app.route('/events/<int:id>/attendees/<int:attendees_id>/edit')
def edit_attendee(id, attendees_id):
    return render_template('edit_attendee.html', event=id, attendee=attendees_id)

@app.route('/events/<int:id>/attendees/<int:attendees_id>/edit', methods=["POST"])
def edit_attendee_details(id, attendees_id):
    # edit the data on the basis of unique id and
    # directs to home page
    attendee = Attendees.query.filter_by(id=attendees_id).first()
    #User.query.filter_by(role='admin').update(dict(permission='add_user'))
    attendee_details = request.form.get("attendee_details")
    if attendee_details == 'first_name':
        attendee.first_name = request.form.get("new_value")
    elif attendee_details == 'last_name':
        attendee.last_name = request.form.get("new_value")
    elif attendee_details == 'email':
        attendee.email = request.form.get("new_value")
    else:
        attendee.phone = request.form.get("new_value")
    db.session.commit()
    return redirect('/')

@app.route('/events/attendees/delete')
def find_event_attendees_erase():
    return render_template('select_event.html', data='/events/attendees/delete')

@app.route('/events/attendees/delete', methods=["POST"])
def find_event_attendees_to_erase():
    id = request.form.get("id")
    attendee_id = request.form.get("attendee_id")
    return redirect(url_for('erase_attendee', id=id, attendee_id=attendee_id))

@app.route('/events/<int:id>/attendees/<int:attendee_id>/delete', methods=["GET"])
def erase_attendee(id, attendee_id):
    # Deletes the data on the basis of unique id and
    # redirects to home page
    #attendee = Attendees.query.get_or_404(attendee_id)
    #event_id = attendee.event.id
    attendee = Attendees.query.filter_by(id=attendee_id).first()
    db.session.delete(attendee)
    db.session.commit()
    return redirect(url_for('all_attendees', event_id=id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

"""
a1 = Attendees(id=1, first_name="Sarah", last_name="Galenda", email='sgalenda@gmail.com', phone='07393906455')
a2 = Attendees(id=2, first_name="Sarah", last_name="Aisagbon", email='saisagbon@yahoo.com', phone='07393906456')
a3 = Attendees(id=3, first_name="Justin", last_name="Bieber", email='jbieber@gmail.com', phone='07757720249')
a4 = Attendees(id=4, first_name="Anita", last_name="Victor", email='avictor@yahoo.co.uk', phone='07523186400')
a5 = Attendees(id=5, first_name="Assana", last_name="Mahmoud", email='assana@gmail.com', phone='07986341975')
a6 = Attendees(id=6, first_name="Rachel", last_name="Smith", email='rachelsmith@yahoo.co.uk', phone='07747734509')

e1 = Events(id=1, name="Ben's Wedding", start_time='12:00', end_time='22:00',location="Royal Hospital Chelsea", budget=1000)
e2 = Events(id=2, name="Emily's Christening", start_time='10:00', end_time='16:00', location="St Pauls", budget=2500)
e3 = Events(id=3, name="Sarah's Birthday", start_time="14:00", end_time="23:00", location="LSO", budget=3000)
"""