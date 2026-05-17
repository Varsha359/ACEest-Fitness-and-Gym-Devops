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

- Added Kubernetes manifests demonstrating multiple deployment strategies under `k8s/`.
- Added `sonar-project.properties` for SonarQube static analysis.
- Verified and ran unit tests with `pytest` (all tests pass).
- Confirmed `Dockerfile` builds image exposing port 5000.
- Prepared this short report and pointers to generate screenshots and pipeline runs.

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

## Jenkins pipeline

- The `Jenkinsfile` automates checkout, dependency install, test execution, artifact build, docker image build and a simple staging run+healthcheck.
- I added a `SonarQube Analysis` stage to the `Jenkinsfile`; configure the SonarQube server in Jenkins (named `SonarQube`) to enable scanning.

## Challenges & Mitigations

- Network/push limitations: Pushing images to Docker Hub and pushing commits to GitHub require user credentials — I prepared all files locally and added commands for pushing.
- Cluster endpoint: Exposing a public cluster endpoint requires cloud infra; instructions provided are for Minikube/local testing.

## Deliverables and Checklist

- Flask app source (in `app/` and `run.py`) — included
- Tests (`tests/`) — included and passing
- `Jenkinsfile` — included
- `Dockerfile` — included
- Kubernetes YAML manifests (`k8s/`) — included
- `sonar-project.properties` — included
- Short report — this file (REPORT.md)

## Next steps for submission

1. Commit changes and push to your GitHub repo:

```bash
git add .
git commit -m "Assignment 2: add k8s manifests, sonar config, report"
git push origin main
```

2. Build and push Docker images (example):

```bash
docker build -t <dockerhub-username>/aceest-fitness-api:staging .
docker push <dockerhub-username>/aceest-fitness-api:staging
```

3. Configure Jenkins job to run the `Jenkinsfile` from the repo. Configure credentials for Docker and SonarQube.

4. Capture screenshots of Jenkins successful runs, SonarQube report, Docker Hub repository, and Kubernetes deployments. Place screenshots under `screenshots/`.

---
_Prepared by Varsha. Add screenshots into `screenshots/` and then compress the repo for submission._
