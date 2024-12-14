import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Sample achievements of different complexities
TEST_CASES = {
    "Simple": "Led a team project",
    "Medium": "Led a team of 5 developers to complete a mobile app project",
    "Complex": "Led a cross-functional team of 5 developers and 3 designers to develop and launch a mobile app that achieved 10,000 downloads in first month, increasing user engagement by 45%"
}

def benchmark_request(complexity, text):
    """Benchmark a single request"""
    start_time = time.time()
    response = requests.post(
        'http://localhost:8080/generate',
        json={'achievement': text, 'isEnglish': True}
    )
    end_time = time.time()

    return {
        'complexity': complexity,
        'response_time': end_time - start_time,
        'timestamp': datetime.now(),
        'status': response.status_code
    }

def run_benchmark(iterations=5):
    """Run benchmarks for each complexity level"""
    results = []
    print("Running benchmarks...")

    for complexity, text in TEST_CASES.items():
        print(f"\nTesting {complexity} input ({len(text)} chars):")
        for i in range(iterations):
            result = benchmark_request(complexity, text)
            results.append(result)
            print(f"✓ Iteration {i+1}: {result['response_time']:.2f}s")

    return pd.DataFrame(results)

def create_visualization(df):
    """Create an attractive visualization for the hackathon"""
    plt.figure(figsize=(12, 5))

    # Create a professional-looking boxplot
    plt.subplot(1, 2, 1)
    sns.boxplot(x='complexity', y='response_time', data=df,
                palette='viridis')
    plt.title('Response Time by Input Complexity', pad=20)
    plt.ylabel('Response Time (seconds)')

    # Add trend line
    plt.subplot(1, 2, 2)
    sns.regplot(x=range(len(df)), y='response_time', data=df,
                scatter_kws={'alpha':0.5}, line_kws={'color': 'red'})
    plt.title('Response Time Trend', pad=20)
    plt.xlabel('Request Sequence')
    plt.ylabel('Response Time (seconds)')

    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'benchmark_results.png'")

def main():
    # Run benchmark
    print("🚀 Starting Achievement Generator Benchmark")
    print("-" * 50)
    df = run_benchmark()

    # Calculate statistics
    stats = df.groupby('complexity')['response_time'].agg([
        'mean', 'min', 'max', 'std'
    ]).round(2)

    # Print results
    print("\n📊 Benchmark Results:")
    print("-" * 50)
    print(f"Total Requests: {len(df)}")
    print(f"Average Response Time: {df['response_time'].mean():.2f}s")
    print("\nBy Complexity Level:")
    print(stats)

    # Create visualization
    create_visualization(df)

if __name__ == "__main__":
    main()
