#!/bin/bash
# =============================================================
#  Finly — Deployment Script
#  Builds, pushes images, and deploys to Cloud Run
#  Production-ready: Handles all edge cases, idempotent
# =============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── CONFIG ───────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-massive-mantra-125114}"
REGION="${REGION:-asia-south1}"
REPO="${REPO:-finly}"
API_SERVICE="${API_SERVICE:-finly-api}"
WORKER_SERVICE="${WORKER_SERVICE:-finly-worker}"
SERVICE_ACCOUNT_NAME="${SERVICE_ACCOUNT_NAME:-finly-cloud-run}"
NETWORK="${NETWORK:-default}"
SUBNET="${SUBNET:-default}"
# ─────────────────────────────────────────────────────────────

IMAGE_BASE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO"
API_IMAGE="$IMAGE_BASE/api:latest"
WORKER_IMAGE="$IMAGE_BASE/worker:latest"
SERVICE_ACCOUNT="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_file() {
    if [ ! -f "$1" ]; then
        log_error "Required file not found: $1"
        echo "Please ensure you're running from the project root directory with Dockerfile and Dockerfile.worker"
        exit 1
    fi
}

check_secret() {
    local secret_name=$1
    if ! gcloud secrets describe "$secret_name" \
        --project="$PROJECT_ID" \
        --format="value(name)" &>/dev/null; then
        log_error "Secret not found: $secret_name"
        return 1
    fi
    return 0
}

# ── MAIN SCRIPT ──────────────────────────────────────────────

echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 Finly Cloud Run Deployment${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""
log_info "Project ID: $PROJECT_ID"
log_info "Region: $REGION"
log_info "Service Account: $SERVICE_ACCOUNT_NAME"
echo ""

# ── Step 1: Verify prerequisites ─────────────────────────────
log_info "Step 1/9: Verifying prerequisites..."

# Check Docker files
check_file "Dockerfile"
check_file "Dockerfile.worker"
log_success "Docker files found"

# Verify gcloud auth
CURRENT_USER=$(gcloud config get-value account 2>/dev/null)
if [ -z "$CURRENT_USER" ] || [ "$CURRENT_USER" = "None" ]; then
    log_error "Not authenticated with gcloud. Run: gcloud auth login"
    exit 1
fi
log_success "gcloud authenticated as: $CURRENT_USER"

# Verify project
gcloud config set project "$PROJECT_ID" --quiet
log_success "gcloud project set to: $PROJECT_ID"

# Check service account exists
if ! gcloud iam service-accounts describe "$SERVICE_ACCOUNT" \
    --project="$PROJECT_ID" &>/dev/null; then
    log_error "Service account does not exist: $SERVICE_ACCOUNT"
    log_info "Run: bash setup_infra.sh"
    exit 1
fi
log_success "Service account verified"

echo ""

# ── Step 2: Verify all secrets exist ─────────────────────────
log_info "Step 2/9: Verifying secrets..."

required_secrets=(
    "finly-firebase-cert"
    "finly-firebase-project-id"
    "finly-redis-host"
    "finly-redis-port"
    "finly-redis-db"
    "finly-kite-api-key"
    "finly-kite-api-secret"
)

secrets_missing=0
for secret in "${required_secrets[@]}"; do
    if check_secret "$secret"; then
        log_success "Secret found: $secret"
    else
        log_error "Secret not found: $secret"
        secrets_missing=$((secrets_missing + 1))
    fi
done

if [ $secrets_missing -gt 0 ]; then
    log_error "Missing $secrets_missing secret(s)"
    log_info "Run: bash setup_creds.sh"
    exit 1
fi

echo ""

# ── Step 3: Verify Artifact Registry ─────────────────────────
log_info "Step 3/9: Verifying Artifact Registry..."

if ! gcloud artifacts repositories describe "$REPO" \
    --location="$REGION" \
    --format="value(name)" &>/dev/null; then
    log_error "Artifact Registry repository not found: $REPO"
    log_info "Run: bash setup_infra.sh"
    exit 1
fi
log_success "Artifact Registry verified: $REPO"

echo ""

# ── Step 4: Configure Docker authentication ──────────────────
log_info "Step 4/9: Configuring Docker authentication..."

rm -f ~/.docker/config.json 2>/dev/null || true
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

mkdir -p ~/.docker
cat > ~/.docker/config.json << EOF
{
  "credHelpers": {
    "$REGION-docker.pkg.dev": "gcloud",
    "gcr.io": "gcloud"
  }
}
EOF

log_success "Docker authenticated"

echo ""

# ── Step 5: Build API image ──────────────────────────────────
log_info "Step 5/9: Building API image..."

if docker build -t "$API_IMAGE" -f Dockerfile .; then
    log_success "API image built: $API_IMAGE"
else
    log_error "Failed to build API image"
    exit 1
fi

echo ""

# ── Step 6: Push API image ───────────────────────────────────
log_info "Step 6/9: Pushing API image..."

if docker push "$API_IMAGE"; then
    log_success "API image pushed"
else
    log_error "Failed to push API image"
    log_info "Check Docker authentication: gcloud auth configure-docker $REGION-docker.pkg.dev --quiet"
    exit 1
fi

echo ""

# ── Step 7: Build Worker image ───────────────────────────────
log_info "Step 7/9: Building Worker image..."

if docker build -t "$WORKER_IMAGE" -f Dockerfile.worker .; then
    log_success "Worker image built: $WORKER_IMAGE"
else
    log_error "Failed to build Worker image"
    exit 1
fi

echo ""

# ── Step 8: Push Worker image ────────────────────────────────
log_info "Step 8/9: Pushing Worker image..."

if docker push "$WORKER_IMAGE"; then
    log_success "Worker image pushed"
else
    log_error "Failed to push Worker image"
    exit 1
fi

echo ""

# ── Step 9: Deploy services to Cloud Run ─────────────────────
log_info "Step 9/9: Deploying services to Cloud Run..."

# Deploy API Service
log_info "Deploying API service..."

gcloud run deploy "$API_SERVICE" \
    --image "$API_IMAGE" \
    --region "$REGION" \
    --service-account "$SERVICE_ACCOUNT" \
    --allow-unauthenticated \
    --port 8000 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --network "$NETWORK" \
    --subnet "$SUBNET" \
    --vpc-egress private-ranges-only \
    --set-env-vars "PROJECT_ID=$PROJECT_ID" \
    --set-secrets "\
FIREBASE_CERT=finly-firebase-cert:latest,\
FIREBASE_PROJECT_ID=finly-firebase-project-id:latest,\
REDIS_HOST=finly-redis-host:latest,\
REDIS_PORT=finly-redis-port:latest,\
REDIS_DB=finly-redis-db:latest,\
KITE_API_KEY=finly-kite-api-key:latest,\
KITE_API_SECRET=finly-kite-api-secret:latest" \
    --quiet

log_success "API service deployed: $API_SERVICE"

# Deploy Worker Service
log_info "Deploying Worker service..."

gcloud run deploy "$WORKER_SERVICE" \
    --image "$WORKER_IMAGE" \
    --region "$REGION" \
    --service-account "$SERVICE_ACCOUNT" \
    --no-allow-unauthenticated \
    --port 8000 \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 0 \
    --max-instances 5 \
    --network "$NETWORK" \
    --subnet "$SUBNET" \
    --vpc-egress private-ranges-only \
    --set-env-vars "PROJECT_ID=$PROJECT_ID" \
    --set-secrets "\
FIREBASE_CERT=finly-firebase-cert:latest,\
FIREBASE_PROJECT_ID=finly-firebase-project-id:latest,\
REDIS_HOST=finly-redis-host:latest,\
REDIS_PORT=finly-redis-port:latest,\
REDIS_DB=finly-redis-db:latest" \
    --quiet

log_success "Worker service deployed: $WORKER_SERVICE"

echo ""

# ── Display Deployment Summary ───────────────────────────────
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""

# Get service URLs
API_URL=$(gcloud run services describe "$API_SERVICE" \
    --region "$REGION" \
    --format "value(status.url)" 2>/dev/null || echo "Not available")

WORKER_URL=$(gcloud run services describe "$WORKER_SERVICE" \
    --region "$REGION" \
    --format "value(status.url)" 2>/dev/null || echo "Not available")

echo -e "${BLUE}🌐 Service URLs:${NC}"
echo "   API URL: $API_URL"
echo "   Worker URL: $WORKER_URL (internal only)"
echo ""

echo -e "${BLUE}📊 View Logs:${NC}"
echo "   API logs:"
echo "   gcloud run services logs read $API_SERVICE --region $REGION --limit 50"
echo ""
echo "   Worker logs:"
echo "   gcloud run services logs read $WORKER_SERVICE --region $REGION --limit 50"
echo ""

echo -e "${BLUE}🔍 Health Check:${NC}"
echo "   curl $API_URL/health"
echo ""

echo -e "${BLUE}💡 Redeploy (after code changes):${NC}"
echo "   bash deploy.sh"
echo ""

echo -e "${YELLOW}⚠️  Important:${NC}"
echo "   Check logs for: 'Firebase initialized successfully'"
echo "   If deployment fails, check:"
echo "   - All secrets exist: bash setup_creds.sh"
echo "   - Infrastructure ready: bash setup_infra.sh"
echo "   - Docker authentication: gcloud auth configure-docker $REGION-docker.pkg.dev --quiet"
echo ""

log_success "Deployment successful!"