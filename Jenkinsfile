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

              withCredentials([string(credentialsId: 'vault', variable: 'SECRET')]) {

                sh 'hostname'
                sh 'hostname -i'
                sh 'ls -la'
                sh 'cat requirements.txt'
                sh 'cat bot/.env'
                sh "ansible-vault decrypt --vault-id=${SECRET} bot/.env"
                sh 'cat bot/.env'
            }
            container('kubectl') { 
                sh 'kubectl version'
                sh 'kubectl get pods -n jenkins'  
            }
            container('helm') { 
                sh 'helm list'
                sh 'helm version'     
            }
        }  

        stage('Build Image'){
            container('docker'){

              withCredentials([usernamePassword(credentialsId: 'docker-login', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'), string(credentialsId: 'BOT_TOKEN', variable: 'SECRET')]) {

                sh "echo 'SECRET=${SECRET}'>test"
                sh "echo 'USER=${USERNAME}'>>test"
                sh 'cat test'
                sh "sed -i 's/BOT_TOKEN/"${SECRET}"/' bot.py"
                sh 'cat bot.py'
                sh 'docker login --username="${USERNAME}" --password="${PASSWORD}"'
                sh "docker build -t ${REPOSITORY_URI}:${BUILD_NUMBER} ."
                sh 'docker image ls' 
              } 
                
            }
        } 

        stage('Testing') {
            container('docker') { 

              sh 'whoami'
              sh 'cat /etc/os-release'
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
