#!/usr/bin/env bash
set -euo pipefail

DOCKER_USER=${1:-}
IMAGE_NAME=${2:-aceest-fitness-api}
TAG=${3:-staging}

if [ -z "$DOCKER_USER" ]; then
  echo "Usage: $0 <dockerhub-username> [image-name] [tag]"
  exit 1
fi

IMAGE="${DOCKER_USER}/${IMAGE_NAME}:${TAG}"

echo "Tagging local image as $IMAGE"
docker tag ${IMAGE_NAME}:staging "$IMAGE"

echo "Pushing $IMAGE"
docker push "$IMAGE"

echo "Done."
