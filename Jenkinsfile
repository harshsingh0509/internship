pipeline {
    agent any

    stages {
        stage('Run Python Script') {
            steps {
                script {
                    bat """
                    call venv\\Scripts\\activate || exit 1
                    python main.pyt || exit 1
                    """
                }
            }
        }
    }
}
