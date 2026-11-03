
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mokshaskanda1410/devops-web-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'

                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
                sh 'docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities'

                sh '''
                    docker save $IMAGE_NAME:$BUILD_NUMBER -o image.tar
                '''

                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/work" \
                      aquasec/trivy:latest image \
                      --timeout 15m \
                      --input /work/image.tar \
                      --scanners vuln \
                      --severity HIGH,CRITICAL \
                      --exit-code 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Docker image built and scanned successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
