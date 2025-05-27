from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATABASE'] = 'security.db'

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS personnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                photo_path TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

class SecurityCamera:
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.load_known_faces()
        
    def load_known_faces(self):
        with get_db() as conn:
            personnel = conn.execute('SELECT * FROM personnel').fetchall()
            for person in personnel:
                if os.path.exists(person['photo_path']):
                    image = face_recognition.load_image_file(person['photo_path'])
                    encoding = face_recognition.face_encodings(image)[0]
                    self.known_faces.append(encoding)
                    self.known_names.append(person['name'])

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_faces, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_names[first_match_index]
                
                with get_db() as conn:
                    conn.execute(
                        'UPDATE personnel SET last_seen = ? WHERE name = ?',
                        (datetime.now(), name)
                    )
            
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        
        return frame

camera = SecurityCamera()

def gen_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            processed_frame = camera.process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register', methods=['POST'])
def register_person():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo provided'}), 400
    
    photo = request.files['photo']
    name = request.form.get('name')
    position = request.form.get('position')
    
    if photo.filename == '':
        return jsonify({'error': 'No photo selected'}), 400
    
    filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(photo_path)
    
    with get_db() as conn:
        conn.execute(
            'INSERT INTO personnel (name, position, photo_path) VALUES (?, ?, ?)',
            (name, position, photo_path)
        )
    
    camera.load_known_faces()
    return jsonify({'message': 'Person registered successfully'})

@app.route('/personnel')
def get_personnel():
    with get_db() as conn:
        personnel = conn.execute('SELECT * FROM personnel').fetchall()
        return jsonify([dict(row) for row in personnel])

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True)