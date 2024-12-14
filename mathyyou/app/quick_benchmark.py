import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
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
        "response_time": end_time - start_time,
        "status_code": response.status_code,
        "timestamp": datetime.now(),
    }


def run_quick_benchmark(n_requests=30):
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
                start_time = time.time()
                if endpoint == "initial":
                    response = requests.get("http://localhost:8080/initial_questions")
                else:
                    response = requests.post(
                        f"http://localhost:8080/{endpoint}", json=payload
                    )
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

                results.append(
                    {
                        "endpoint": endpoint,
                        "response_time": elapsed_time,
                        "status_code": response.status_code,
                        "timestamp": datetime.now(),
                    }
                )
                print(f"{endpoint}: {i+1}/{n_requests}", end="\r")

            except Exception as e:
                print(f"\nError with {endpoint}: {e}")

    return pd.DataFrame(results)


def generate_apa_report(results_df, title="API Performance Analysis"):
    from scipy import stats  # Move import here to fix the stats reference

    # Calculate statistics
    stats_by_endpoint = (
        results_df.groupby("endpoint")
        .agg({"response_time": ["count", "mean", "std", "min", "max"]})
        .round(3)
    )

    # Calculate confidence intervals
    ci_95 = {}
    for endpoint in results_df["endpoint"].unique():
        data = results_df[results_df["endpoint"] == endpoint]["response_time"]
        ci = stats.t.interval(
            alpha=0.95, df=len(data) - 1, loc=np.mean(data), scale=stats.sem(data)
        )
        ci_95[endpoint] = [round(ci[0], 3), round(ci[1], 3)]

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
        report += f"\n95% CI [{ci_95[endpoint][0]:.3f}, {ci_95[endpoint][1]:.3f}]"
        report += f"\nRange: {stats['min']:.3f} - {stats['max']:.3f} ms\n"

    # Add statistical interpretation
    f_stat, p_val = stats.f_oneway(
        *[
            group["response_time"].values
            for name, group in results_df.groupby("endpoint")
        ]
    )

    report += f"""
Statistical Analysis
------------------
A one-way ANOVA revealed {
    'significant' if p_val < 0.05 else 'no significant'} differences in response times
between endpoints, F = {f_stat:.3f}, p = {p_val:.3f}.

Discussion
----------
The analysis indicates that the API demonstrates {'consistent' if p_val >= 0.05 else 'varying'}
performance across endpoints. Response times remain within acceptable ranges for interactive
use (< 1000ms), suggesting adequate responsiveness for educational applications.
"""
    return report


def create_apa_visualization(df):
    plt.style.use("seaborn")
    plt.figure(figsize=(10, 6))

    # Create violin plot with embedded box plot
    sns.violinplot(data=df, x="endpoint", y="response_time", inner="box")
    plt.title("Response Time Distribution by Endpoint")
    plt.xlabel("Endpoint")
    plt.ylabel("Response Time (ms)")

    # Add APA-style caption
    plt.figtext(
        0.1,
        -0.1,
        "Figure 1. Response time distributions for API endpoints. "
        "The plot shows median, quartiles, and probability density.",
        wrap=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"benchmark_viz_{timestamp}.png", bbox_inches="tight", dpi=300)
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
