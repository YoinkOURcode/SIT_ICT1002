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
    
class UpwardsDownwardsArray:
    __slots__ = ("data","tolerance", "upwards", "downwards", "n")

    def __init__(self, data: Iterable[float], tolerance: int = 3):
        """
        Efficient upward/downward run length calculator without NumPy or pandas.

        Parameters
        ----------
        data : iterable of float
            Numeric sequence (list or similar)
        tolerance : int
            Minimum length of consecutive runs to be considered significant
            (default is 3)
        """
        data = list(data)
        if len(data) < 2:
            raise ValueError("data must contain at least two elements")

        self.data: List[float] = data
        self.n = len(data)

        #Keeping track of upwards and downwards runs
        self.upwards = 0
        self.downwards = 0

    def create_run_group(self) -> List[int]:
        """
        First computes consecutive differences in-place
        Next, it will create a run group based on the sign of the differences.
        If positive, it is an upward run; if negative, it is a downward run.
        First element becomes NaN.

        Parameters
        ----------
        values : iterable of floats

        Returns
        -------
        list of integers
        """
        values = self.data

        if not values:
            return

        prev = values[0]
        values[0] = math.nan
        for i in range(1, len(values)):
            curr = values[i]
            
            values[i] = curr - prev
            if values[i] > 0:
                values[i] = 1  # Upward run
                self.upwards += 1

            elif values[i] < 0:
                values[i] = -1  # Downward run
                self.downwards += 1

            else:
                values[i] = 0  # No change
            prev = curr

        return values
    
    def create_run_group_naive(self) -> List[int]:
        """
        Naive way of computing consecutive differences in-place

        Parameters
        ----------
        values : iterable of floats

        Returns
        -------
        list of integers
        """
        values = self.data
        n = len(values)

        if n == 0:
            return []

        result = [math.nan] * n  # First element is NaN
        for i in range(1, n):
            result[i] = 1 if( values[i] - values[i - 1]) > 0 else -1 if (values[i] - values[i - 1]) < 0 else 0 # Upward run, Downward run, No change respectively

        return result
    


   

