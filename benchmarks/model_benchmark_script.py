import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys


def verify_server(url):
    """Verify server is running and return appropriate error message"""
    try:
        print(f"\nTrying to connect to server at {url}...")
        test_response = requests.get(url, timeout=5)
        test_response.raise_for_status()
        print("✅ Server is running and responding!")
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server!")
        print("\nPossible solutions:")
        print("1. Make sure you're in the correct directory: cd super-essays/app")
        print("2. Start the Flask server: python main.py")
        print("3. Wait a few seconds for the server to start")
        print("4. If using Cloud Run URL, make sure it's correct and accessible")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: Unexpected error while connecting to server: {str(e)}")
        return False


def run_benchmark(url="http://localhost:8080", n_requests=30):
    """Run performance benchmark on the API"""

    if not verify_server(url):
        sys.exit(1)

    # Test data
    test_query = "Tell me about a time you demonstrated leadership"

    metrics = {"query_time": [], "generate_time": [], "total_time": []}

    print(f"\nRunning benchmark with {n_requests} requests...")
    print(f"Server URL: {url}")

    successful_requests = 0

    try:
        for _ in tqdm(range(n_requests)):
            try:
                start_total = time.time()

                # Test query_essays_achievements endpoint
                start = time.time()
                response = requests.post(
                    f"{url.rstrip('/')}/query_essays_achievements",
                    json={"query": test_query},
                    timeout=30,
                )  # Add timeout
                response.raise_for_status()
                query_time = time.time() - start

                data = response.json()
                essays = data["essays"]
                achievements = data["achievements"]

                # Test generate_essay endpoint
                start = time.time()
                response = requests.post(
                    f"{url.rstrip('/')}/generate_essay",
                    json={
                        "query": test_query,
                        "selected_essays": [essays[0]["content"]],
                        "selected_achievements": [achievements[0]["content"]],
                    },
                    timeout=60,
                )  # Longer timeout for generation
                response.raise_for_status()
                generate_time = time.time() - start

                total_time = time.time() - start_total

                metrics["query_time"].append(query_time)
                metrics["generate_time"].append(generate_time)
                metrics["total_time"].append(total_time)

                successful_requests += 1

                # Add small delay to prevent rate limiting
                time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                print(f"\nRequest failed: {str(e)}")
                continue

    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")

    if successful_requests == 0:
        print("No successful requests completed!")
        sys.exit(1)

    print(f"\nCompleted {successful_requests}/{n_requests} requests successfully")
    return pd.DataFrame(metrics)


def plot_metrics(df):
    """Generate visualization of benchmark results"""

    # Set style
    sns.set_theme(style="whitegrid")

    # Calculate statistics for the title
    mean_total = df['total_time'].mean()

    # Create figure with multiple plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Box plot for distribution
    sns.boxplot(data=df, ax=ax1)
    ax1.set_title(f'Response Time Distribution\nAvg Total: {mean_total:.2f}s')
    ax1.set_ylabel('Time (seconds)')

    # Line plot for response times over requests
    ax2.plot(df.index + 1, df['query_time'], label='Query Time', marker='o')
    ax2.plot(df.index + 1, df['generate_time'], label='Generate Time', marker='o')
    ax2.plot(df.index + 1, df['total_time'], label='Total Time', marker='o')

    ax2.set_title('Response Times Over Requests')
    ax2.set_xlabel('Request Number')
    ax2.set_ylabel('Time (seconds)')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("\nBenchmark visualization saved as 'benchmark_results.png'")

    # Print summary statistics
    print("\nSummary Statistics (in seconds):")
    stats = df.describe().round(2)
    print(stats)

    # Print average timings
    print("\nAverage Timings:")
    print(f"Query Time:     {df['query_time'].mean():.2f}s")
    print(f"Generate Time:  {df['generate_time'].mean():.2f}s")
    print(f"Total Time:     {df['total_time'].mean():.2f}s")


if __name__ == "__main__":
    print("🔄 Starting benchmark process...")
    print("\n📋 Checklist before running:")
    print("1. Flask server should be running")
    print("2. You have valid API keys in .env")
    print("3. You're using the correct URL")

    # Allow custom URL from command line
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", default="http://localhost:8080", help="URL of the server to benchmark"
    )
    parser.add_argument(
        "--requests", type=int, default=30, help="Number of requests to make"
    )
    args = parser.parse_args()

    try:
        results = run_benchmark(url=args.url, n_requests=args.requests)
        plot_metrics(results)
    except Exception as e:
        print(f"Benchmark failed: {str(e)}")
        sys.exit(1)
