
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

                sh '''
                    docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                    docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest
                '''
            }
        }

        stage('Docker Hub Login and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x

                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        docker push $IMAGE_NAME:$BUILD_NUMBER
                        docker push $IMAGE_NAME:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'k8s-jenkins-token',
                        variable: 'K8S_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        set -eu

                        echo "Checking Kubernetes authentication..."

                        CAN_DEPLOY=$(kubectl \
                          --server=https://host.docker.internal:58351 \
                          --insecure-skip-tls-verify=true \
                          --token="$K8S_TOKEN" \
                          auth can-i create deployments -n devops-dev)

                        if [ "$CAN_DEPLOY" != "yes" ]; then
                            echo "Jenkins does not have deployment permissions"
                            exit 1
                        fi

                        echo "Kubernetes authentication successful"

                        echo "Updating application image..."

                        kubectl \
                          --server=https://host.docker.internal:58351 \
                          --insecure-skip-tls-verify=true \
                          --token="$K8S_TOKEN" \
                          set image deployment/devops-web-app \
                          web-app=$IMAGE_NAME:$BUILD_NUMBER \
                          -n devops-dev

                        echo "Waiting for Kubernetes rollout..."

                        kubectl \
                          --server=https://host.docker.internal:58351 \
                          --insecure-skip-tls-verify=true \
                          --token="$K8S_TOKEN" \
                          rollout status deployment/devops-web-app \
                          -n devops-dev \
                          --timeout=300s

                        echo "Kubernetes deployment successful"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image built, pushed and deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
