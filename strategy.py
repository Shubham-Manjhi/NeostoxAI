"""
This is the file that the user has to edit, the strategy function to be precise.
How to modify:
1. specify the list of options you are going to trade on
2. specify the enter conditions and exit conditions
3. To get access to the latest minute data just use self.data[instrument_name][-1] where instrument_name is an instrument from the list specified in the 1st step.
4. You can add additional parameters to the init of the Strategy class if needed.
"""
from broker import *

class Strategy(broker):
    def __init__(self):
        super().__init__()
        # Get the first available instrument from the list
        if self.instruments:
            self.instrument_name = list(self.instruments.keys())[0]
            print(f"Selected instrument: {self.instrument_name}")
        else:
            self.instrument_name = None
            print("No instruments found!")

    def strategy(self):
        # Simple demo strategy - alternates between buy and sell every other minute
        if self.instrument_name and self.instrument_name in self.instruments:
            print(f"Executing strategy for {self.instrument_name} at index {self.index}")
            if self.index % 2 == 1:
                print(f"BUY signal for {self.instrument_name}")
                self.buy_order(self.instrument_name, 1)
            else:
                print(f"SELL signal for {self.instrument_name}")
                self.sell_order(self.instrument_name, 1)
        else:
            print("No valid instrument to trade")


if __name__ == "__main__":
    model = Strategy()
    model.run()

