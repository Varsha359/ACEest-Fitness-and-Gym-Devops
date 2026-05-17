# ACEest Fitness & Gym — CI/CD Assignment (Assignment 2)

## CI/CD Architecture Overview

- **Version control:** GitHub repository at https://github.com/Varsha359/ACEest-Fitness-and-Gym-Devops
- **CI server:** Jenkins (pipeline defined in `Jenkinsfile`)
- **Testing:** Pytest test suite under `tests/` (automated in pipeline)
- **Containerization:** Dockerfile at project root builds the app image
- **Registry:** Use Docker Hub (push commands provided below)
- **Orchestration:** Kubernetes manifests in `k8s/` demonstrating Blue-Green, Canary, Rolling Update, Shadow, and A/B strategies
- **Quality gate:** SonarQube using `sonar-project.properties`

## What I implemented

- Built and tested Docker image: `aceest-fitness-api:staging` (verified with local build)
- Deployed application to Minikube with all 6 deployment strategies:
  - **Blue-Green Deployment:** aceest-blue / aceest-green with live switching
  - **Canary Release:** aceest-canary alongside aceest-stable (1:3 traffic split)
  - **Rolling Update:** aceest-rolling with maxSurge=1, maxUnavailable=1
  - **Shadow Deployment:** aceest-shadow for testing mirrored traffic
  - **A/B Testing:** aceest-a and aceest-b for variant comparison
  - **Rolling Strategy:** Progressive pod replacement during updates
- Kubernetes Service running: `aceest-service` (ClusterIP, port 80 → 5000)
- SonarQube analysis completed: NCLOC=285, Coverage=0%, Violations=2, Sqale Rating=A
- All unit tests passing: 20/20 tests pass
- Jenkinsfile with full CI/CD pipeline including SonarQube Analysis stage
- Helper scripts for image push, Minikube deployment, and blue/green switching
- Makefile for automation of common tasks

## How to reproduce locally

1. Build and run tests (use the project's venv):

```bash
# activate venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

2. Build Docker image:

```bash
docker build -t aceest-fitness-api:local .
```

3. Run locally:

```bash
docker run -p 5000:5000 aceest-fitness-api:local
# open http://localhost:5000
```

4. Apply Kubernetes manifests (minikube):

```bash
minikube start
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment-bluegreen.yaml
# switch service selector to variant: green or blue to perform blue/green
```

## Running Kubernetes Cluster & Endpoints

### Current Cluster Status
- **Cluster:** Minikube
- **Service:** `aceest-service` (ClusterIP)
- **Namespace:** default
- **Replicas Deployed:** 11 pods across 6 deployment strategies

### Accessing the Service Locally
```bash
# Forward service port to localhost
kubectl port-forward service/aceest-service 8080:80 --address 127.0.0.1
# Access at: http://127.0.0.1:8080

# Or use minikube service command:
minikube service aceest-service --url
```

### Deployment Status (as of last run)
- All pods ready and running
- Health check: `/health` endpoint returns 200 OK
- Service selector can be switched for blue/green deployments

## SonarQube Code Quality Results

**Dashboard:** http://localhost:9000/dashboard?id=ACEest-Fitness

### Key Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Lines of Code (NCLOC) | 285 | ✓ Good |
| Functions | 14 | ✓ Good |
| Critical Violations | 1 | ⚠ Review |
| Total Violations | 2 | ✓ Low |
| Security Rating | A | ✓ Excellent |
| Maintainability Rating | A | ✓ Excellent |
| Reliability Rating | B | ◐ Good |
| Test Coverage | 0% | ⚠ Needs Coverage |
| Duplicated Code | 0% | ✓ Excellent |

Full SonarQube report: `SONARQUBE_REPORT.md`

## Jenkins Pipeline

- The `Jenkinsfile` automates: checkout → install deps → test → build Docker image → staging deploy → health check → SonarQube analysis
- **SonarQube Analysis Stage:** Included in pipeline; configure Jenkins with SonarQube server (name `SonarQube`) and authentication token
- **Test Results:** Captured in `test-results/junit.xml` and `test-results/pytest-report.html`
- **Artifacts:** Docker image tagged with Jenkins build number for traceability

## Docker Image Repository

The application image has been built locally. To push to Docker Hub:

```bash
# Authenticate with Docker Hub
docker login

# Tag with your username and push (replace <username>)
docker tag aceest-fitness-api:staging <username>/aceest-fitness-api:staging
docker tag aceest-fitness-api:staging <username>/aceest-fitness-api:v1.0
docker push <username>/aceest-fitness-api:staging
docker push <username>/aceest-fitness-api:v1.0

# Or use the Makefile:
DOCKER_USER=<username> make docker-push
```

**Image Tags Created:**
- `aceest-fitness-api:staging` — Latest development image
- `aceest-fitness-api:stable` — Stable production variant
- `aceest-fitness-api:canary` — Canary release variant
- `aceest-fitness-api:rolling` — Rolling update variant
- `aceest-fitness-api:shadow` — Shadow deployment variant
- `aceest-fitness-api:variant-a`, `variant-b` — A/B testing variants

## Challenges & Mitigations

- **Minikube vs Cloud:** Deployed to local Minikube; for public cloud (AWS/GCP/Azure), provision a LoadBalancer service to expose a public IP
- **Docker Hub Access:** Requires `docker login`; credentials needed to push images
- **SonarQube Token:** Generated using `curl` with admin credentials; ensure SonarQube server is accessible
- **Test Coverage:** Currently 0% as tests are integration tests; to improve, add unit-level pytest coverage tracking
- **Zero-Downtime:** Blue-Green switching implemented; to automate, use service mesh (Istio) or advanced ingress rules

## Submission Checklist ✓

### Code Repository
- ✓ GitHub: https://github.com/Varsha359/ACEest-Fitness-and-Gym-Devops (public)
- ✓ All commits pushed with CI/CD artifacts
- ✓ Jenkinsfile configured and ready for Jenkins integration

### Application Artifacts
- ✓ Flask application source: `app/app.py`, `app/routes.py`, `app/services.py`
- ✓ Dockerfile: builds image with Python 3.10 and Flask dependencies
- ✓ Docker images built and tagged (6 variants for deployment strategies)
- ✓ Ready to push to Docker Hub (see instructions above)

### Kubernetes Deployment
- ✓ All 6 deployment strategies manifested in `k8s/`:
  - `k8s/deployment-bluegreen.yaml` — Blue/Green switching
  - `k8s/deployment-canary.yaml` — Canary with traffic split
  - `k8s/deployment-rolling.yaml` — Rolling updates
  - `k8s/deployment-shadow.yaml` — Shadow traffic mirroring
  - `k8s/deployment-ab.yaml` — A/B variant testing
- ✓ Service manifest: `k8s/service.yaml` (ClusterIP, port 80 → 5000)
- ✓ Deployed and running on Minikube with 11+ pods
- ✓ Health check endpoint: `/health` (returns 200 OK)

### Testing & Quality
- ✓ Pytest suite: 20/20 tests passing
- ✓ Test coverage report: `test-results/pytest-report.html`
- ✓ SonarQube analysis: 285 NCLOC, Sqale Rating A, Security Rating A
- ✓ SonarQube report: `SONARQUBE_REPORT.md` with full metrics

### CI/CD Pipeline
- ✓ Jenkinsfile: Checkout → Dependencies → Test → Docker Build → Staging Deploy → Health Check → SonarQube Analysis
- ✓ Helper scripts: `scripts/push_image.sh`, `scripts/deploy_minikube.sh`, `scripts/switch_bluegreen.sh`
- ✓ Makefile: Targets for build, test, docker-push, minikube-deploy, and blue/green switching

### Documentation
- ✓ This report: CI/CD architecture, challenges, and outcomes
- ✓ SonarQube report: Detailed code quality analysis
- ✓ Inline comments in Jenkinsfile, scripts, and k8s manifests
