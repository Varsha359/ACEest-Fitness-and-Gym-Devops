pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness:v1 .'
            }
        }

        stage('Run Container') {
           git  steps {
                sh '''
                docker stop aceest-container || true
                docker rm aceest-container || true
                docker run -d -p 5000:5000 --name aceest-container aceest-fitness:v1
                '''
            }
        }
    }
}