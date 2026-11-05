pipeline {
  agent any

  environment {
    ENV = 'test'
    PYTHONUNBUFFERED = '1'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup') {
      steps {
        sh '''
          python -m venv .venv || true
          . .venv/bin/activate
          pip install -U pip
          pip install -r requirements.txt
          playwright install --with-deps chromium
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p reports/allure-results
          pytest -m "api or ui" --alluredir=reports/allure-results --clean-alluredir
        '''
      }
    }

    stage('Allure Report') {
      steps {
        sh '''
          if command -v allure >/dev/null 2>&1; then
            allure generate reports/allure-results -o reports/allure-report --clean
          else
            echo "allure CLI not found; raw results kept in reports/allure-results"
          fi
        '''
        allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
      }
    }

    stage('Notify') {
      steps {
        sh '''
          . .venv/bin/activate
          python -c "from report_ci.notify.webhook import send_webhook; send_webhook('PyTestFramework', 'Jenkins pipeline finished')"
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
    }
  }
}
