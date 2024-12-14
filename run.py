import os
import subprocess

# Define the apps and their respective ports
apps = {
    "bullet_achievements": 8081,
    "super-essays": 8082,
    "origin_story": 8083,
    "fluent": 8084,
    "foundational-essays": 8085,
    "mathyyou": 8086,
}

# Base directory for the apps
base_dir = "backend/AI_Features"


# Function to run a Flask app
def run_app(app_name, port):
    app_dir = os.path.join(base_dir, app_name, "app")
    env = os.environ.copy()
    env["FLASK_APP"] = "main.py"
    env["PORT"] = str(port)
    subprocess.Popen(
        ["flask", "run", "--host=0.0.0.0", "--port", str(port)], cwd=app_dir, env=env
    )


# Run each app on its respective port
for app_name, port in apps.items():
    run_app(app_name, port)
