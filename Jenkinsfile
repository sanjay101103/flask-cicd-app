pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        IMAGE_NAME = "sanjay101103/flask-cicd-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    
                    url: 'https://github.com/sanjay101103/flask-cicd-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh "echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy with Ansible') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig-cred',
                        variable: 'KUBECONFIG_FILE'
                    )
                ]) {
                    sh '''
                        sudo cp $KUBECONFIG_FILE /home/jenkins-kubeconfig
                        sudo chmod 644 /home/jenkins-kubeconfig

                        ansible-playbook \
                        -i ansible/inventory.ini \
                        ansible/deploy.yml \
                        --extra-vars \
                        "docker_image=${IMAGE_NAME}:${IMAGE_TAG} workspace_dir=${WORKSPACE}"
                    '''
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'sleep 10 && curl -f http://localhost:30080/health'
            }
        }
    }

    post {
        success {
            echo "Deployed ${IMAGE_NAME}:${IMAGE_TAG} successfully."
        }

        failure {
            echo "Pipeline failed — check console output."
        }
    }
}
