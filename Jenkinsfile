pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Fillsogood/clova_tes.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t <container-registry>/clova-tes:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                sh 'docker push <container-registry>/clova-tes:latest'
            }
        }
        stage('Deploy with Helm') {
            steps {
                sh '''
                helm upgrade --install clova-tes ./charts/clova-tes \
                  --set image.repository=<container-registry>/clova-tes \
                  --set image.tag=latest
                '''
            }
        }
    }
}
