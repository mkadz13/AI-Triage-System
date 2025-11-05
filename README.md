# Medical Triage System

A modern, AI-powered medical triage system built with React frontend and Flask backend. This system helps healthcare providers assess patient symptoms and prioritize care using advanced AI technology.

## Features

- **AI-Powered Triage**: Uses OpenAI GPT-4 for intelligent symptom assessment
- **Real-time Chat**: WebSocket-based patient-doctor communication
- **Priority Ranking**: Automatic urgency level assessment (Critical, High, Medium, Low)
- **Modern UI/UX**: Beautiful React frontend with Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices
- **Secure Authentication**: JWT-based doctor authentication
- **Real-time Updates**: Live patient queue updates for doctors

## Tech Stack

### Frontend
- React 18
- React Router for navigation
- Tailwind CSS for styling
- Lucide React for icons
- Socket.io client for real-time communication
- Axios for HTTP requests

### Backend
- Flask (Python)
- Flask-SocketIO for WebSocket support
- SQLAlchemy for database management
- SQLite database (can be upgraded to PostgreSQL)
- OpenAI GPT-4 API integration
- JWT authentication
- CORS support

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd TRIAGE
```

### 2. Backend Setup

#### Install Python dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the root directory (copy from `env_template.txt`):
```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

**⚠️ Security Note**: Never commit `.env` files to version control! The `.gitignore` file is configured to exclude sensitive files.

#### Initialize Database
```bash
python main.py
```
This will create the database and a default doctor account:
- Email: `doctor@example.com`
- Password: `doctor123`

### 3. Frontend Setup

#### Install Node.js dependencies
```bash
npm install
```

#### Start Development Server
```bash
npm start
```

The React app will run on `http://localhost:3000`

## Usage

### For Patients
1. Visit the homepage
2. Enter your name and age
3. Start the triage assessment
4. Answer AI-generated questions about your symptoms
5. Receive a priority ranking and summary

### For Doctors
1. Login with credentials:
   - Email: `doctor@example.com`
   - Password: `doctor123`
2. View the patient queue
3. See real-time patient updates
4. Review triage summaries and urgency levels
5. Prioritize patient care based on AI assessment

## API Endpoints

### Authentication
- `POST /api/auth/login` - Doctor login
- `GET /api/auth/me` - Get current user info

### Triage
- `POST /api/start_triage` - Start new triage session

### Doctor Dashboard
- `GET /api/doctor/patients` - Get patient queue

### WebSocket Events
- `patient_message` - Patient sends message
- `bot_response` - AI bot responds
- `new_patient` - New patient notification
- `join/leave` - Room management

## Project Structure

```
TRIAGE/
├── main.py                 # Flask backend
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
├── tailwind.config.js     # Tailwind CSS config
├── public/                # Static files
├── src/                   # React source code
│   ├── components/        # Reusable components
│   ├── contexts/          # React contexts
│   ├── pages/            # Page components
│   ├── App.js            # Main app component
│   └── index.js          # Entry point
├── templates/             # Old Flask templates (legacy)
├── static/                # Old Flask static files (legacy)
└── instance/              # Database files
```

## Development

### Running Both Servers

#### Terminal 1 - Backend
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run Flask server
python main.py
```

#### Terminal 2 - Frontend
```bash
npm start
```

### Building for Production
```bash
npm run build
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 access | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `JWT_SECRET` | JWT signing secret | Yes |

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_doctor`: Boolean flag
- `name`: User's full name

### Patients Table
- `id`: Primary key
- `name`: Patient's name
- `age`: Patient's age
- `created_at`: Timestamp
- `status`: Current status (waiting, in_progress, completed)
- `summary`: AI-generated triage summary
- `session_id`: Unique session identifier
- `triage_data`: JSON field for structured data
- `urgency_level`: Priority ranking

### Chat Messages Table
- `id`: Primary key
- `patient_id`: Foreign key to patients
- `message`: Message content
- `is_bot`: Boolean flag for bot messages
- `timestamp`: Message timestamp
- `message_type`: Type of message

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository.

## Security Notes

- This is a demonstration system and should not be used in production without proper security hardening
- API keys and secrets should be properly secured in production
- Consider implementing rate limiting and additional security measures
- Database should be properly secured and backed up
- HTTPS should be used in production

## Version Control / GitHub

### Before Pushing to GitHub

1. **Run the security check**:
   ```bash
   check_before_push.bat
   ```

2. **Verify sensitive files are excluded**:
   - `.env` file should NOT be in git status
   - `instance/triage.db` should NOT be in git status
   - `venv/` folder should NOT be in git status
   - `node_modules/` should NOT be in git status

3. **Never commit**:
   - API keys or secrets
   - Database files with real patient data
   - Environment files (`.env`)

See `GITHUB_SETUP.md` for detailed instructions on setting up your GitHub repository safely.

## Future Enhancements

- [ ] PostgreSQL database support
- [ ] Docker containerization
- [ ] AWS/GCP deployment guides
- [ ] Additional AI models
- [ ] Patient history tracking
- [ ] Integration with hospital systems
- [ ] Mobile app development
- [ ] Multi-language support
