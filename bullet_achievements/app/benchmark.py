import requests
import time
import psutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


def measure_single_request(text):
    """Make a single request and measure its performance"""
    start_time = time.time()
    response = requests.post(
        "http://localhost:8080/generate", json={"achievement": text, "isEnglish": True}
    )
    end_time = time.time()

    return {
        "response_time": end_time - start_time,
        "status_code": response.status_code,
        "input_length": len(text),
        "timestamp": datetime.now(),
    }


def run_quick_benchmark(num_requests=10):
    """Run a quick benchmark with fewer samples"""
    # Simple test inputs of varying lengths
    test_inputs = [
        "Led a team",  # Short
        "Led a team of 5 developers",  # Medium
        "Led a team of 5 developers to complete project ahead of schedule",  # Long
    ]

    results = []
    print(f"Starting quick benchmark with {num_requests} total requests...")

    for text in test_inputs:
        for _ in range(num_requests // len(test_inputs)):
            try:
                result = measure_single_request(text)
                results.append(result)
                print(".", end="", flush=True)
            except Exception as e:
                print(f"\nError: {e}")

    print("\nBenchmark completed!")
    return pd.DataFrame(results)


def generate_quick_viz(df):
    """Generate simplified visualizations"""
    plt.figure(figsize=(12, 5))

    # 1. Response Time Distribution
    plt.subplot(1, 2, 1)
    sns.boxplot(data=df, y="response_time", x="input_length")
    plt.title(
        "Figure 1\nResponse Time Distribution by Input Length for Achievement Bullet Maker"
    )
    plt.xlabel("Input Length (characters)")
    plt.ylabel("Response Time (seconds)")

    # 2. Performance Over Time
    plt.subplot(1, 2, 2)
    sns.scatterplot(data=df, x="timestamp", y="response_time", alpha=0.6)
    plt.title("Figure 2\nAchievement Bullet Maker Response Time Trend")
    plt.xlabel("Request Timestamp")
    plt.ylabel("Response Time (seconds)")

    plt.tight_layout()
    plt.savefig("achievement_bullet_maker_benchmark.png")
    print("Visualizations saved as 'achievement_bullet_maker_benchmark.png'")

    # Quick stats
    stats = {
        "avg_response_time": df["response_time"].mean(),
        "median_response_time": df["response_time"].median(),
        "max_response_time": df["response_time"].max(),
        "total_requests": len(df),
    }

    return stats


def main():
    print("Starting Quick Performance Benchmark...")
    df = run_quick_benchmark()

    print("\nCalculating statistics...")
    stats = generate_quick_viz(df)

    print("\nPerformance Summary:")
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Average Response Time: {stats['avg_response_time']:.2f} seconds")
    print(f"Median Response Time: {stats['median_response_time']:.2f} seconds")
    print(f"Max Response Time: {stats['max_response_time']:.2f} seconds")

    # Save raw data
    df.to_csv("quick_benchmark_data.csv", index=False)


if __name__ == "__main__":
    main()
