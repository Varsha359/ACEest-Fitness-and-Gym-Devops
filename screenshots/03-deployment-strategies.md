# Deployment Strategies Implementation

## Overview of 6 Deployment Strategies

### 1. Blue-Green Deployment
**Files:** `k8s/deployment-bluegreen.yaml`

**Description:** Run two identical production environments (blue and green). Switch traffic between them for zero-downtime deployments.

**Implementation:**
- Blue deployment: `aceest-blue` (2 replicas)
- Green deployment: `aceest-green` (2 replicas)
- Service selector switches between variants

**How to Switch:**
```bash
# Switch to green
kubectl patch service aceest-service -p '{"spec":{"selector":{"variant":"green"}}}'

# Switch back to blue
kubectl patch service aceest-service -p '{"spec":{"selector":{"variant":"blue"}}}'
```

**Use Case:** Stable production deployments; instant rollback capability

---

### 2. Canary Release
**Files:** `k8s/deployment-canary.yaml`

**Description:** Gradually roll out new version to a subset of users before full rollout.

**Implementation:**
- Stable deployment: `aceest-stable` (3 replicas) - 75% of traffic
- Canary deployment: `aceest-canary` (1 replica) - 25% of traffic
- Service mesh or ingress weighted routing for traffic split

**Traffic Distribution:**
- 75% to stable (tag: `stable`)
- 25% to canary (tag: `canary`)

**Use Case:** Testing new features with real traffic; early issue detection

---

### 3. Rolling Update
**Files:** `k8s/deployment-rolling.yaml`

**Description:** Gradually replace old pods with new pods, maintaining availability throughout.

**Implementation:**
- Deployment: `aceest-rolling` (3 replicas)
- Strategy: RollingUpdate
  - `maxSurge: 1` (1 extra pod during update)
  - `maxUnavailable: 1` (max 1 pod down during update)

**Update Flow:**
1. Start new pod (4 total momentarily)
2. Drain old pod
3. Repeat until all updated

**Use Case:** Standard Kubernetes deployments; least disruptive for stateless apps

---

### 4. Shadow Deployment
**Files:** `k8s/deployment-shadow.yaml`

**Description:** Send mirrored traffic to new version without affecting user experience. Monitor behavior before promoting.

**Implementation:**
- Shadow deployment: `aceest-shadow` (1 replica)
- Receives copy of production traffic via service mesh (Istio) or iptables mirroring
- No user traffic is affected; results not returned to users

**Requirements:**
- Istio service mesh or custom traffic mirroring (iptables/nginx)
- VirtualService with mirror destination

**Use Case:** Validate new version behavior in production without risk

---

### 5. A/B Testing
**Files:** `k8s/deployment-ab.yaml`

**Description:** Run two variants simultaneously and route traffic based on criteria (user ID, headers, etc.).

**Implementation:**
- Variant A deployment: `aceest-a` (2 replicas) - 50% of users
- Variant B deployment: `aceest-b` (2 replicas) - 50% of users
- Ingress or service mesh routes based on header, cookie, or user ID

**Routing Logic:**
- Route to A for users with `user_id % 2 == 0`
- Route to B for users with `user_id % 2 == 1`

**Use Case:** Feature experimentation; measuring user experience differences

---

### 6. Progressive/Rolling Deployment with Health Checks
**Integrated in all strategies**

**Description:** Kubernetes native approach combining rolling updates with readiness/liveness probes.

**Implementation:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 2
```

**Use Case:** Automatic recovery and traffic management

---

## Deployment Comparison Matrix

| Strategy | Downtime | Rollback | Complexity | Use Case |
|----------|----------|----------|------------|----------|
| **Blue-Green** | 0 | Instant (1 click) | Medium | Production critical |
| **Canary** | 0 | Instant | High | New features |
| **Rolling** | 0 | Gradual | Low | Standard upgrades |
| **Shadow** | 0 | N/A | High | Validation |
| **A/B Testing** | 0 | Instant | High | Experiments |
| **Progressive** | Minimal | Automatic | Medium | Daily operations |

---

## Managing Deployments

### View Current Status
```bash
# All pods
kubectl get pods -o wide

# Specific deployment
kubectl get deployment aceest-blue -o yaml

# Rollout history
kubectl rollout history deployment/aceest-blue
```

### Perform Blue-Green Switch
```bash
# Deploy green (new version)
kubectl apply -f k8s/deployment-bluegreen.yaml

# Wait for green pods ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/aceest-green

# Switch service to green
kubectl patch service aceest-service \
  -p '{"spec":{"selector":{"variant":"green"}}}'

# Test green
kubectl port-forward service/aceest-service 8080:80 &
curl http://localhost:8080/health
```

### Trigger Rolling Update
```bash
# Update image in deployment
kubectl set image deployment/aceest-rolling \
  aceest=aceest-fitness-api:v1.1

# Watch rollout
kubectl rollout status deployment/aceest-rolling

# If needed, rollback
kubectl rollout undo deployment/aceest-rolling
```

### Monitor Canary Deployment
```bash
# Check traffic distribution (requires Istio metrics)
kubectl logs -l app=aceest,track=canary -f

# Promote canary to stable
kubectl scale deployment aceest-canary --replicas=0
kubectl scale deployment aceest-stable --replicas=3
```

---

## Rollback Procedures

### Quick Rollback (Blue-Green)
```bash
# Simply switch service selector back
kubectl patch service aceest-service \
  -p '{"spec":{"selector":{"variant":"blue"}}}'
```

### Rolling Deployment Rollback
```bash
# Undo last update
kubectl rollout undo deployment/aceest-rolling

# Undo to specific revision
kubectl rollout undo deployment/aceest-rolling --to-revision=2
```

### A/B Testing Rollback
```bash
# Route all traffic back to variant A
kubectl patch virtualservice/aceest-ab \
  -p '[{"op":"replace","path":"/spec/hosts/0/http/0/match","value":[]}]'
```

---

## Configuration for Production Cloud Deployments

### AWS EKS
```bash
# Expose via LoadBalancer (creates ELB)
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: aceest-public
spec:
  type: LoadBalancer
  selector:
    app: aceest
  ports:
    - port: 80
      targetPort: 5000
EOF
```

### GCP GKE
```bash
# Use Ingress for external access
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: aceest-ingress
spec:
  rules:
    - host: aceest.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: aceest-service
                port:
                  number: 80
EOF
```

### Azure AKS
```bash
# Create public IP and ingress
az network public-ip create --resource-group myRG --name aceestIP
kubectl apply -f k8s/ingress-azure.yaml
```

---

**Summary:** All 6 deployment strategies are configured and ready to use. Start with blue-green for safe production deployments, then advance to canary for feature validation and A/B testing for experiments.
