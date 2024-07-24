cd to folder

gcloud builds submit --tag gcr.io/padayon-ko-gemini/achievement-generator

gcloud run deploy achievement-generator \
--image gcr.io/padayon-ko-gemini/achievement-generator \
--platform managed \
--allow-unauthenticated
