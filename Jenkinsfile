pipeline {
    agent {
        docker {
            image 'python:3.9'
            label 'docker'
        }
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install --user -r requirements.txt'
                // Adding the local bin directory to PATH
                sh 'export PATH=$HOME/.local/bin:$PATH'            }
        }
        stage('Test') {
            steps {
                sh 'pytest --junitxml=results.xml'
            }
        }
    }
    post {
        always {
            junit 'results.xml'
        }
    }
}
