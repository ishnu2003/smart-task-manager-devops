pipeline {
    agent any

    environment {
        STAGING_IMAGE = "smart-task-manager:staging"
        PRODUCTION_IMAGE = "smart-task-manager:production"
        STAGING_PORT = "5000"
        PRODUCTION_PORT = "5050"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build Stage: Creating Docker image for the Flask API...'
                sh 'docker build -t ${STAGING_IMAGE} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Test Stage: Running automated pytest test suite...'
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && pytest tests/ -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Code Quality Stage: Running flake8 and pylint...'
                sh '. venv/bin/activate && flake8 app tests --max-line-length=120'
                sh '. venv/bin/activate && pylint app --exit-zero > pylint-report.txt'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pylint-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Security') {
            steps {
                echo 'Security Stage: Running Bandit and pip-audit scans...'
                sh '. venv/bin/activate && bandit -r app -f txt -o bandit-report.txt || true'
                sh '. venv/bin/activate && pip-audit -r requirements.txt > pip-audit-report.txt || true'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.txt,pip-audit-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy Stage: Deploying application to staging environment...'
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
                sh 'sleep 10'
                sh 'curl -f http://localhost:${STAGING_PORT}/health'
            }
        }

        stage('Release') {
            steps {
                echo 'Release Stage: Promoting staging image to production environment...'
                sh 'docker tag ${STAGING_IMAGE} ${PRODUCTION_IMAGE}'
                sh 'docker compose -f docker-compose.prod.yml down || true'
                sh 'docker compose -f docker-compose.prod.yml up -d'
                sh 'sleep 10'
                sh 'curl -f http://localhost:${PRODUCTION_PORT}/health'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Monitoring Stage: Starting Prometheus and Grafana...'
                sh 'docker compose -f docker-compose.monitoring.yml down || true'
                sh 'docker compose -f docker-compose.monitoring.yml up -d'
                sh 'sleep 15'
                sh 'curl -f http://localhost:9090/-/ready'
                sh 'curl -f http://localhost:${PRODUCTION_PORT}/metrics'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. All 7 stages passed.'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output for details.'
        }

        always {
            echo 'Cleaning temporary Python cache files...'
            sh 'find . -type d -name "__pycache__" -exec rm -rf {} + || true'
            sh 'find . -type d -name ".pytest_cache" -exec rm -rf {} + || true'
        }
    }
}
