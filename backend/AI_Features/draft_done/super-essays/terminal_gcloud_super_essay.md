gcloud config set builds/use_kaniko True

gcloud builds submit --no-cache --tag gcr.io/padayon-ko-gemini/super-essay

gcloud run deploy super-essay \
    --image gcr.io/padayon-ko-gemini/super-essay \
    --platform managed \
    --allow-unauthenticated
