# 🏋️ ACEest Fitness & Gym - Full Stack DevOps System

![Build Status](https://github.com/Varsha359/ACEest-Fitness-and-Gym-Devops/actions/workflows/main.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

> A production-ready fitness management platform built with Flask, featuring analytics, authentication, and a complete CI/CD pipeline with Docker and GitHub Actions.

---

## 📋 Table of Contents

* [Project Overview](#-project-overview)
* [Architecture](#-architecture)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Local Development Setup](#-local-development-setup)
* [Running the Application](#-running-the-application)
* [Docker Deployment](#-docker-deployment)
* [CI/CD Pipeline](#-cicd-pipeline)
* [Git Workflow](#-git-workflow)
* [Rollback Strategy](#-rollback-strategy)
* [Troubleshooting](#-troubleshooting)
* [Future Enhancements](#-future-enhancements)

---

## 🎯 Project Overview

**ACEest Fitness System** is a full-stack fitness management platform that evolved across multiple versions, demonstrating real-world software engineering and DevOps practices.

This project showcases:

* ✅ End-to-end application development (UI + backend)
* ✅ Progressive feature evolution (v1 → v3)
* ✅ Database-driven architecture
* ✅ Analytics and visualization
* ✅ CI/CD automation with GitHub Actions
* ✅ Containerized deployment using Docker
* ✅ Version control with rollback capability

---

## 🏗️ Architecture

### System Flow

```
User → Flask Web App → Services Layer → SQLite DB
                      ↓
                 Matplotlib (Charts)
                      ↓
                 HTML UI (Jinja)
```

---

### Project Structure

```bash
aceest-devops/
├── app/
│   ├── __init__.py        # App factory
│   ├── routes.py          # Routes / Controllers
│   ├── services.py        # Business logic + DB
│   ├── templates/         # HTML UI
│   └── static/            # CSS
├── tests/                 # Unit tests
├── run.py                 # Entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Features

### 🔹 Core Features

* Client management (Add / Load)
* Calorie calculation based on fitness programs
* Weekly adherence tracking

### 🔹 Advanced Features

* 📊 Progress analytics (charts using matplotlib)
* 🗄️ SQLite database persistence
* 🏋️ Workout tracking
* 📄 PDF report generation
* 💳 Membership management

### 🔹 System Features

* 🔐 Login system (Admin access)
* 🎯 Role-based functionality
* ⚙️ CI/CD pipeline integration
* 🐳 Docker containerization
* 🔁 Version-based rollback strategy

---

## 🛠️ Tech Stack

| Layer            | Technology                   |
| ---------------- | ---------------------------- |
| Backend          | Flask (Python)               |
| Database         | SQLite                       |
| Frontend         | HTML + CSS (Jinja templates) |
| Analytics        | Matplotlib (Agg backend)     |
| PDF              | FPDF                         |
| CI/CD            | GitHub Actions               |
| Containerization | Docker                       |

---

## ⚙️ Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/Varsha359/ACEest-Fitness-and-Gym-Devops.git
cd ACEest-Fitness-and-Gym-Devops
```

---

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python run.py
```

Open in browser:

```
http://localhost:5001
```

---

## 🔐 Login Credentials

```text
Username: admin
Password: admin
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t aceest-fitness:v3.2.4 .
```

---

### Run Container

```bash
docker run -p 5001:5001 aceest-fitness:v3.2.4
```

---

## ⚙️ CI/CD Pipeline

Implemented using **GitHub Actions**:

### Pipeline Stages:

* ✅ Install dependencies
* ✅ Run tests (pytest)
* ✅ Generate reports
* ✅ Build Docker image
* ✅ Tag versioned images

---

### Trigger Pipeline

```bash
git tag v3.2.4
git push origin v3.2.4
```

---

## 🔁 Rollback Strategy

Each version is tagged and stored as a Docker image:

```bash
aceest-fitness:v1.0
aceest-fitness:v2.2.1
aceest-fitness:v3.2.4
```

### Rollback Example

```bash
docker run aceest-fitness:v2.2.1
```

---

## 🌿 Git Workflow

```bash
feature → develop → main → tag release
```

### Example

```bash
git checkout -b feature/v3-final
git commit -m "feat: add analytics and dashboard"
git push origin feature/v3-final
```

---

## 🐛 Troubleshooting

### Port already in use

```bash
lsof -i :5001
kill -9 <PID>
```

---

### Docker issues

```bash
docker system prune -a
```

---

### Matplotlib error (Mac fix)

```python
import matplotlib
matplotlib.use('Agg')
```

---

## 🚀 Future Enhancements

* REST APIs for frontend/mobile
* Deployment on AWS / Render
* Role-based dashboards (Trainer / Client)
* Real-time analytics
* Notification system

---

## 🧠 Key Learnings

* Full-stack system design
* DevOps lifecycle implementation
* CI/CD pipeline automation
* Containerized deployments
* Versioning & rollback strategies

---

## 👩‍💻 Author

**Varsha Gajula**
MTech Software Engineering
Backend + DevOps Enthusiast
2024tm93599

---

## ⭐ Final Note

This project demonstrates **industry-level practices** including:

* Scalable architecture
* Clean code separation
* Automated pipelines
* Real-world deployment strategies
