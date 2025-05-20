
# Flask Expert System Project

This is a Flask-based web application that includes an expert system component. It is designed to run with **Python 3.9.13**.

## 📁 Project Structure

```
├── app/                 # Main application package
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   ├── __init__.py      # Initializes the Flask app
│   ├── expert_system.py # Expert system logic
│   ├── models.py        # Data models
│   └── routes.py        # App routes
├── instance/            # Instance folder (e.g. config, local db)
├── run.py               # Entry point to run the Flask app
├── requirements.txt     # Python dependencies
├── runtime.txt          # Specifies Python runtime (Heroku, etc.)
└── .gitignore           # Files/folders to exclude from Git
```

## 🚀 Getting Started

### Prerequisites

- Python **3.9.13** (strictly required)
- Git (optional but recommended)
- A virtual environment tool like `venv`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hosana-/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker

   ```

2. **Set up a virtual environment**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access it**
   Open your browser and go to `http://127.0.0.1:5000`

## 🛠 Configuration

- Any secrets or environment-specific settings should be placed in the `instance/` folder (ignored by Git).
- You can use a `.env` file for environment variables (Flask secret key, DB credentials, etc.).

## 🧠 Expert System

The expert system logic resides in `app/expert_system.py`. It can be customized or extended to suit different knowledge domains.

## 📌 Notes

- Make sure to use **Python 3.9.13**. Other versions might not be compatible due to package dependencies.
- The app uses Flask, so it’s lightweight and easy to deploy (even on platforms like Heroku or Replit).

## 📤 License

This project is for academic purposes. You may share it or modify it, but please give appropriate credit.


