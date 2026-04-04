pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness-api"
        IMAGE_TAG = "jenkins"
        STAGING_NAME = "aceest-staging-jenkins"
        STAGING_PORT = "5099"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate

                mkdir -p test-results allure-results

                pytest tests/ -v --tb=short \
                  --junitxml=test-results/junit.xml \
                  --alluredir=allure-results \
                  --html=test-results/pytest-report.html --self-contained-html

                PYEXIT=$?

                python scripts/build_test_dashboard.py || true

                exit $PYEXIT
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:staging
                '''
            }
        }

        stage('Staging Deploy + Health Check') {
            steps {
                sh '''
                docker rm -f $STAGING_NAME 2>/dev/null || true

                docker run -d \
                --name $STAGING_NAME \
                $IMAGE_NAME:staging

                echo "Waiting for app..."
                sleep 5

                i=1
                while [ $i -le 30 ]
                do
                RESPONSE=$(docker exec $STAGING_NAME curl -s http://localhost:5000/health || true)

                echo "Attempt $i: $RESPONSE"

                if echo "$RESPONSE" | grep -q ok; then
                    echo "Health check passed"
                    exit 0
                fi

                sleep 2
                i=$((i+1))
                done

                echo "Health check failed"
                docker logs $STAGING_NAME
                exit 1
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results/junit.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'test-results/*.html,allure-results/**/*', allowEmptyArchive: true
        }
    }
}