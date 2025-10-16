# 🚀 Blockchain Chat Application

A secure, decentralized chat application built with Django, WebSockets, and Blockchain technology. Real-time messaging with encrypted PIN-protected rooms and immutable message history.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Deployment](#deployment)

---

## ✨ Features

- ✅ **Real-time Messaging** - WebSocket-based instant communication
- ✅ **Blockchain Integration** - Immutable message history with SHA256 hashing
- ✅ **PIN-Protected Rooms** - Create private chat rooms with password protection
- ✅ **User Authentication** - Secure login and registration system
- ✅ **Typing Indicators** - See when others are typing
- ✅ **File Sharing** - Upload and download files in chat rooms
- ✅ **Blockchain Explorer** - View all blockchain transactions
- ✅ **Notifications** - Get notified about room invitations
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **FontAwesome Icons** - Beautiful UI with modern icons

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 5.1 |
| **Real-time** | Django Channels 4.0+ |
| **WebSocket Server** | Daphne ASGI Server |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | Bootstrap 5, FontAwesome 6.4 |
| **Blockchain** | Custom Python implementation |
| **Language** | Python 3.8+ |

---

## 📦 System Requirements

```
- Python: 3.8 or higher
- Node.js: Optional (for frontend tooling)
- RAM: Minimum 2GB
- Storage: Minimum 500MB
- OS: macOS, Linux, or Windows with WSL2
```

---

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/blockchain-chat.git
cd Decentralized-Chat-APP
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Or manually install:**

```bash
pip install Django==5.1.7
pip install Pillow==10.0.0
pip install channels==4.0.0
pip install daphne==4.0.0
pip install python-dotenv==1.0.0
pip install asgiref==3.7.2
```

### Step 4: Create requirements.txt (if not exists)

```bash
cat > requirements.txt << 'EOF'
Django==5.1.7
Pillow==10.0.0
channels==4.0.0
daphne==4.0.0
python-dotenv==1.0.0
asgiref==3.7.2
EOF
```

---

## ⚙️ Configuration

### Step 1: Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

**Follow the prompts:**
```
Username: admin
Email: admin@example.com
Password: (enter secure password)
Password (again): (confirm password)
```

### Step 3: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 4: Update Settings (Optional)

Edit `blockchainchat/settings.py`:

**For Development:**
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

**For Production:**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-secure-secret-key'
```

---

## 🚀 Running the Application

### Option 1: Using Daphne (Recommended - With WebSockets)

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.\.venv\Scripts\activate  # Windows

# Run Daphne server
daphne -b 0.0.0.0 -p 8000 blockchainchat.asgi:application
```

Then visit: **http://localhost:8000**

✅ **This enables real-time chat and WebSockets**

### Option 2: Using Django Development Server

```bash
source .venv/bin/activate  # macOS/Linux
python manage.py runserver
```

Then visit: **http://localhost:8000**

⚠️ **Note:** Real-time features won't work without Daphne

### Option 3: Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn blockchainchat.wsgi:application --bind 0.0.0.0:8000
```

### Option 4: Using uWSGI (Production)

```bash
pip install uwsgi
uwsgi --http :8000 --wsgi-file blockchainchat/wsgi.py --master --processes 4 --threads 2
```

---

## 📖 Usage Guide

### 1️⃣ Register New User

1. Navigate to `http://localhost:8000/register/`
2. Enter username and password
3. Click "Create Account"
4. Redirects to login page

### 2️⃣ Login

1. Go to `http://localhost:8000/login/`
2. Enter your credentials
3. Click "Sign In"

### 3️⃣ Create a Chat Room

1. Go to Dashboard
2. Scroll to "Join or Create Room" section
3. Enter room name
4. Enter a PIN (password)
5. Click "Create / Join Room"

### 4️⃣ Send Messages

1. Enter the chat room
2. Type your message in the input box
3. Press Enter or click Send button
4. Message appears with blockchain hash

### 5️⃣ Invite Users to Room

1. Go to Dashboard
2. Find "Send Room PIN Notification"
3. Select room and user
4. Enter the room PIN
5. Click "Send Notification"

### 6️⃣ View Blockchain

1. Go to Dashboard
2. Click "Blockchain Explorer" in sidebar
3. View all transactions and blocks
4. Check block hashes and validation status

### 7️⃣ Upload Files

1. In chat room, click the attachment icon
2. Select a file
3. Click upload button
4. File appears in "Files" section

---

## 📁 Project Structure

```
Decentralized-Chat-APP/
│
├── blockchainchat/
│   ├── __init__.py
│   ├── asgi.py                 # ASGI config (WebSocket)
│   ├── wsgi.py                 # WSGI config (HTTP)
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   └── routing.py              # WebSocket routing
│
├── chatapp/
│   ├── migrations/             # Database migrations
│   ├── static/
│   │   └── css/
│   │       └── styles.css      # Main stylesheet
│   ├── templates/
│   │   └── chatapp/
│   │       ├── base1.html
│   │       ├── dashboard.html
│   │       ├── chat_room1.html
│   │       ├── login1.html
│   │       ├── register1.html
│   │       ├── upload_file.html
│   │       ├── list_files.html
│   │       └── blockchain_explorer.html
│   ├── admin.py                # Django admin config
│   ├── apps.py                 # App config
│   ├── blockchain.py           # Blockchain implementation
│   ├── consumers.py            # WebSocket consumers
│   ├── middleware.py           # Custom middleware
│   ├── models.py               # Database models
│   ├── routing.py              # WebSocket URL routing
│   ├── urls.py                 # App URL routing
│   ├── utils.py                # Utility functions
│   └── views.py                # View functions
│
├── manage.py                   # Django CLI
├── db.sqlite3                  # SQLite database
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔍 Troubleshooting

### ❌ WebSocket Connection Error

**Problem:** "WebSocket connection failed"

**Solution:**
```bash
# Make sure you're using Daphne, not runserver
daphne -b 0.0.0.0 -p 8000 blockchainchat.asgi:application

# Check if port is in use
# macOS/Linux:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000
```

---

### ❌ Database Migration Error

**Problem:** "No such table: chatapp_room"

**Solution:**
```bash
python manage.py migrate
python manage.py migrate chatapp
```

---

### ❌ Static Files Not Loading

**Problem:** CSS/JS/icons not appearing

**Solution:**
```bash
python manage.py collectstatic --noinput
```

Then add to `blockchainchat/settings.py`:
```python
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'chatapp', 'static')]
```

---

### ❌ FontAwesome Icons Not Showing

**Problem:** Icons appear as boxes or don't display

**Solution:**

Check `chatapp/templates/chatapp/base1.html` has this in `<head>`:

```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

---

### ❌ Port Already in Use

**Problem:** "Address already in use"

**Solution:**

```bash
# macOS/Linux - Kill process on port 8000
kill -9 $(lsof -t -i :8000)

# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port:
daphne -b 0.0.0.0 -p 8001 blockchainchat.asgi:application
```

---

### ❌ Permission Denied Error

**Problem:** "Permission denied: 'db.sqlite3'"

**Solution:**
```bash
# Fix permissions
chmod 644 db.sqlite3
chmod 755 .

# Or remove and recreate
rm db.sqlite3
python manage.py migrate
```

---

### ❌ Module Not Found

**Problem:** "ModuleNotFoundError: No module named 'channels'"

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

---

## 🔐 Security

### Generate New SECRET_KEY

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Production Checklist

```python
# blockchainchat/settings.py

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 🚢 Deployment

### Heroku Deployment

1. Create `Procfile`:
```
web: daphne -b 0.0.0.0 -p $PORT blockchainchat.asgi:application
worker: python manage.py runworker channel_layer
```

2. Create `runtime.txt`:
```
python-3.12.0
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku open
```

### AWS Deployment

Use Elastic Beanstalk:
```bash
eb init -p python-3.12 blockchain-chat
eb create blockchain-chat-env
eb deploy
eb open
```

---

## 🎯 Quick Start (One Command)

**Linux/macOS:**
```bash
git clone https://github.com/yourusername/blockchain-chat.git && \
cd Decentralized-Chat-APP && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
python manage.py migrate && \
echo "✅ Setup complete! Run: daphne -b 0.0.0.0 -p 8000 blockchainchat.asgi:application"
```

**Windows:**
```cmd
git clone https://github.com/yourusername/blockchain-chat.git
cd Decentralized-Chat-APP
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 blockchainchat.asgi:application
```

Then visit: **http://localhost:8000**

---

## 📚 API Endpoints

### Authentication
```
POST   /register/           Register new user
POST   /login/             Login user
GET    /logout/            Logout user
```

### Dashboard & Rooms
```
GET    /dashboard/                    View dashboard
GET    /dashboard/<room_name>/        Dashboard with room
POST   /send-pin-notification/        Send room PIN
```

### Chat
```
GET    /chat/<room_name>/             Enter chat room
POST   /save-message/...              Save message
POST   /clear/<room_name>/            Clear chat
POST   /upload/<room_name>/           Upload file
GET    /files/<room_name>/            List files
```

### Blockchain
```
GET    /blockchain/                   View blockchain explorer
POST   /blockchain/tamper/<index>/    Tamper demo
```

### WebSocket
```
ws/chat/<room_name>/     Real-time chat connection
```

---

## 📝 Default Test Credentials

After running migrations:

```
Admin Panel URL: http://localhost:8000/admin/
Username: admin
Password: (whatever you set during createsuperuser)
```

---

## 🐛 Debug Mode

**Enable detailed error messages:**

Add to `blockchainchat/settings.py`:
```python
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 📞 Support

**Check logs:**
```bash
python manage.py runserver --verbosity 3
```

**Clear cache:**
- Windows/Linux: `Ctrl+Shift+Del`
- macOS: `Cmd+Shift+Del`

**Restart after changes:**
```bash
# Stop server (Ctrl+C)
# Then restart
daphne -b 0.0.0.0 -p 8000 blockchainchat.asgi:application
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## ⭐ Version Info

```
Version: 1.0.0
Python: 3.8+
Django: 5.1.7
Channels: 4.0.0
Last Updated: October 2025
```

---

**Made with ❤️ for secure decentralized communication**
