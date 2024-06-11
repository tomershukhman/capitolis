pipeline {
    agent {
        docker { label 'docker'}
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}