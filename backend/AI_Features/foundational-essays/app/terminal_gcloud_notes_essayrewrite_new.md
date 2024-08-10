cd to folder

gcloud builds submit --no-cache --tag gcr.io/padayon-ko-gemini/scholarship-essay-helper

gcloud run deploy scholarship-essay-helper `
--image gcr.io/padayon-ko-gemini/scholarship-essay-helper `
--platform managed `
--allow-unauthenticated
