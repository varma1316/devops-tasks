pipeline {
    agent none   

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-creds')
        DOCKER_IMAGE = "varma8k8k/subhadrafoods"
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            agent { docker { image 'alpine/git:latest' } }   
            steps {
                git branch: 'main', url: 'https://github.com/varma1316/Subhadrafoods.git'
            }
        }

        stage('Build') {
            agent { docker { image 'maven:3.9.4-eclipse-temurin-17' } }
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Test') {
            agent { docker { image 'maven:3.9.4-eclipse-temurin-17' } }
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Lint') {
            agent { docker { image 'node:18-alpine' } }
            steps {
                sh 'npm install eslint'
                sh 'npx eslint . || true'   
            }
        }

        stage('Docker Build') {
            agent { docker { image 'docker:20.10.24-dind-rootless' } }
            steps {
                sh """
                    docker build -t $DOCKER_IMAGE:$APP_VERSION .
                    docker tag $DOCKER_IMAGE:$APP_VERSION $DOCKER_IMAGE:latest
                """
            }
        }

        stage('Docker Push') {
            agent { docker { image 'docker:20.10.24-dind-rootless' } }
            steps {
                sh """
                    echo "$DOCKER_HUB_CREDENTIALS_PSW" | docker login -u "$DOCKER_HUB_CREDENTIALS_USR" --password-stdin
                    docker push $DOCKER_IMAGE:$APP_VERSION
                    docker push $DOCKER_IMAGE:latest
                """
            }
        }

        stage('Deploy') {
            agent { docker { image 'bitnami/kubectl:1.28' } }
            steps {
                sh 'echo "Deploying $DOCKER_IMAGE:$APP_VERSION to Kubernetes cluster..."'
                sh 'kubectl apply -f k8s/deployment.yaml'
            }
        }
    }

    post {
        success {
            echo "Subhadrafoods pipeline finished successfully!"
        }
        failure {
            echo " Subhadrafoods pipeline failed. Check logs."
        }
    }
}
