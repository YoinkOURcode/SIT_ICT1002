import math
from typing import Iterable, List

class RollingMeanArray:
    __slots__ = ("data", "window", "n")

    def __init__(self, data: Iterable[float], window: int):
        """
        Efficient rolling mean calculator without NumPy or array.array.

        Parameters
        ----------
        data : iterable of float
            Numeric sequence (list or similar)
        window : int
            Size of rolling window (must be > 0)
        """
        data = list(data)
        if window <= 0:
            raise ValueError("window must be positive")
        if len(data) < window:
            raise ValueError("window larger than data length")

        self.data: List[float] = data
        self.window = window
        self.n = len(data)

    def rolling_mean(self) -> List[float]:
        n = self.n
        w = self.window
        data = self.data

        # Initialize result list
        result = [math.nan] * n

        # Compute first window sum
        window_sum = sum(data[:w])
        result[w - 1] = window_sum / w

        # Slide window across data
        for i in range(w, n):
            window_sum += data[i] - data[i - w]
            result[i] = window_sum / w

        return result
    
    # --- Naive Implementation ---
    def naive_rolling_mean(self) -> List[float]:
        data = self.data
        window = self.window
        n = len(data)
        result = [math.nan] * n
        for i in range(window - 1, n):
            result[i] = sum(data[i - window + 1:i + 1]) / window
        return result
    



