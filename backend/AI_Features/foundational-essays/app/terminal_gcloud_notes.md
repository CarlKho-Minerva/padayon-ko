gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

docker build -t gcr.io/padayon-ko-gemini/scholarship-essay-helper .

gcloud auth configure-docker

docker push gcr.io/padayon-ko-gemini/scholarship-essay-helper

gcloud run deploy scholarship-essay-helper \
  --image gcr.io/padayon-ko-gemini/scholarship-essay-helper \
  --platform managed \
  --allow-unauthenticated \
