cd to folder

gcloud config set builds/use_kaniko True

gcloud builds submit --no-cache --tag gcr.io/padayon-ko-gemini/math-socratic-practice

gcloud run deploy math-socratic-practice \
    --image gcr.io/padayon-ko-gemini/math-socratic-practice \
    --platform managed \
    --allow-unauthenticated
