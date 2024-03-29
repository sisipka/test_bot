podTemplate(label: 'mypod', serviceAccount: 'jenkins', containers: [ 
    containerTemplate(
      name: 'docker', 
      image: 'docker', 
      command: 'cat', 
      resourceRequestCpu: '50m',
      resourceLimitCpu: '150m',
      resourceRequestMemory: '150Mi',
      resourceLimitMemory: '250Mi',
      ttyEnabled: true
    ),
    containerTemplate(
      name: 'kubectl', 
      image: 'amaceog/kubectl',
      resourceRequestCpu: '10m',
      resourceLimitCpu: '200m',
      resourceRequestMemory: '150Mi',
      resourceLimitMemory: '250Mi', 
      ttyEnabled: true, 
      command: 'cat'
    ),
    containerTemplate(
      name: 'helm', 
      image: 'alpine/helm:3.11.1', 
      resourceRequestCpu: '50m',
      resourceLimitCpu: '150m',
      resourceRequestMemory: '150Mi',
      resourceLimitMemory: '250Mi',
      ttyEnabled: true, 
      command: 'cat'
    ),
    containerTemplate(
      name: 'vault', 
      image: 'bedasoftware/ansible-vault', 
      resourceRequestCpu: '50m',
      resourceLimitCpu: '150m',
      resourceRequestMemory: '150Mi',
      resourceLimitMemory: '250Mi',
      ttyEnabled: true, 
      command: 'cat'
    )
  ],

  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    hostPathVolume(mountPath: '/usr/local/bin/helm', hostPath: '/usr/local/bin/helm')
  ]
  ) {
    node('mypod') {

        def REPOSITORY_URI = "sisipka/test_bot"
        def HELM_APP_NAME = "bot-app"
        def HELM_CHART_DIRECTORY = "helm_test_bot"

        stage('Get latest version of code') {

          checkout scm

        }

        stage('Check running containers') {

            container('docker') {  

                sh 'docker version'
                sh 'ls -la'
                sh 'cat requirements.txt'

            }
            container('kubectl') { 

                sh 'kubectl version'
                sh 'kubectl get pods -n jenkins'  

            }
            container('helm') { 

                sh 'helm list'
                sh 'helm version'  

            }

            container('vault') { 
              withCredentials([file(credentialsId: 'vault', variable: 'vault')]) {

                sh 'ansible-vault --version'
                sh 'cat bot/.env'
                sh "ansible-vault decrypt bot/.env --vault-password-file ${vault}"
                sh 'cat bot/.env'
              }
            }
        }  

        stage('Build Image'){
            container('docker'){

              withCredentials([usernamePassword(credentialsId: 'docker-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'), string(credentialsId: 'BOT_TOKEN', variable: 'SECRET')]) {

                sh 'cat bot/main.py'
                sh 'docker login --username="${USERNAME}" --password="${PASSWORD}"'
                sh "docker build -t ${REPOSITORY_URI}:${BUILD_NUMBER} ."
                sh 'docker image ls' 
              } 
                
            }
        } 

        stage('Testing') {
            container('docker') { 

              sh 'cat /etc/os-release'
              sh 'docker ps'
            }
        }

        stage('Push Image'){
            container('docker'){
              withCredentials([usernamePassword(credentialsId: 'docker-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {

                sh 'docker image ls'
                sh "docker push ${REPOSITORY_URI}:${BUILD_NUMBER}"
              }                 
            }
        } 
        
        stage('Deploy Image to k8s'){
            
            container('helm'){
        
              sh 'ls -l'
              sh 'helm list'
              sh "sed -i 's/xxx/${BUILD_NUMBER}/' ./helm_test_bot/values.yaml"
              sh 'cat ./helm_test_bot/values.yaml'
              sh "helm lint ./${HELM_CHART_DIRECTORY}"
              sh "helm upgrade -i -n jenkins ${HELM_APP_NAME} ./${HELM_CHART_DIRECTORY}"
              sh "helm list | grep ${HELM_APP_NAME}"
            }
              
         
            
        }      
        
    }
}
