cd to folder

gcloud builds submit --tag gcr.io/padayon-ko-gemini/origin-story-writer

gcloud run deploy origin-story-writer \
    --image gcr.io/padayon-ko-gemini/origin-story-writer \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY=""
