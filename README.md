# Medical Triage System

An AI-powered medical triage system that helps healthcare providers assess patient symptoms and prioritize care. Built with React frontend and Flask backend, using OpenAI GPT-4 for intelligent symptom assessment.

## Features

- AI-powered symptom assessment using GPT-4
- Real-time patient-doctor communication via WebSocket
- Automatic priority ranking (Critical, High, Medium, Low)
- Modern, responsive UI built with React and Tailwind CSS
- Secure doctor authentication

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project>
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file with your API keys
   # OPENAI_API_KEY=your_key_here
   # SECRET_KEY=your_secret_here
   # JWT_SECRET=your_jwt_secret_here
   
   # Start backend
   python main.py
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000

## Usage

### For Patients
1. Visit the homepage
2. Enter your name and age
3. Start triage assessment
4. Answer AI-generated questions about your symptoms
5. Receive priority ranking and summary

### For Doctors
1. Login at `/login` with:
   - Email: `doctor@example.com`
   - Password: `doctor123`
2. View patient queue on dashboard
3. Review triage summaries and urgency levels
4. Prioritize care based on AI assessment

## Tech Stack

- **Frontend**: React, Tailwind CSS, Socket.io
- **Backend**: Python (Flask), SQLAlchemy, OpenAI GPT-4
- **Database**: SQLite
