#!/bin/bash
# =============================================================
#  Finly — Cloud Run Job + Cloud Scheduler Setup
#  Runs queue_consumer.py on a cron schedule.
#
#  Flow:
#    Cloud Scheduler (every 5 min)
#         │
#         ▼
#    Cloud Run Job  (pulls Pub/Sub, runs AI, exits)
#         │
#         ▼
#    Firestore (saves analysis result)
# =============================================================

set -e

PROJECT_ID="massive-mantra-125114"  # Your GCP project ID
REGION="asia-south1"
REPO="finly"
JOB_NAME="finly-portfolio-worker"
SCHEDULER_JOB="finly-portfolio-scheduler"
CRON_SCHEDULE="*/5 * * * *"   # every 5 minutes — change as needed
VPC_CONNECTOR="finly-vpc-connector"

IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/job:latest"

gcloud config set project "$PROJECT_ID"

# ── 1. Enable required APIs ───────────────────────────────────
echo "⚙️  Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  artifactregistry.googleapis.com \
  --quiet

# ── 2. Build & push the job image ────────────────────────────
echo "🔨 Building job image..."
docker build -t "$IMAGE" -f Dockerfile.job .
docker push "$IMAGE"

# ── 3. Create or update the Cloud Run Job ────────────────────
echo "☁️  Deploying Cloud Run Job..."
gcloud run jobs create "$JOB_NAME" \
  --image "$IMAGE" \
  --region "$REGION" \
  --memory 2Gi \
  --cpu 2 \
  --task-timeout 300 \
  --max-retries 3 \
  --vpc-connector "$VPC_CONNECTOR" \
  --set-env-vars "PROJECT_ID=$PROJECT_ID" \
  --set-secrets "\
REDIS_HOST=finly-redis-host:latest,\
REDIS_PORT=finly-redis-port:latest,\
REDIS_DB=finly-redis-db:latest,\
FIREBASE_CERT_PATH=finly-firebase-cert-path:latest,\
FIREBASE_PROJECT_ID=finly-firebase-project-id:latest" \
  --quiet 2>/dev/null \
|| \
gcloud run jobs update "$JOB_NAME" \
  --image "$IMAGE" \
  --region "$REGION" \
  --memory 2Gi \
  --cpu 2 \
  --task-timeout 300 \
  --max-retries 3 \
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

# ── 4. Get the job resource name for Cloud Scheduler ─────────
JOB_URI="https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/$JOB_NAME:run"

# ── 5. Get or create a service account for the scheduler ─────
SA_EMAIL="finly-scheduler-sa@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create finly-scheduler-sa \
  --display-name "Finly Scheduler SA" \
  --quiet 2>/dev/null || echo "   Service account already exists, skipping."

# Grant permission to invoke Cloud Run Jobs
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member "serviceAccount:$SA_EMAIL" \
  --role "roles/run.invoker" \
  --quiet

# ── 6. Create or update Cloud Scheduler job ───────────────────
# echo "⏰ Setting up Cloud Scheduler (cron: $CRON_SCHEDULE)..."
# gcloud scheduler jobs create http "$SCHEDULER_JOB" \
#   --location "$REGION" \
#   --schedule "$CRON_SCHEDULE" \
#   --uri "$JOB_URI" \
#   --http-method POST \
#   --oauth-service-account-email "$SA_EMAIL" \
#   --time-zone "Asia/Kolkata" \
#   --quiet 2>/dev/null \
# || \
# gcloud scheduler jobs update http "$SCHEDULER_JOB" \
#   --location "$REGION" \
#   --schedule "$CRON_SCHEDULE" \
#   --uri "$JOB_URI" \
#   --http-method POST \
#   --oauth-service-account-email "$SA_EMAIL" \
#   --time-zone "Asia/Kolkata" \
#   --quiet

echo ""
echo "✅ Cloud Run Job + Scheduler ready!"
echo ""
echo "   Job name  : $JOB_NAME"
echo "   Schedule  : $CRON_SCHEDULE (Asia/Kolkata)"
echo ""
echo "   To run the job manually:"
echo "   gcloud run jobs execute $JOB_NAME --region $REGION"
echo ""
echo "   To check job logs:"
echo "   gcloud logging read 'resource.type=cloud_run_job' --limit 50 --format='table(timestamp, textPayload)'"