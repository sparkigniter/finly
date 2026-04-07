#!/bin/bash
# =============================================================
#  Finly — Infrastructure Setup Script
#  Sets up: GCP APIs, Service Account, IAM roles, VPC, etc.
#  Production-ready: Idempotent, handles all edge cases
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
SERVICE_ACCOUNT_NAME="${SERVICE_ACCOUNT_NAME:-finly-cloud-run}"
NETWORK="${NETWORK:-default}"
SUBNET="${SUBNET:-default}"
# ─────────────────────────────────────────────────────────────

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

# ── MAIN SCRIPT ──────────────────────────────────────────────

echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 Finly Infrastructure Setup${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""
log_info "Project ID: $PROJECT_ID"
log_info "Region: $REGION"
log_info "Service Account: $SERVICE_ACCOUNT_NAME"
echo ""

# ── 1. Set up gcloud config ──────────────────────────────────
log_info "Step 1/8: Configuring gcloud..."

gcloud config set project "$PROJECT_ID" --quiet
log_success "gcloud configured"

# ── 2. Enable required GCP APIs ──────────────────────────────
log_info "Step 2/8: Enabling GCP APIs..."

apis=(
    "run.googleapis.com"
    "artifactregistry.googleapis.com"
    "pubsub.googleapis.com"
    "firestore.googleapis.com"
    "redis.googleapis.com"
    "secretmanager.googleapis.com"
    "iam.googleapis.com"
    "compute.googleapis.com"
    "servicenetworking.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${apis[@]}"; do
    gcloud services enable "$api" --quiet 2>/dev/null || true
done

log_success "All GCP APIs enabled"

# ── 3. Create Artifact Registry repository ───────────────────
log_info "Step 3/8: Setting up Artifact Registry..."

if gcloud artifacts repositories describe "$REPO" \
    --location="$REGION" \
    --format="value(name)" &>/dev/null; then
    log_success "Repository already exists: $REPO"
else
    gcloud artifacts repositories create "$REPO" \
        --repository-format=docker \
        --location="$REGION" \
        --quiet
    log_success "Repository created: $REPO"
fi

# ── 4. Create service account ────────────────────────────────
log_info "Step 4/8: Setting up service account..."

if gcloud iam service-accounts describe "$SERVICE_ACCOUNT" \
    --format="value(email)" &>/dev/null; then
    log_success "Service account already exists: $SERVICE_ACCOUNT_NAME"
else
    gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
        --display-name="Finly Cloud Run Service Account" \
        --quiet
    log_success "Service account created: $SERVICE_ACCOUNT_NAME"
fi

# ── 5. Grant IAM roles to service account ────────────────────
log_info "Step 5/8: Granting IAM roles..."

roles=(
    "roles/secretmanager.secretAccessor"
    "roles/datastore.user"
    # RCA FIX: Pub/Sub Admin is needed to CREATE topics at runtime (Status 7 fix)
    "roles/pubsub.admin" 
    "roles/pubsub.publisher"
    "roles/pubsub.subscriber"
    # RCA FIX: Firebase Auth Admin is needed to verify ID tokens in auth.py
    "roles/firebaseauth.admin"
    "roles/iam.serviceAccountTokenCreator"
    "roles/logging.logWriter"
    "roles/monitoring.metricWriter"
)

for role in "${roles[@]}"; do
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:${SERVICE_ACCOUNT}" \
        --role="$role" \
        --quiet \
        --condition=None 2>/dev/null || true
done

log_success "All IAM roles granted"

# ── 6. Grant current user Artifact Registry permissions ───────
log_info "Step 6/8: Configuring local Docker push permissions..."

CURRENT_USER=$(gcloud config get-value account)

if [ -z "$CURRENT_USER" ] || [ "$CURRENT_USER" = "None" ]; then
    log_warning "Not authenticated with gcloud. Run: gcloud auth login"
else
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="user:${CURRENT_USER}" \
        --role="roles/artifactregistry.writer" \
        --quiet \
        --condition=None 2>/dev/null || true
    
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="user:${CURRENT_USER}" \
        --role="roles/artifactregistry.admin" \
        --quiet \
        --condition=None 2>/dev/null || true
    
    log_success "Local Docker push permissions configured for $CURRENT_USER"
fi

# ── 7. Configure Docker authentication ───────────────────────
log_info "Step 7/8: Configuring Docker authentication..."

# Remove stale credentials
rm -f ~/.docker/config.json 2>/dev/null || true

# Fresh Docker authentication
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

# Ensure docker config has credential helper
mkdir -p ~/.docker
cat > ~/.docker/config.json << EOF
{
  "credHelpers": {
    "$REGION-docker.pkg.dev": "gcloud",
    "gcr.io": "gcloud"
  }
}
EOF

log_success "Docker configured"

# ── 8. Verify setup ──────────────────────────────────────────
log_info "Step 8/8: Verifying infrastructure..."

# Check service account
if gcloud iam service-accounts describe "$SERVICE_ACCOUNT" \
    --format="value(email)" &>/dev/null; then
    log_success "Service account verified"
else
    log_error "Service account verification failed"
    exit 1
fi

# Check artifact registry
if gcloud artifacts repositories describe "$REPO" \
    --location="$REGION" &>/dev/null; then
    log_success "Artifact Registry verified"
else
    log_error "Artifact Registry verification failed"
    exit 1
fi

# ── Display Summary ──────────────────────────────────────────
echo ""
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Infrastructure Setup Complete!${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "   Project ID          : $PROJECT_ID"
echo "   Region              : $REGION"
echo "   Service Account     : $SERVICE_ACCOUNT_NAME"
echo "   Artifact Registry   : $REPO"
echo "   Docker Registry     : $REGION-docker.pkg.dev/$PROJECT_ID/$REPO"
echo ""

if [ -n "$CURRENT_USER" ] && [ "$CURRENT_USER" != "None" ]; then
    echo -e "${BLUE}🔑 Authentication:${NC}"
    echo "   User                : $CURRENT_USER"
    echo "   Authenticated       : ✅ Yes"
else
    echo -e "${YELLOW}⚠️  Authentication:${NC}"
    echo "   Please run: gcloud auth login"
fi

echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo "   1. Run: bash setup_creds.sh"
echo "   2. Then: bash deploy.sh"
echo ""
echo -e "${BLUE}💡 Environment Variables (optional):${NC}"
echo "   You can set these before running scripts:"
echo "   export PROJECT_ID=534974989580"
echo "   export REGION=asia-south1"
echo "   export REPO=finly"
echo ""

# Wait for IAM propagation
log_warning "IAM changes may take 30 seconds to propagate."
log_info "Waiting 30 seconds..."
sleep 30

log_success "Infrastructure setup complete!"