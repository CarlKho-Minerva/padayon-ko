cd to folder

gcloud config set builds/use_kaniko True

gcloud builds submit --no-cache --tag gcr.io/padayon-ko-gemini/fluent-verbal-practice

gcloud run deploy fluent-verbal-practice \
    --image gcr.io/padayon-ko-gemini/fluent-verbal-practice \
    --platform managed \
    --allow-unauthenticated
