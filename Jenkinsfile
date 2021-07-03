pipeline {
    agent any

    triggers {
        pollSCM('*/3 * * * *')
    }

    environment {
        AWS_ACCESS_KEY_ID = credentials('awsAccessKeyId')
        AWS_SECRET_ACCESS_KEY = credentials('awsSecretAccessKey')
        AWS_DEAFAULT_REGION = 'ap-northeast-2'
    }

    stages {
        stage('Prepare'){
            agent any

            steps {
                echo "Clonning Repository"

                git url: 'https://github.com/When-You-Come-Merona-Dev/GRank-Server.git',
                        branch: 'master',
                        credentialsId: 'tokenforjenkins'
            }

            post {
                echo "Successfully cloned Repository"
            }

            always {
                echo "I tried..."
            }

            cleanup {
                echo "after all other post condition"
            }
        }

        stage('Test'){
            agent {
                docker {
                    image 'python:3.7'
                }
            }
            steps {
                echo 'Test'

                dir ('.'){
                    sh '''
                    PYTHONPATH=. pytest
                    '''
                }
            }
        }

        stage('Build') {
            agent any
            steps{
                echo 'build'

                dir('.'){
                    sh """
                    docker build . -t grank-server
                    """
                }
            }

            post {
                failure {
                    error 'This pipeline stops here...'
                }
            }
        }

        stage('Deploy') {
            agent any

            steps {
                echo 'Stop and Remove existed container'
                sh '''
                docker stop -f $(docker ps -aq) || true && sudo docker rm -f $(docker ps -aq) || true
                docker run -p 80:3052 -d grank-server
                '''
            }
        }
        
    }
}