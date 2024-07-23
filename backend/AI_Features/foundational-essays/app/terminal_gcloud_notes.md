
gcloud builds submit --tag gcr.io/padayon-ko-gemini/scholarship-essay-helper
gcloud run deploy scholarship-essay-helper \
  --image gcr.io/padayon-ko-gemini/scholarship-essay-helper \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-api-key-here
