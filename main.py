from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json
import secrets
import jwt
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///triage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_doctor = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='waiting')  # waiting, in_progress, completed
    summary = db.Column(db.Text)
    session_id = db.Column(db.String(100), unique=True)
    triage_data = db.Column(db.JSON)
    urgency_level = db.Column(db.String(20))

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_bot = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='chat')  # chat, question, answer

# Triage questions and flow
TRIAGE_QUESTIONS = [
    {
        "id": "chief_complaint",
        "question": "What is your main reason for seeking medical attention today?",
        "type": "text"
    },
    {
        "id": "pain_level",
        "question": "On a scale of 1-10, how would you rate your pain/discomfort?",
        "type": "number",
        "validation": {"min": 1, "max": 10}
    },
    {
        "id": "symptom_onset",
        "question": "When did your symptoms begin?",
        "type": "text"
    },
    {
        "id": "medical_history",
        "question": "Do you have any relevant medical history or conditions?",
        "type": "text"
    },
    {
        "id": "medications",
        "question": "Are you currently taking any medications?",
        "type": "text"
    }
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# JWT Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# API Routes
@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'API is working!', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/start_triage', methods=['POST'])
def start_triage():
    print(f"Received triage request: {request.get_json()}")
    
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    print(f"Extracted data - name: {name}, age: {age}")

    if not name or not age:
        print("Missing name or age")
        return jsonify({'error': 'Name and age are required'}), 400

    try:
        # Create new patient and session
        session_id = secrets.token_urlsafe(32)
        patient = Patient(
            name=name,
            age=age,
            session_id=session_id,
            status='in_progress',
            triage_data={}
        )
        db.session.add(patient)
        db.session.commit()
        
        print(f"Created patient with session_id: {session_id}")
        
        return jsonify({
            'session_id': session_id,
            'patient_id': patient.id,
            'message': 'Triage session started successfully'
        })
    except Exception as e:
        print(f"Error creating patient: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = jwt.encode(
            {'user_id': user.id, 'email': user.email, 'is_doctor': user.is_doctor},
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_doctor': user.is_doctor
            }
        })
    
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_user_info(current_user):
    return jsonify({
        'user': {
            'id': current_user.id,
            'email': current_user.email,
            'name': current_user.name,
            'is_doctor': current_user.is_doctor
        }
    })

@app.route('/api/doctor/patients', methods=['GET'])
@token_required
def get_patients(current_user):
    if not current_user.is_doctor:
        return jsonify({'error': 'Unauthorized'}), 403

    patients = Patient.query.filter(
        Patient.status.in_(['waiting', 'in_progress'])
    ).order_by(Patient.created_at.desc()).all()

    patient_list = []
    for patient in patients:
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'created_at': patient.created_at.isoformat(),
            'status': patient.status,
            'summary': patient.summary,
            'session_id': patient.session_id,
            'urgency_level': patient.urgency_level
        }
        patient_list.append(patient_data)

    return jsonify({'patients': patient_list})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        print(f'Client joined room: {room}')

@socketio.on('leave')
def handle_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        print(f'Client left room: {room}')

@socketio.on('patient_message')
def handle_patient_message(data):
    session_id = data.get('session_id')
    message = data.get('message')

    if not session_id or not message:
        return

    patient = Patient.query.filter_by(session_id=session_id).first()
    if not patient:
        return

    # Save patient message
    chat_message = ChatMessage(
        patient_id=patient.id,
        message=message,
        is_bot=False
    )
    db.session.add(chat_message)
    db.session.commit()

    # Process message and get bot response
    bot_response = get_bot_response(message, patient)

    # Save bot response
    bot_message = ChatMessage(
        patient_id=patient.id,
        message=bot_response['message'],
        is_bot=True,
        message_type=bot_response['type']
    )
    db.session.add(bot_message)

    # Update patient triage data if applicable
    if bot_response.get('triage_data'):
        if patient.triage_data is None:
            patient.triage_data = {}
        patient.triage_data.update(bot_response['triage_data'])

    if bot_response.get('triage_complete'):
        patient.status = 'waiting'
        generate_and_save_summary(patient)
        emit('new_patient', {'patient_id': patient.id}, room='doctors')

    db.session.commit()

    # Send response back to patient
    emit('bot_response', {
        'message': bot_response['message'],
        'type': bot_response['type']
    }, room=f"patient_{session_id}")

def get_bot_response(message, patient):
    # Get current triage step from patient data
    triage_data = patient.triage_data or {}
    current_step = len(triage_data)

    # If we've completed all structured questions, use OpenAI for follow-up
    if current_step >= len(TRIAGE_QUESTIONS):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical triage assistant. Ask relevant follow-up questions based on the patient's responses. Focus on gathering important medical information."},
                    {"role": "user", "content": message}
                ]
            )
            return {
                'message': response.choices[0].message.content,
                'type': 'chat'
            }
        except Exception as e:
            app.logger.error(f"OpenAI API error: {str(e)}")
            return {
                'message': "I'm sorry, I'm having trouble processing your response. Please try again.",
                'type': 'error'
            }

    # Handle structured triage questions
    current_question = TRIAGE_QUESTIONS[current_step]
    
    # Store the answer in triage data
    triage_data[current_question['id']] = message
    patient.triage_data = triage_data

    return {
        'message': current_question['question'],
        'type': 'question',
        'triage_data': {current_question['id']: message}
    }

def generate_and_save_summary(patient):
    try:
        # Combine all patient messages and triage data
        messages = ChatMessage.query.filter_by(patient_id=patient.id).order_by(ChatMessage.timestamp).all()
        message_history = "\n".join([f"{'Bot' if msg.is_bot else 'Patient'}: {msg.message}" for msg in messages])

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate a concise medical triage summary from the following conversation. Include chief complaint, severity, key symptoms, and recommended urgency level (Low, Medium, High, Critical)."},
                {"role": "user", "content": f"Patient Info:\nName: {patient.name}\nAge: {patient.age}\n\nConversation:\n{message_history}"}
            ]
        )

        summary = response.choices[0].message.content

        # Extract urgency level from summary
        urgency_levels = ['Critical', 'High', 'Medium', 'Low']
        patient.urgency_level = next((level for level in urgency_levels if level.lower() in summary.lower()), 'Medium')
        patient.summary = summary
        db.session.commit()

    except Exception as e:
        app.logger.error(f"Error generating summary: {str(e)}")
        patient.summary = "Error generating summary. Please review chat history."
        patient.urgency_level = 'Medium'
        db.session.commit()

def create_default_doctor():
    with app.app_context():
        # Check if doctor already exists
        doctor = User.query.filter_by(email='doctor@example.com').first()
        if not doctor:
            doctor = User(
                email='doctor@example.com',
                name='Doctor',
                is_doctor=True
            )
            doctor.set_password('doctor123')  # Set default password
            db.session.add(doctor)
            db.session.commit()
            print("Default doctor account created!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_doctor()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)
