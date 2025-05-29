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
                    bat """
                    if not exist venv (
                        echo Virtual environment not found. Creating venv...
                        python -m venv venv
                    )
                    call venv\\Scripts\\activate
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    bat """
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list | find "requests"
                    """
                }
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    bat """
                    call venv\\Scripts\\activate
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
