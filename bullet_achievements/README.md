# Achievement Resume Bullet Point Generator

A Flask-based web application using Google's Gemini AI to generate professional resume bullet points and detailed descriptions from achievement inputs, with real-time processing indicators and Cloud Run deployment support.

## Features

- Real-time processing status indicators
- Automatic input cleaning and formatting
- Support for non-English inputs
- Mobile-responsive design
- Google Cloud Run ready
- Service account authentication for Gemini API
- Fallback to API key authentication
- Debug logging system

## Prerequisites

- Python 3.9+
- Google Cloud account
- Gemini API access
- Docker (for containerization)
- Google Cloud CLI

## Tech Stack

- Python 3.9
- Flask 2.0.1
- Google Gemini AI
- Docker
- Google Cloud Run
- Gunicorn

## Project Structure

```
bullet_achievements/
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── clean_input.py
│   ├── extract_info.py
│   ├── generate_content.py
│   ├── main.py
│   ├── refine_output.py
│   ├── structure_achievement.py
│   ├── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── .env
├── .gcloudignore
└── README.md
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
cd app
pip install -r requirements.txt
```

4. Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## Local Development

1. Run the Flask application:
```bash
python main.py
```

2. Visit http://localhost:8080

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t bullet-achievements .
```

2. Run the container:
```bash
docker run -p 8080:8080 --env-file .env bullet-achievements
```

## Google Cloud Run Deployment

1. Set up Google Cloud:
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

2. Create service account for Gemini API:
```bash
# Create service account
gcloud iam service-accounts create gemini-service --display-name="Gemini API Service Account"

# Get project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:gemini-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Download key
gcloud iam service-accounts keys create key.json \
    --iam-account=gemini-service@$PROJECT_ID.iam.gserviceaccount.com
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy bullet-achievements \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## Security Considerations

- API keys and service account credentials are stored securely
- CORS configuration for production
- Rate limiting implementation
- Secure Cloud Run configuration

## Processing Pipeline

1. Input Cleaning
   - Remove filler words
   - Translate non-English inputs
   - Format text

2. Information Extraction
   - Identify key achievements
   - Extract quantifiable results
   - Determine skills and impact

3. Achievement Structuring
   - Apply X-Y-Z formula
   - Organize information

4. Content Generation
   - Create bullet points
   - Generate detailed descriptions

5. Output Refinement
   - Optimize for scholarships
   - Ensure natural language
   - Format final output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Acknowledgments

- Google Gemini AI for natural language processing
- Flask framework for web application
- Google Cloud Run for deployment