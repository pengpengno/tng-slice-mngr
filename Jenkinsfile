pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Slice Manager') {
          steps {
            echo 'Building Slice Manager container'
            sh 'docker build -t registry.sonata-nfv.eu:5000/tng-slice-mngr .'
          }
        }
      }
    }
    stage('Unit Test Dependencies') {
      steps {
        echo 'If needed, add unit test dependencies in the future'
        sh 'sudo rm -rf unit_tests/spec || true'
      }
    }
    /*
    stage('Unit Test Execution'){
      parallel {
        stage('Performing NST Unit Tests') {
          steps {
            dir(path: 'unit_tests'){
              sh './nstapi.sh'
            }
          }
        }
        stage('Performing NSI Unit Tests') {
          steps {
            dir(path: 'unit_tests'){
              sh './nsiapi.sh'
            }
          }
        }
      }
    }
    */
    stage('Checkstyle') {
      parallel {
        stage('Slice Manager') {
          steps {
            sh 'echo TODO Checkstyle pep8'
          }
        }
      }
    }
    stage('Publish to :latest') {
      parallel {
        stage('Slice Manager') {
          steps {
            echo 'Publishing Slice Manager container'
            sh 'docker push registry.sonata-nfv.eu:5000/tng-slice-mngr'
          }
        }
      }
    }
    stage('Deploying in pre-integration ') {
      when{
        not{
          branch 'master'
        }        
      }      
      steps {
        sh 'rm -rf tng-devops || true'
        sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
        dir(path: 'tng-devops') {
          sh 'ansible-playbook roles/sp.yml -i environments -e "target=pre-int-sp component=slice-manager"'
        }
      }
    }
    stage('Publishing to :int') {
      when{
        branch 'master'
      }      
      parallel {
        stage('Slice Manager') {
          steps {
            echo 'Publishing Slice Manager container'
            sh 'docker tag registry.sonata-nfv.eu:5000/tng-slice-mngr:latest registry.sonata-nfv.eu:5000/tng-slice-mngr:int'
            sh 'docker push registry.sonata-nfv.eu:5000/tng-slice-mngr:int'
          }
        }
      }
    }
    stage('Deploying in integration') {
      when{
        branch 'master'
      }      
      steps {
        sh 'docker tag registry.sonata-nfv.eu:5000/tng-slice-mngr:latest registry.sonata-nfv.eu:5000/tng-slice-mngr:int'
        sh 'docker push registry.sonata-nfv.eu:5000/tng-slice-mngr:int'
        sh 'rm -rf tng-devops || true'
        sh 'git clone https://github.com/sonata-nfv/tng-devops.git'
        dir(path: 'tng-devops') {
          sh 'ansible-playbook roles/sp.yml -i environments -e "target=int-sp component=slice-manager"'
        }
      }
    }
    stage('Checking Swagger Documentation'){
      parallel {
        stage('NST_API swagger validation'){
          steps {
            sh 'swagger-cli validate doc/v1_1/slice-mngr_NST.json'
          }
        }
        stage('NSI_API swagger validation'){
          steps {
            sh 'swagger-cli validate doc/v1_1/slice-mngr_NSI.json'
          }
        }
      }
    }
    stage('Promoting release v5.0'){
      when{
        branch'v5.0'
      }stages{
        stage('Generating release'){
          steps{
            sh'docker tag registry.sonata-nfv.eu:5000/tng-slice-mngr:latest registry.sonata-nfv.eu:5000/tng-slice-mngr:v5.0'
            sh'docker tag registry.sonata-nfv.eu:5000/tng-slice-mngr:latest sonatanfv/tng-slice-mngr:v5.0'
            sh'docker push registry.sonata-nfv.eu:5000/tng-slice-mngr:v5.0'
            sh'docker push sonatanfv/tng-slice-mngr:v5.0'
          }
        }stage('Deploying in v5.0 servers'){
          steps{
            sh'rm -rf tng-devops || true'
            sh'git clone https://github.com/sonata-nfv/tng-devops.git'
            dir(path: 'tng-devops') {
              sh'ansible-playbook roles/vnv.yml -i environments -e "target=sta-sp-v5-0 component=slice-manager"'
            }
          }
        }
      }
    }
  }
  post {
    always {
      echo 'Clean Up'
      sh 'echo TODO Clean environment'
    }
    success {
      emailext (
        subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """<p>SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
          <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
      )
    }
    failure {
      emailext (
        subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
          <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
      )
    }  
  }
}
