#!/usr/bin/env bash
set -euo pipefail

# Usage: ./deploy_minikube.sh [image-name:tag]
IMAGE=${1:-aceest-fitness-api:staging}

echo "Loading image into minikube: $IMAGE"
if command -v minikube >/dev/null 2>&1; then
  minikube image load "$IMAGE"
else
  echo "minikube not found. Ensure minikube is installed and running."
  exit 1
fi

echo "Applying Kubernetes manifests"
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment-bluegreen.yaml
kubectl apply -f k8s/deployment-canary.yaml
kubectl apply -f k8s/deployment-rolling.yaml
kubectl apply -f k8s/deployment-shadow.yaml
kubectl apply -f k8s/deployment-ab.yaml

echo "Done. Use kubectl get pods/services to inspect the cluster."
