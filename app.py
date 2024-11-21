from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configurar la URI de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/agenda_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo para la tabla 'contacts'
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    events = db.relationship('Event', backref='contact', lazy=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

# Modelo para la tabla 'events'
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    event_title = db.Column(db.String(255))
    event_date = db.Column(db.Date)
    event_time = db.Column(db.Time)

    def __repr__(self):
        return f'<Event {self.event_title}>'

# Ruta principal para mostrar los contactos
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# Ruta para agregar un nuevo contacto
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        new_contact = Contact(name=name, phone=phone, email=email)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_contact.html')

# Ruta para editar un contacto
@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contact)

# Ruta para eliminar un contacto
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para agregar un evento
@app.route('/add_event/<int:contact_id>', methods=['GET', 'POST'])
def add_event(contact_id):
    contact = Contact.query.get(contact_id)
    if request.method == 'POST':
        event_title = request.form['event_title']
        event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
        event_time = datetime.strptime(request.form['event_time'], '%H:%M').time()
        new_event = Event(event_title=event_title, event_date=event_date, event_time=event_time, contact_id=contact.id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html', contact=contact)

# Ruta para ver los eventos de un contacto
@app.route('/events/<int:contact_id>')
def view_events(contact_id):
    contact = Contact.query.get(contact_id)
    events = Event.query.filter_by(contact_id=contact_id).all()
    return render_template('events.html', contact=contact, events=events)

if __name__ == '__main__':
    app.run(debug=True)
