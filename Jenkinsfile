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
                        branch: 'develop',
                        credentialsId: 'tokenforjenkins'
            }

            post {
                success{
                    echo "Successfully cloned Repository"
                }

                always {
                    echo "I tried..."
                }

                cleanup {
                    echo "after all other post condition"
                }
                failure {
                    error 'This pipeline stops here...'
                }
            }

            
        }

        stage('Build') {
            agent any
            steps{
                echo 'build'

                dir('.'){
                    sh """
                    sudo docker build . -t grank-server
                    """
                }
            }

            post {
                success{
                    echo "Successfully cloned Repository"
                }

                always {
                    echo "I tried..."
                }

                cleanup {
                    echo "after all other post condition"
                }
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
                sudo docker stop -f $(docker ps -aq) || true && sudo docker rm -f $(docker ps -aq) || true
                sudo docker run -p 80:3052 -d grank-server
                '''
            }
            post {
                success{
                    echo "Successfully cloned Repository"
                }

                always {
                    echo "I tried..."
                }

                cleanup {
                    echo "after all other post condition"
                }
                failure {
                    error 'This pipeline stops here...'
                }
            }
        }
        
    }
}