#!/bin/bash
# =============================================================
#  Finly — Credentials Setup Script
#  Creates all required secrets in Google Cloud Secret Manager
#  Production-ready: Handles existing secrets, validates input
# =============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── CONFIG ───────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-534974989580}"
REGION="${REGION:-asia-south1}"
# ─────────────────────────────────────────────────────────────

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

prompt_file() {
    local prompt_text=$1
    local file_path
    
    while true; do
        read -p "$prompt_text: " file_path
        
        if [ -z "$file_path" ]; then
            log_error "File path cannot be empty"
            continue
        fi
        
        if [ ! -f "$file_path" ]; then
            log_error "File not found: $file_path"
            continue
        fi
        
        echo "$file_path"
        break
    done
}

prompt_input() {
    local prompt_text=$1
    local input_value
    
    while true; do
        read -p "$prompt_text: " input_value
        
        if [ -z "$input_value" ]; then
            log_error "Input cannot be empty"
            continue
        fi
        
        echo "$input_value"
        break
    done
}

create_or_update_secret() {
    local secret_name=$1
    local secret_value=$2
    local secret_type=$3  # "file" or "text"
    
    log_info "Processing secret: $secret_name"
    
    # Check if secret exists
    if gcloud secrets describe "$secret_name" \
        --project="$PROJECT_ID" \
        --format="value(name)" &>/dev/null; then
        
        log_warning "Secret already exists: $secret_name"
        read -p "Update it? (y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if [ "$secret_type" = "file" ]; then
                gcloud secrets versions add "$secret_name" \
                    --data-file="$secret_value" \
                    --project="$PROJECT_ID" \
                    --quiet
            else
                echo "$secret_value" | gcloud secrets versions add "$secret_name" \
                    --data-file=- \
                    --project="$PROJECT_ID" \
                    --quiet
            fi
            log_success "Secret updated: $secret_name"
        else
            log_info "Skipped: $secret_name"
        fi
    else
        # Create new secret
        if [ "$secret_type" = "file" ]; then
            gcloud secrets create "$secret_name" \
                --data-file="$secret_value" \
                --project="$PROJECT_ID" \
                --replication-policy="automatic" \
                --quiet
        else
            echo "$secret_value" | gcloud secrets create "$secret_name" \
                --data-file=- \
                --project="$PROJECT_ID" \
                --replication-policy="automatic" \
                --quiet
        fi
        log_success "Secret created: $secret_name"
    fi
}

# ── MAIN SCRIPT ──────────────────────────────────────────────

echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔐 Finly Credentials Setup${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""
log_info "Project ID: $PROJECT_ID"
echo ""

# Enable Secret Manager API
log_info "Enabling Secret Manager API..."
gcloud services enable secretmanager.googleapis.com --quiet
log_success "Secret Manager API enabled"
echo ""

# ── 1. Firebase Certificate ──────────────────────────────────
echo -e "${BLUE}📋 Step 1/7: Firebase Certificate${NC}"
echo "Get your Firebase service account key:"
echo "  1. Go to Google Cloud Console"
echo "  2. Service Accounts → Choose firebase service account"
echo "  3. Keys tab → Create new key → JSON"
echo "  4. Save the downloaded file"
echo ""

firebase_cert_file=$(prompt_file "Enter path to Firebase JSON key file")
create_or_update_secret "finly-firebase-cert" "$firebase_cert_file" "file"
echo ""

# ── 2. Firebase Project ID ───────────────────────────────────
echo -e "${BLUE}📋 Step 2/7: Firebase Project ID${NC}"
echo "Your Firebase project ID (e.g., 'my-firebase-project')"
echo ""

firebase_project=$(prompt_input "Enter Firebase Project ID")
create_or_update_secret "finly-firebase-project-id" "$firebase_project" "text"
echo ""

# ── 3. Redis Host ────────────────────────────────────────────
echo -e "${BLUE}📋 Step 3/7: Redis Host${NC}"
echo "If using Google Memorystore for Redis:"
echo "  Go to Memorystore → Redis → Choose your instance"
echo "  Copy the 'Primary endpoint' (host part only)"
echo ""

redis_host=$(prompt_input "Enter Redis Host (e.g., '10.0.0.3')")
create_or_update_secret "finly-redis-host" "$redis_host" "text"
echo ""

# ── 4. Redis Port ────────────────────────────────────────────
echo -e "${BLUE}📋 Step 4/7: Redis Port${NC}"
echo "Usually 6379 for Memorystore"
echo ""

redis_port=$(prompt_input "Enter Redis Port (default: 6379)")
create_or_update_secret "finly-redis-port" "$redis_port" "text"
echo ""

# ── 5. Redis DB ──────────────────────────────────────────────
echo -e "${BLUE}📋 Step 5/7: Redis Database Number${NC}"
echo "Usually 0"
echo ""

redis_db=$(prompt_input "Enter Redis DB number (default: 0)")
create_or_update_secret "finly-redis-db" "$redis_db" "text"
echo ""

# ── 6. Kite API Key ──────────────────────────────────────────
echo -e "${BLUE}📋 Step 6/7: Kite Broker API Key${NC}"
echo "Get from your Kite broker API credentials"
echo ""

kite_key=$(prompt_input "Enter Kite API Key")
create_or_update_secret "finly-kite-api-key" "$kite_key" "text"
echo ""

# ── 7. Kite API Secret ───────────────────────────────────────
echo -e "${BLUE}📋 Step 7/7: Kite Broker API Secret${NC}"
echo "Get from your Kite broker API credentials"
echo ""

kite_secret=$(prompt_input "Enter Kite API Secret")
create_or_update_secret "finly-kite-api-secret" "$kite_secret" "text"
echo ""

# ── Verify all secrets ───────────────────────────────────────
log_info "Verifying all secrets..."
echo ""

secrets=(
    "finly-firebase-cert"
    "finly-firebase-project-id"
    "finly-redis-host"
    "finly-redis-port"
    "finly-redis-db"
    "finly-kite-api-key"
    "finly-kite-api-secret"
)

missing_secrets=0

for secret in "${secrets[@]}"; do
    if gcloud secrets describe "$secret" \
        --project="$PROJECT_ID" \
        --format="value(name)" &>/dev/null; then
        log_success "Secret exists: $secret"
    else
        log_error "Secret missing: $secret"
        missing_secrets=$((missing_secrets + 1))
    fi
done

echo ""

if [ $missing_secrets -eq 0 ]; then
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ All Credentials Configured!${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}📝 Next Steps:${NC}"
    echo "   bash deploy.sh"
    echo ""
else
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    log_error "Some secrets are missing"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    exit 1
fi