pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests (Quality Gate)') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness:v1 .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                docker stop aceest-container || true
                docker rm aceest-container || true
                docker run -d -p 5000:5000 --name aceest-container aceest-fitness:v1
                '''
            }
        }
    }
}