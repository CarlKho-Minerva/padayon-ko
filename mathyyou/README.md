# MathyYou - Interest-aligned Math Practice

A Socratic math tutor that aligns math problems with students' career interests, powered by Google's Gemini Pro.

## Features

- Career-contextualized math problems
- Socratic teaching method
- Integrated tools:
  - Scientific calculator
  - Matrix calculator
  - Graphing calculator
  - Python/SageMath interpreters
  - Sketchpad

## Setup & Installation

1. Clone the repository

```bash
git clone [your-repo-url]
cd mathyyou
```

2. Install dependencies

```bash
pip install -r app/requirements.txt
```

3. Set up environment variables

```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Local Development

Run the Flask application:

```bash
cd app
python main.py
```

The application will be available at `http://localhost:8080`

## Cloud Run Deployment

1. Build and deploy using Cloud Run:

```bash
cd app
gcloud config set builds/use_kaniko True
gcloud builds submit --no-cache --build-arg GEMINI_API_KEY=$GEMINI_API_KEY --tag gcr.io/[PROJECT-ID]/math-socratic-practice
gcloud run deploy math-socratic-practice \
    --image gcr.io/[PROJECT-ID]/math-socratic-practice \
    --platform managed \
    --allow-unauthenticated
```

2. Cloud Run will provide a URL where your application is deployed.

## Performance Benchmarking

Run the benchmarking script to measure API performance:

```bash
python benchmark.py
```

The script measures:

- Response times for each endpoint
- Memory usage over time
- Distribution of response latencies

Results are saved as:

- Visual plots in `performance_metrics.png`
- Printed summary statistics in the console

### Benchmark Metrics

- Response Time (ms)
  - Mean, median, p95 latencies
  - Distribution across endpoints
- Memory Usage (MB)
  - Peak memory consumption
  - Memory usage patterns
  - Resource efficiency

## Architecture

```
app/
├── main.py           # Flask application entry point
├── config.py         # Gemini AI configuration
├── handlers.py       # Request handlers
├── chat.py          # Chat session management
├── benchmark.py      # Performance testing
└── templates/
    └── index.html    # Frontend interface
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your chosen license]

## Contact

Your Name - [kho@uni.minerva.edu](mailto:kho@uni.minerva.edu)
