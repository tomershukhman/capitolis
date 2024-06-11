pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        DOCKER_REGISTRY = 'your-docker-registry-url'
        DOCKER_IMAGE = 'your-image-name'
    }
    stages {
        stage('Login to Docker Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'your-credentials-id', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login $DOCKER_REGISTRY -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${BUILD_NUMBER}"
                    sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${imageTag} ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    def imageTag = "${BUILD_NUMBER}"
                    sh """
                    docker tag ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${imageTag} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${imageTag}
                    docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${imageTag}
                    """
                }
            }
        }
    }
}
