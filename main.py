"""
This application is a simple web note taking application.
It allows you to create, edit, and delete notes.
Notes will have 
    - a title
    - description
    - date created
    - date modified
    - tags
    - a link to a web page
    - images
    - login is not required
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask import jsonify
# allow cross origin and same origin requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:james@localhost:5432/notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allow cross origin and same origin requests
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)
# CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(100))
    link = db.Column(db.String(100))
    image = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.title}'

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'tags': self.tags,
            'link': self.link,
            'image': self.image
        }

@app.route('/')
def index():
    #limit the number of notes to 2
    notes = Note.query.limit(2).all()
    return render_template('index.html', notes = notes)

@app.route('/notes')
def notes():
    notes = Note.query.all()
    # return json data of all notes
    return render_template('index.html', notes = notes)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        # get data from post request
        request_data = request.get_json()
        print(request_data)
        # print(request_data['title'])
        title = request_data['title']
        description = request_data['description']
        tags = request_data['tags']
        link = request_data['link']
        image = request_data['image']
        note = Note(title=title, description=description, tags=tags, link=link, image=image)
        db.session.add(note)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Note created successfully',
            'note': note.serialize()
        })

@app.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.description = request.form['description']
        note.tags = request.form['tags']
        note.link = request.form['link']
        note.image = request.form['image']
        note.date_modified = datetime.utcnow()
        db.session.commit()
        flash('Note updated successfully')
        return redirect(url_for('notes'))
    return render_template('edit_note.html', note=note)

@app.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully')
    return redirect(url_for('notes'))


# handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    pass

@app.errorhandler(400)
def bad_request(e):
    # print the error
    print(e)


if __name__ == '__main__':
    app.run(debug=True)
