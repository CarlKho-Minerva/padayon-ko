import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def measure_single_request(prompt_type, essay_text):
    """
    Measure performance metrics for a single essay processing request.

    Parameters
    ----------
    prompt_type : str
        Type of essay prompt
    essay_text : str
        Input essay text

    Returns
    -------
    dict
        Performance metrics for the request
    """
    start_time = time.time()
    response = requests.post(
        "http://localhost:8080/process",
        json={
            "essay_type": prompt_type,
            "essay_content": essay_text,
            "needs_translation": False
        }
    )
    end_time = time.time()

    return {
        "prompt_type": prompt_type,
        "response_time": end_time - start_time,
        "status_code": response.status_code,
        "input_length": len(essay_text),
        "timestamp": datetime.now()
    }

def run_benchmark(num_requests=30):
    """
    Run benchmark tests across different essay prompts and lengths.

    Parameters
    ----------
    num_requests : int, optional
        Number of requests per test case (default is 30)

    Returns
    -------
    pandas.DataFrame
        Benchmark results
    """
    test_cases = [
        ("tell_us_about_you", "I overcame challenges in my life."),  # Short
        ("academic_and_career_goals", "I want to study computer science and become a software engineer. " * 3),  # Medium
        ("community_contribution", "I volunteered at the local food bank and helped organize donations. " * 5),  # Long
    ]

    results = []
    print(f"Starting benchmark with {len(test_cases) * num_requests} total requests...")

    for prompt_type, text in test_cases:
        for _ in range(num_requests):
            try:
                result = measure_single_request(prompt_type, text)
                results.append(result)
                print(".", end="", flush=True)
            except Exception as e:
                print(f"\nError: {e}")

    print("\nBenchmark completed!")
    return pd.DataFrame(results)

def generate_visualizations(df):
    """
    Generate and save performance visualization plots.

    Parameters
    ----------
    df : pandas.DataFrame
        Benchmark results data

    Returns
    -------
    dict
        Summary statistics
    """
    plt.style.use('seaborn')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    # Response Time by Prompt Type
    sns.boxplot(data=df, x="prompt_type", y="response_time", ax=ax1)
    ax1.set_title("Response Time Distribution by Prompt Type", pad=20)
    ax1.set_xlabel("Prompt Type")
    ax1.set_ylabel("Response Time (seconds)")
    ax1.tick_params(axis='x', rotation=45)

    # Response Time vs Input Length
    sns.scatterplot(data=df, x="input_length", y="response_time", ax=ax2)
    ax2.set_title("Response Time vs Input Length", pad=20)
    ax2.set_xlabel("Input Length (characters)")
    ax2.set_ylabel("Response Time (seconds)")

    plt.tight_layout()
    plt.savefig("essay_platform_benchmark.png", dpi=300, bbox_inches='tight')
    print("\nVisualizations saved as 'essay_platform_benchmark.png'")

    stats = {
        "avg_response_time": df["response_time"].mean(),
        "median_response_time": df["response_time"].median(),
        "p95_response_time": df["response_time"].quantile(0.95),
        "max_response_time": df["response_time"].max(),
        "total_requests": len(df)
    }

    return stats

def main():
    """Main execution function for the benchmark suite."""
    print("Starting Essay Platform Performance Benchmark...")
    df = run_benchmark()

    print("\nCalculating statistics...")
    stats = generate_visualizations(df)

    print("\nPerformance Summary:")
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Average Response Time: {stats['avg_response_time']:.2f} seconds")
    print(f"Median Response Time: {stats['median_response_time']:.2f} seconds")
    print(f"95th Percentile Response Time: {stats['p95_response_time']:.2f} seconds")
    print(f"Maximum Response Time: {stats['max_response_time']:.2f} seconds")

    # Save raw data for further analysis
    df.to_csv("essay_platform_benchmark_data.csv", index=False)

if __name__ == "__main__":
    main()
