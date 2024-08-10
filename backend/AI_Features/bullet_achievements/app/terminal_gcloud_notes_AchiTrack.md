cd backend\AI_Features\bullet_achievements\app

gcloud builds submit --no-cache --tag gcr.io/padayon-ko-gemini/achievement-generator

gcloud run deploy achievement-generator `
--image gcr.io/padayon-ko-gemini/achievement-generator `
--platform managed `
--allow-unauthenticated
