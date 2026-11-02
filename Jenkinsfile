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
    }

    post {
        success {
            echo 'Docker image built successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}