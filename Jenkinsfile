pipeline {
    agent none

    stages {

        stage('Checkout Code') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Run Tests') {
            agent {
                docker {
                    image 'python:3.10-slim'
                }
            }
            steps {
                sh '''
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                sh 'docker build -t aceest-fitness:v1 .'
            }
        }

        stage('Deploy Container') {
            agent any
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