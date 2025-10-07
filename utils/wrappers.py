import time
from functools import wraps
import tracemalloc


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result
    return wrapper

def measure_time_and_space(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start memory tracking
        tracemalloc.start()
        
        # Start time
        start_time = time.perf_counter()
        
        # Run the function
        result = func(*args, **kwargs)
        
        # Stop time
        end_time = time.perf_counter()
        
        # Stop memory tracking and get peak memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Print measurements
        print(f"[{func.__name__}] Time elapsed: {end_time - start_time:.6f} seconds")
        print(f"[{func.__name__}] Peak memory: {peak / 1024:.2f} KB")
        
        return result
    return wrapper

