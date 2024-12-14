import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import base64
import os


def measure_conversation_turn(mode, audio_file_path):
    """Measure performance of a single conversation turn"""
    start_time = time.time()

    try:
        with open(audio_file_path, "rb") as audio:
            files = {"audio": ("recording.wav", audio, "audio/wav")}
            data = {"mode": mode}

            response = requests.post(
                "http://localhost:8080/process_audio", files=files, data=data
            )

        end_time = time.time()

        return {
            "mode": mode,
            "response_time": end_time - start_time,
            "status_code": response.status_code,
            "audio_size": os.path.getsize(audio_file_path),
            "timestamp": datetime.now(),
            "has_audio_response": (
                "audio_response" in response.json()
                if response.status_code == 200
                else False
            ),
        }
    except Exception as e:
        print(f"\nError in {mode} mode: {str(e)}")
        return None


def run_benchmark(num_requests=20):
    """Run benchmarks across different conversation modes"""
    modes = ["debate", "storytelling", "qa", "explain"]
    # Use the actual audio file name
    test_audio_path = "/Users/cvk/Downloads/[CODE] Local Projects/24SUMR_PadayonKo/fluent/app/micro-machines.wav"

    if not os.path.exists(test_audio_path):
        raise FileNotFoundError(f"Test audio file not found: {test_audio_path}")

    results = []
    print(f"Starting benchmark with {num_requests} requests per mode...")
    print(f"Using test audio file: {test_audio_path}")

    for mode in modes:
        print(f"\nTesting {mode} mode...")
        for i in range(num_requests):
            result = measure_conversation_turn(mode, test_audio_path)
            if result:  # Only append successful results
                results.append(result)
                print(f"Request {i+1}/{num_requests} completed", end="\r")

    if not results:
        raise ValueError("No successful benchmark results were collected")

    print("\nBenchmark completed!")
    return pd.DataFrame(results)


def generate_visualizations(df):
    """Generate comprehensive performance visualizations"""
    if df.empty:
        print("No data available for visualization")
        return None

    plt.style.use("seaborn")
    fig = plt.figure(figsize=(15, 10))

    try:
        # 1. Response Time by Mode
        plt.subplot(2, 2, 1)
        if len(df["mode"].unique()) > 0:
            sns.boxplot(x=df["mode"], y=df["response_time"])
            plt.title("Response Time Distribution by Mode")
            plt.xticks(rotation=45)
            plt.ylabel("Response Time (seconds)")

        # 2. Performance Over Time
        plt.subplot(2, 2, 2)
        sns.scatterplot(
            data=df, x="timestamp", y="response_time", hue="mode", alpha=0.6
        )
        plt.title("Response Time Trend")
        plt.xticks(rotation=45)
        plt.ylabel("Response Time (seconds)")

        # 3. Audio Size vs Response Time
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=df, x="audio_size", y="response_time", hue="mode")
        plt.title("Response Time vs Audio Size")
        plt.xlabel("Audio Size (bytes)")
        plt.ylabel("Response Time (seconds)")

        # 4. Success Rate by Mode
        plt.subplot(2, 2, 4)
        success_rate = df.groupby("mode")["status_code"].apply(
            lambda x: (x == 200).mean() * 100
        )
        sns.barplot(x=success_rate.index, y=success_rate.values)
        plt.title("Success Rate by Mode")
        plt.ylabel("Success Rate (%)")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig("fluent_benchmark_results.png")
        print("Visualizations saved as 'fluent_benchmark_results.png'")

        return calculate_statistics(df)
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")
        return None


def calculate_statistics(df):
    """Calculate detailed performance statistics"""
    stats = {
        "overall": {
            "avg_response_time": df["response_time"].mean(),
            "median_response_time": df["response_time"].median(),
            "95th_percentile": df["response_time"].quantile(0.95),
            "success_rate": (df["status_code"] == 200).mean() * 100,
        },
        "by_mode": {},
    }

    for mode in df["mode"].unique():
        mode_df = df[df["mode"] == mode]
        stats["by_mode"][mode] = {
            "avg_response_time": mode_df["response_time"].mean(),
            "median_response_time": mode_df["response_time"].median(),
            "success_rate": (mode_df["status_code"] == 200).mean() * 100,
        }

    return stats


def main():
    print("Starting Fluent Performance Benchmark...")
    print("Note: Make sure the Fluent server is running on localhost:8080")

    try:
        df = run_benchmark(num_requests=5)  # Reduced number for testing
        if not df.empty:
            stats = generate_visualizations(df)
            if stats:
                print("\nPerformance Summary:")
                print(f"\nOverall Statistics:")
                print(
                    f"Average Response Time: {stats['overall']['avg_response_time']:.2f} seconds"
                )
                print(
                    f"Median Response Time: {stats['overall']['median_response_time']:.2f} seconds"
                )
                print(
                    f"95th Percentile: {stats['overall']['95th_percentile']:.2f} seconds"
                )
                print(f"Overall Success Rate: {stats['overall']['success_rate']:.1f}%")

                print("\nPerformance by Mode:")
                for mode, mode_stats in stats["by_mode"].items():
                    print(f"\n{mode.upper()}:")
                    print(
                        f"  Average Response Time: {mode_stats['avg_response_time']:.2f} seconds"
                    )
                    print(
                        f"  Median Response Time: {mode_stats['median_response_time']:.2f} seconds"
                    )
                    print(f"  Success Rate: {mode_stats['success_rate']:.1f}%")
                df.to_csv("fluent_benchmark_data.csv", index=False)
                print("\nRaw benchmark data saved to 'fluent_benchmark_data.csv'")
        else:
            print("No benchmark data was collected")
    except Exception as e:
        print(f"Benchmark failed: {str(e)}")


if __name__ == "__main__":
    main()
