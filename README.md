# Techtrends Web Apps
## Description
TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news 
within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new 
media articles and share them.

Imagine the following scenario: you joined a small team as a Platform Engineer. The team is composed of 2 developers, 
1 platform engineer (you), 1 project manager, and 1 manager. The team was assigned with the TechTrends project, aiming 
to build a fully functional online news sharing platform. The developers in the team are currently working on the first 
prototype of the TechTrends website. As a platform engineer, you should package and deploy TechTrends to Kubernetes 
using a CI/CD pipeline.

The web application is written using the Python Flask framework. It uses SQLite, a lightweight disk-based database to 
store the submitted articles.

# Deployment
## Local
Please refer `docker_commands`

## Continuous Delivery - Argo CD
### Step 1: Install lightweight version of Kubernetes, k3s.
```commandline
curl -sfL https://get.k3s.io | sh -
```

### Step 2: Deploy Argocd with Kubernetes
```commandline
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Create ArgoCD server Nodeport
```commandline
kubectl apply -f argocd-server-nodeport.yaml
```

Please refer the Argo server nodeport manifest at:
```commandline
https://github.com/udacity/nd064_course_1/blob/main/solutions/argocd/argocd-server-nodeport.yaml
```


### Step 4: Open Argo CD interface with a browser
#### 4.1 - Get ArgoCD credentials
```commandline
username: admin
```
```commandline
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

#### 4.2 - Access below address through a browser
```commandline
<YOUR_MACHINE_IP>:30008
```

### Step 5: Deploy techtrends web application, production and staging
```commandline
kubectl apply -f /argocd/helm-techtrends-prod.yaml

kubectl apply -f /argocd/helm-techtrends-staging.yaml
```