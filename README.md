Here's the full corrected README — properly fenced code blocks, the two weak sections replaced, and the new Challenges & Fixes section added in the right spot (after Key Features, matching the pattern from DiackPain's README).

markdown
# Project 3: Jenkins CI/CD Pipeline + Microservices on EKS

A complete enterprise-grade CI/CD pipeline demonstrating declarative
Jenkins pipelines, multi-service microservices architecture, and
Kubernetes orchestration. From code push to live deployment in minutes.

## 🏗️ Architecture

GitHub (Code)
↓
GitHub Webhook
↓
Jenkins Pipeline (triggered)
├─ Build API Service
├─ Build Frontend Service
└─ Build PostgreSQL
↓
Docker Images → Amazon ECR
↓
kubectl Deploy to EKS
↓
Services Running on Kubernetes
├─ API (Flask) — ClusterIP
├─ Frontend (Nginx) — LoadBalancer
└─ PostgreSQL — ClusterIP


## Why I Built This

I'd already built CI/CD pipelines with GitHub Actions on earlier
projects and wanted hands-on depth with Jenkins specifically, since
it's still the incumbent CI tool at a lot of larger/regulated
organizations. This project was a chance to build a declarative
Jenkins pipeline from scratch — webhook trigger through multi-service
Docker builds to an automated EKS rollout — and compare that workflow
directly against the GitOps/ArgoCD approach used in my other projects.

## 📋 What's Included

### Services (3 Microservices)

**API Service** — Flask Python backend
- `/health` — Readiness probe
- `/api/data` — Data endpoint
- Connected to PostgreSQL

**Frontend Service** — Nginx static server
- Calls API from JavaScript
- Purple gradient UI
- LoadBalancer exposed

**Database Service** — PostgreSQL
- Initialized with admin credentials
- Isolated in private cluster network

### CI/CD Pipeline (Jenkins)
- Declarative Jenkinsfile — All stages defined in code
- Multi-stage build — API and Frontend built in parallel
- ECR push — Tagged images stored in private registry
- Kubernetes deployment — Automatic rollout to EKS
- Rollout verification — Waits for healthy pods

### Kubernetes Infrastructure
- EKS Cluster — Managed Kubernetes
- Deployments — 2 replicas per service (high availability)
- Services — Networking between pods
- Load Balancer — Public access to frontend
- Health Checks — Readiness probes ensure traffic only to ready pods

## 🎯 Key Features

- ✅ Declarative CI/CD — Jenkins pipeline as code (version controlled)
- ✅ Multi-Service — Demonstrates real-world microservices
- ✅ Automated Deployment — Push → Build → Deploy in ~5 minutes
- ✅ GitHub Webhook — Triggered automatically on every push
- ✅ High Availability — 2 replicas per service
- ✅ Docker Containers — Reproducible builds, portable across environments
- ✅ Kubernetes Orchestration — Auto-scaling, self-healing
- ✅ Public Endpoint — LoadBalancer provides external access

## Challenges & Fixes

- **Jenkins failed to start on initial EC2 setup** — traced to a Java
  version mismatch; Jenkins required Java 21 but the instance had
  Java 17 (Amazon Corretto) installed. Resolved by upgrading to
  Corretto 21 and reconfiguring the Jenkins service to point at the
  correct `JAVA_HOME`.

## 🚀 Quick Start

### Prerequisites

```bash
# AWS Account
aws sts get-caller-identity

# kubectl
kubectl version --client

# eksctl
eksctl version

# Docker (optional, for local testing)
docker --version

# GitHub account
git --version
```

### Deploy

**Step 1: Create EKS Cluster**

```bash
eksctl create cluster \
  --name jenkins-microservices-cluster \
  --region us-east-1 \
  --nodegroup-name workers \
  --node-type t3.small \
  --nodes 2 \
  --managed
```

**Step 2: Apply Kubernetes Manifests**

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

**Step 3: Set Up Jenkins**

- Launch EC2 t3.medium (Amazon Linux 2023)
- Install Java 21, Jenkins, Docker, kubectl
- Configure AWS credentials
- Create GitHub webhook

**Step 4: Trigger Build**

- Jenkins detects GitHub push
- Pipeline builds API + Frontend
- Pushes to ECR
- Deploys to EKS
- Frontend appears at LoadBalancer URL

### Verify

```bash
# Check all pods running
kubectl get pods

# Get LoadBalancer URL
kubectl get svc frontend

# Open in browser
# http://EXTERNAL-IP
```

## 📊 NIST 800-53 Controls (Simplified Compliance)

| Control | Implementation |
|---|---|
| CM-3 (Change Control) | Jenkinsfile version controlled |
| CM-2 (Baseline Config) | k8s manifests as source of truth |
| AU-2 (Audit Trail) | Jenkins console logs all builds |
| SI-2 (Flaw Remediation) | Automated image pushes, updates |
| SC-3 (Access Enforcement) | Kubernetes RBAC (minimal shown) |

## 💰 Cost Estimate

| Resource | Cost |
|---|---|
| EKS Cluster | ~$73/month |
| 2x t3.small nodes | ~$15/month |
| EBS volumes (2x 20GB) | ~$3/month |
| NAT Gateway | $32/month |
| Jenkins EC2 t3.medium | ~$30/month |
| **Total** | **~$150/month (if left running)** |

Save costs — delete when done:

```bash
eksctl delete cluster --name jenkins-microservices-cluster --region us-east-1
# Terminate Jenkins EC2
```

## 🛠️ How It Works

**1. Developer Pushes Code**

```bash
git commit -m "Update API message"
git push origin main
```

**2. GitHub Webhook Triggers Jenkins**

GitHub sends a POST to `http://JENKINS_IP:8080/github-webhook/`.
Jenkins detects the change in the `main` branch.

**3. Jenkins Pipeline Runs**

```groovy
pipeline {
    stages {
        stage('Checkout') { /* Pull from GitHub */ }
        stage('Build API') { /* docker build api/ */ }
        stage('Build Frontend') { /* docker build frontend/ */ }
        stage('Push to ECR') { /* aws ecr push */ }
        stage('Deploy to EKS') { /* kubectl set image */ }
    }
}
```

**4. Docker Images Built**
- API: Flask app on port 5000
- Frontend: Nginx on port 80
- Tagged with git commit SHA for traceability

**5. Pushed to ECR**

Private registry stores images with automatic versioning.

**6. Deployed to EKS**
- `kubectl set image` updates deployment
- Kubernetes pulls new image from ECR
- Old pods terminated, new pods created
- Health checks verify readiness

**7. App is Live**

Frontend LoadBalancer URL accessible worldwide.

## 📁 Project Structure

jenkins-microservices-project/
├── api/
│ ├── app.py # Flask backend
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # Container definition
├── frontend/
│ ├── index.html # HTML page
│ ├── style.css # Styling (purple gradient)
│ ├── script.js # Calls /api/data
│ └── Dockerfile # Nginx container
├── k8s/
│ ├── api-deployment.yaml
│ ├── api-service.yaml
│ ├── frontend-deployment.yaml
│ ├── frontend-service.yaml
│ ├── postgres-deployment.yaml
│ └── postgres-service.yaml
├── Jenkinsfile # CI/CD pipeline definition
├── .github/
│ └── workflows/ # GitHub Actions (optional)
└── README.md


## 🔐 Security & Best Practices

- Declarative Pipeline — Jenkins pipeline as code
- Private Registry — ECR for image storage
- Least Privilege — Services only access needed resources
- Health Checks — Readiness probes on all services
- Horizontal Scaling — 2 replicas for redundancy
- Immutable Images — SHA-tagged for reproducibility
- Secret Management — K8s secrets for credentials (shown simplified)

## 🐛 Troubleshooting

**Pods not starting**
```bash
kubectl describe pod -l app=api
kubectl logs -l app=api
```

**Jenkins can't reach EKS**
```bash
# Verify kubectl works on Jenkins EC2
sudo -u jenkins kubectl get nodes
```

**Frontend shows blank page**
```bash
# Check API is reachable
kubectl get svc api
# Update frontend/script.js with correct API URL
```

**GitHub webhook not triggering**
```bash
# Verify webhook in GitHub repo settings
# Check Jenkins: Manage Jenkins → System → GitHub Webhook
# Ensure Jenkins IP is accessible from GitHub
```

## 📖 References

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)

## 📝 License

MIT License - See LICENSE file for details

## 👤 Author

Gallo — DevOps Engineer
GitHub: [@Gallos92](https://github.com/Gallos92)

Questions? Open an issue or reach out!
