import math
class RollingMeanArray:
    __slots__ = ("data", "window", "n", "predict_steps")

    def __init__(self, data , window: int ):
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

        self.data = data
        self.window = window
        self.n = len(data)

    def rolling_mean(self) -> float:
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
        # --- Optional Forecast Extension ---



        return result
    
    @staticmethod
    def predict(data, window, steps: int = 5) -> float:
        """
        Predict next 'steps' values using rolling mean of the last 'window' values.

        Parameters
        ----------
        data : iterable of float
            Numeric sequence (list or similar)
        steps : int
            Number of future steps to predict (default is 5)

        Returns
        -------
        list of floats
            Original data extended with predicted values
        """
        data = list(data)
        # Only keep the last `window` elements (minimal required context)
        if len(data) < window:
            raise ValueError("data length must be at least as large as window size")

        recent_window = data[-window:]  # minimal required data
        window_sum = sum(recent_window)      # precompute initial window sum
        predictions = []  # store predicted values
        for _ in range(steps):
            next_value = window_sum / window
            predictions.append(next_value)

            # Update sliding window sum efficiently
            window_sum += next_value - recent_window[0]
            recent_window.pop(0)
            recent_window.append(next_value)

        # Return the last window + predicted values (or only predicted if you prefer)
        return predictions
    
    # --- Naive Implementation ---
    def naive_rolling_mean(self) -> float:
        data = self.data
        window = self.window
        n = len(data)
        result = [math.nan] * n
        for i in range(window - 1, n):
            result[i] = sum(data[i - window + 1:i + 1]) / window
        return result
    
class UpwardsDownwardsArray:
    __slots__ = ("data", "upwards", "downwards", "n")

    def __init__(self, data: float):
        """
        Efficient upward/downward run length calculator without NumPy or pandas.

        Parameters
        ----------
        data : iterable of float
            Numeric sequence (list or similar)
        
        """
        data = list(data)
        if len(data) < 2:
            raise ValueError("data must contain at least two elements")

        self.data: float = data
        self.n = len(data)

        #Keeping track of upwards and downwards runs
        self.upwards = 0
        self.downwards = 0

    def create_run_group(self) -> int:
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
    
    def create_run_group_naive(self) -> int:
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
    


   

