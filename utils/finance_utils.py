def maxProfit(prices):
    profit = 0
    for i in range(1, len(prices)):
        # If price goes up from yesterday, add the difference
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit