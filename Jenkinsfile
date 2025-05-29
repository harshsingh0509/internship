pipeline {
    agent any

    environment {
        WORKSPACE = "${env.WORKSPACE}"
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    echo "Current workspace: ${WORKSPACE}"
                }
            }
        }

        stage('Initialize Virtual Environment') {
            steps {
                script {
                    sh """
                    if [ ! -d "venv" ]; then
                        echo "Virtual environment not found. Creating venv..."
                        python3 -m venv venv
                    fi
                    source venv/bin/activate
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh """
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list | grep requests
                    """
                }
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    sh """
                    source venv/bin/activate
                    python main.py
                    
                    """
                }
            }
        }
    }

    post {
        success {
            slackSend channel: '#build-notifications', message: "Build SUCCESSFUL: ${env.JOB_NAME} - ${env.BUILD_NUMBER} "
        }
        failure {
            slackSend channel: '#build-notifications', message: "Build FAILED: ${env.JOB_NAME} - ${env.BUILD_NUMBER} "
        }
    }
}