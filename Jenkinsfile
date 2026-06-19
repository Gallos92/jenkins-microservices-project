pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = credentials('aws-account-id') + '.dkr.ecr.us-east-1.amazonaws.com'
        EKS_CLUSTER = 'jenkins-microservices-cluster'
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build API') {
            steps {
                script {
                    sh 'docker build -t api:${GIT_COMMIT_SHORT} api/'
                    sh 'docker tag api:${GIT_COMMIT_SHORT} ${ECR_REGISTRY}/api:${GIT_COMMIT_SHORT}'
                    sh 'docker tag api:${GIT_COMMIT_SHORT} ${ECR_REGISTRY}/api:latest'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                script {
                    sh 'docker build -t frontend:${GIT_COMMIT_SHORT} frontend/'
                    sh 'docker tag frontend:${GIT_COMMIT_SHORT} ${ECR_REGISTRY}/frontend:${GIT_COMMIT_SHORT}'
                    sh 'docker tag frontend:${GIT_COMMIT_SHORT} ${ECR_REGISTRY}/frontend:latest'
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}'
                    sh 'docker push ${ECR_REGISTRY}/api:${GIT_COMMIT_SHORT}'
                    sh 'docker push ${ECR_REGISTRY}/api:latest'
                    sh 'docker push ${ECR_REGISTRY}/frontend:${GIT_COMMIT_SHORT}'
                    sh 'docker push ${ECR_REGISTRY}/frontend:latest'
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    sh 'aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER}'
                    sh 'kubectl set image deployment/api api=${ECR_REGISTRY}/api:${GIT_COMMIT_SHORT}'
                    sh 'kubectl set image deployment/frontend frontend=${ECR_REGISTRY}/frontend:${GIT_COMMIT_SHORT}'
                    sh 'kubectl rollout status deployment/api'
                    sh 'kubectl rollout status deployment/frontend'
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
