import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def measure_single_request(endpoint, payload=None):
    """Make a single request and measure its performance"""
    start_time = time.time()

    if endpoint == "initial":
        response = requests.get("http://localhost:8080/initial_questions")
    else:
        response = requests.post(f"http://localhost:8080/{endpoint}", json=payload)

    end_time = time.time()
    return {
        "endpoint": endpoint,
        "response_time": (end_time - start_time) * 1000,  # Convert to ms
        "status_code": response.status_code,
        "timestamp": datetime.now(),
    }


def run_quick_benchmark(n_requests=50):
    print(f"Starting quick benchmark with {n_requests} requests per endpoint...")

    test_cases = [
        ("initial", None),
        (
            "start_chat",
            {"interest": "software engineering", "problem": "skip", "level": "college"},
        ),
    ]

    results = []
    for endpoint, payload in test_cases:
        for i in range(n_requests):
            try:
                result = measure_single_request(endpoint, payload)
                results.append(result)
                print(f"{endpoint}: {i+1}/{n_requests}", end="\r")
            except Exception as e:
                print(f"\nError with {endpoint}: {e}")

    return pd.DataFrame(results)


def generate_apa_report(results_df, title="Mathy You API Performance Analysis"):
    # Calculate statistics
    stats_by_endpoint = (
        results_df.groupby("endpoint")
        .agg({"response_time": ["count", "mean", "std", "min", "max"]})
        .round(3)
    )

    # Generate APA-style report
    timestamp = datetime.now().strftime("%B %d, %Y")
    report = f"""
{title}
{'='*len(title)}

Date: {timestamp}

Method
------
The performance analysis was conducted on a Flask-based API serving mathematics education content.
The test included {len(results_df)} total requests across {len(results_df['endpoint'].unique())} distinct endpoints.
All measurements were performed on a local development environment.

Results
-------
Response time analysis revealed the following patterns:

"""
    # Add endpoint-specific results
    for endpoint in results_df["endpoint"].unique():
        stats = stats_by_endpoint.loc[endpoint]["response_time"]
        report += f"\n{endpoint.title()} Endpoint:"
        report += f"\nM = {stats['mean']:.3f} ms (SD = {stats['std']:.3f}, n = {int(stats['count'])})"
        report += f"\nRange: {stats['min']:.3f} - {stats['max']:.3f} ms\n"

    return report


def create_apa_visualization(df):
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(2, 1, figsize=(12, 10))

    # Violin plot with embedded box plot
    sns.violinplot(data=df, x="endpoint", y="response_time", inner="box", ax=ax[0])
    ax[0].set_title("MathyYou - Response Time Distribution by Endpoint", fontsize=16)
    ax[0].set_xlabel("Endpoint", fontsize=14)
    ax[0].set_ylabel("Response Time (ms)", fontsize=14)

    # Strip plot for individual data points
    sns.stripplot(
        data=df,
        x="endpoint",
        y="response_time",
        jitter=True,
        color="black",
        alpha=0.5,
        ax=ax[1],
    )
    ax[1].set_title("MathyYou - Individual Response Times by Endpoint", fontsize=16)
    ax[1].set_xlabel("Endpoint", fontsize=14)
    ax[1].set_ylabel("Response Time (ms)", fontsize=14)

    # Add APA-style caption
    plt.figtext(
        0.1,
        -0.1,
        "Figure 1. Response time distributions and individual response times for API endpoints. "
        "The plots show median, quartiles, probability density, and individual data points.",
        wrap=True,
        fontsize=12,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.tight_layout()
    plt.savefig(f"Mathy_You-benchmark_viz_{timestamp}.png", bbox_inches="tight", dpi=300)
    return timestamp


def main():
    print("Starting Performance Analysis...")
    df = run_quick_benchmark()

    # Generate and save APA report
    report = generate_apa_report(df)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"benchmark_report_{timestamp}.txt"

    with open(report_path, "w") as f:
        f.write(report)

    # Create and save visualization
    viz_timestamp = create_apa_visualization(df)

    print(f"\nAnalysis complete!")
    print(f"Report saved as: {report_path}")
    print(f"Visualization saved as: benchmark_viz_{viz_timestamp}.png")
    print("\nSummary Report:")
    print(report)


if __name__ == "__main__":
    main()
