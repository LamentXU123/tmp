import timeit
from statistics import mean, stdev
import sys
# Alternative implementations
def current_clock_sequence():
    import random
    return random.getrandbits(14)

# Alternative implementations
def clockseq_secrets():
    import secrets
    return secrets.randbits(14)

def clockseq_urandom():
    from os import urandom
    return int.from_bytes(urandom(2), 'big') & 0x3fff

def clockseq_urandom_optimized():
    # Using memoryview for potential optimization
    from os import urandom
    return int.from_bytes(urandom(2), 'big', signed=False) & 0x3fff

# Benchmark configuration
NUM_ITERATIONS = 1_000_000
WARMUP_ROUNDS = 100
TEST_CASES = [
    ("current (random.getrandbits)", "current_clock_sequence()"),
    ("secrets.getrandbits", "clockseq_secrets()"),
    ("os.urandom", "clockseq_urandom()"),
    ("os.urandom_optimized", "clockseq_urandom_optimized()"),
]

def run_benchmark():
    print(f"Python {sys.version}")
    print(f"Benchmarking {NUM_ITERATIONS:,} iterations\n")
    
    # Warmup
    print("Running warmup...")
    for _ in range(WARMUP_ROUNDS):
        current_clock_sequence()
        clockseq_secrets()
        clockseq_urandom()
        clockseq_urandom_optimized()
    
    results = {}
    
    for name, stmt in TEST_CASES:
        print(f"\nBenchmarking {name}...")
        
        # Timeit approach
        timer = timeit.Timer(stmt=stmt, globals=globals())
        times = timer.repeat(repeat=5, number=NUM_ITERATIONS)
        
        # Calculate metrics
        avg_time = mean(times) / NUM_ITERATIONS * 1e9  # Convert to nanoseconds
        std_dev = stdev(times) / NUM_ITERATIONS * 1e9
        ops_per_sec = NUM_ITERATIONS / mean(times)
        
        results[name] = {
            'avg_ns': avg_time,
            'stddev_ns': std_dev,
            'ops_per_sec': ops_per_sec
        }
        
        print(f"  Average: {avg_time:.2f} ns ± {std_dev:.2f} ns per loop")
        print(f"  Operations/sec: {ops_per_sec:,.0f}")
    
    # Print comparison table
    print("\n=== Results Summary ===")
    print(f"{'Method':<25} {'Avg (ns)':>10} {'Std Dev':>10} {'Ops/sec':>15}")
    print("-" * 60)
    for name, res in sorted(results.items(), key=lambda x: x[1]['avg_ns']):
        print(f"{name:<25} {res['avg_ns']:>10.2f} {res['stddev_ns']:>10.2f} {res['ops_per_sec']:>15,.0f}")

if __name__ == "__main__":
    run_benchmark()
