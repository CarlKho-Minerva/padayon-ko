# First, ensure you're in the correct project

gcloud config set project padayon-ko-gemini

# Enable necessary APIs if not already enabled

gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build and deploy

gcloud builds submit --tag gcr.io/padayon-ko-gemini/super-essay

# Deploy to Cloud Run with environment variables

gcloud run deploy super-essay \
    --image gcr.io/padayon-ko-gemini/super-essay \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "NOTION_API_KEY=secret_HXtzwRwxLIsZhDXpLmqi7MR2RCAOAWSyMYZy4om1oef" \
    --set-env-vars "GEMINI_API_KEY=AIzaSyAG_a2dwMt2TYxpozHuIPHD_Y_ZLFRumaA"
