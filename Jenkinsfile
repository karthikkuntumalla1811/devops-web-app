
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'GitHub source code checkout'
                sh 'ls -la'
            }
        }

        stage('Build') {
            steps {
                echo 'Application build stage started'
                echo 'Build completed'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
