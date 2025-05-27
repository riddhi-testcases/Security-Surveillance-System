# Advanced Security Surveillance System

A modern web-based security system that uses facial recognition for personnel tracking and surveillance. This system provides real-time monitoring capabilities through a user-friendly web interface.

## Features

- Real-time Face Detection and Recognition
- Web-based Interface
- Personnel Registration System
- Location Tracking with Timestamps
- Live Video Feed
- Secure Database Storage
- Responsive Design

## Technical Stack

- Flask for the backend server
- OpenCV for video processing
- face_recognition library for facial detection
- SQLite for data storage
- Modern HTML5/CSS3 frontend
- Responsive web design

## Setup Instructions

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create required directories:
   ```bash
   mkdir -p static/uploads
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the web interface at `http://localhost:5000`

## System Components

### Backend (app.py)
- Flask server implementation
- Face recognition processing
- Database management
- API endpoints

### Frontend (templates/index.html)
- Responsive web interface
- Real-time video display
- Personnel registration form
- Tracking interface

### Database (security.db)
- SQLite database
- Personnel information storage
- Location tracking data
- Timestamp management

## Security Features

- Secure file upload handling
- Real-time personnel tracking
- Automated face recognition
- Timestamp-based monitoring