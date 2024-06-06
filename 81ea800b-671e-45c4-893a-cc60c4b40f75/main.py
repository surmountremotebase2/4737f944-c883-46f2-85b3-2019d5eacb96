from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers we are interested in
        self.tickers = ["NKE", "ADDYY", "UAA", "SPRTS"]

    @property
    def interval(self):
        # Use daily data for the analysis
        return "1day"
    
    @property
    def assets(self):
        # Return the tickers we're tracking
        return self.tickers
    
    @property
    def data(self):
        # No additional data needed for this strategy
        return []

    def run(self, data):
        # Initialize an empty dictionary to store our target allocations
        allocation_dict = {}
        
        # Loop through each ticker to check its RSI and determine allocation
        for ticker in self.tickers:
            # Calculate the RSI for the last 14 days
            rsi = RSI(ticker, data["ohlcv"], length=14)
            
            if rsi is not None and len(rsi) > 0:
                current_rsi = rsi[-1]
                log(f"Current RSI for {ticker}: {current_rsi}")
                
                # If RSI < 30, the asset is considered oversold, and we might want to buy
                if current_rsi < 30:
                    allocation_dict[ticker] = 0.3  # Assign a 30% allocation
                # If RSI > 70, the asset is considered overbought, and we might want to sell
                elif current_rsi > 70:
                    allocation_dict[ticker] = 0  # No allocation, consider selling if we have it
                else:
                    # Neutral zone, maintain a baseline allocation
                    allocation_dict[ticker] = 0.1
            else:
                # If we cannot compute RSI, allocate a minimal amount
                allocation_dict[ticker] = 0.05

        # Normalize the allocations to make sure they sum up to 1 (or less)
        total_allocation = sum(allocation_dict.values())
        for ticker in allocation_dict:
            allocation_dict[ticker] /= total_allocation

        return TargetAllocation(allocation_dict)