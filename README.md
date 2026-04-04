# ACEest Fitness & Gym Management App (Version 1.0)

## 📌 Overview

This project is a foundational web application built using Flask.
It is developed as part of a DevOps/Software Engineering assignment.

The application allows users to select a fitness program and view:

* Weekly workout plan
* Daily diet plan

This version focuses on migrating a desktop-based Tkinter application into a web-based architecture.

---

## 🚀 Features (Version 1.0)

* Program selection (Fat Loss, Muscle Gain, Beginner)
* Display workout plan
* Display diet plan
* Simple web interface using HTML
* Backend powered by Flask

---

## 🏗️ Architecture

Frontend:

* HTML (Jinja templates)
* Basic CSS

Backend:

* Flask (Python)

Flow:
User → HTML Form → Flask Route → Service Logic → HTML Response

---

## 📂 Project Structure

aceest-fitness/
│
├── app/
│   ├── **init**.py
│   ├── routes.py
│   ├── services.py
│   ├── templates/
│   └── static/
│
├── run.py
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Varsha359/ACEest-Fitness-and-Gym-Devops.git
cd ACEest-Fitness-and-Gym-Devops
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python run.py
```

5. Open in browser

```
http://127.0.0.1:5000
```

---

## 🔄 Version History

### v1.0

* Migrated Tkinter-based application to Flask
* Implemented program selection feature
* Displayed workout and diet plans using web interface
* No database integration (basic version)

---

## 🎯 Future Enhancements

* Add database integration
* User authentication (login/register)
* REST API endpoints
* Improved UI/UX
* Deployment using Docker and CI/CD

---

## 🧠 Key Learning

* Migration from desktop GUI (Tkinter) to web architecture
* Flask application structure
* Separation of concerns (routes, services, templates)
* Version control and commit strategy

---
