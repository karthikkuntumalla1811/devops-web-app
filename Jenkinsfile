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
                        credentialsId: 'k8s-token',
                        variable: 'K8S_TOKEN'
                    ),
                    file(
                        credentialsId: 'k8s-ca',
                        variable: 'K8S_CA_FILE'
                    )
                ]) {
                    sh '''
                        set +x
						TOKEN_HASH=$(printf '%s' "$K8S_TOKEN" | tr -d '[:space:]' | sha256sum | awk '{print $1}')

                         if [ "$TOKEN_HASH" = "c963d84897c9d315226a6a10911a5aba212bf1c25b563826363d415028d029a4" ]; then
                                 echo "Jenkins credential matches PowerShell token"
                          else
                                echo "Jenkins credential does NOT match PowerShell token"
                                exit 1
						fi

                        if [ -n "$K8S_TOKEN" ]; then
                            echo "Kubernetes token is loaded"
                        else
                            echo "Kubernetes token is missing"
                            exit 1
                        fi

                        kubectl \
                          --server=https://host.docker.internal:61178 \
                          --tls-server-name=localhost \
                          --certificate-authority="$K8S_CA_FILE" \
                          --token="$K8S_TOKEN" \
                          auth can-i create deployments -n devops-dev

                        kubectl \
                          --server=https://host.docker.internal:61178 \
                          --tls-server-name=localhost \
                          --certificate-authority="$K8S_CA_FILE" \
                          --token="$K8S_TOKEN" \
                          set image deployment/devops-web-app \
                          web-app=$IMAGE_NAME:$BUILD_NUMBER \
                          -n devops-dev

                        kubectl \
                          --server=https://host.docker.internal:61178 \
                          --tls-server-name=localhost \
                          --certificate-authority="$K8S_CA_FILE" \
                          --token="$K8S_TOKEN" \
                          rollout status deployment/devops-web-app \
                          -n devops-dev \
                          --timeout=300s
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