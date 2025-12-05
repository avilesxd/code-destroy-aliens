import math


class NumberFormatter:
    """

    A class that converts large positive numbers into a compact, human-readable
    string using suffixes like 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx' and 'Oc'.

    Example:
        1500 -> '1.5K'
        2000000 -> '2M'
        3500000000 -> '3.5B'
        1250000000000 -> '1.25T'
        7800000000000000 -> '7.8Qa'
        9600000000000000000 -> '9.6Qi'
        1500000000000000000000 -> '1.5Oc'

    Useful for displaying scores, currency, or statistics in games or applications.
    """

    # Suffixes mapped by index.
    # Index 0 = <1000, 1 = K (10^3), 2 = M (10^6), etc.
    SUFFIXES = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Oc"]

    def __init__(self, decimals: int = 1):
        self.decimals = decimals

    def format(self, number: int | float) -> str:
        """
        Convert a number into a compact string using logarithmic magnitude calculation.
        """
        # 1. Validation
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float")
        if number < 0:
            raise ValueError("Number must be non-negative")

        # 2. Base case for small numbers (0 to 999.99...)
        if number < 1000:
            # Optional: apply decimal formatting to small numbers too if needed
            # currently behaves like the original: raw string
            return str(int(number)) if isinstance(number, int) else str(number)

        # 3. Calculate magnitude (O(1) operation)
        # log10(number) gives the power of 10. Dividing by 3 gives the groups of thousands.
        # Example: log10(2,000,000) ~ 6.3.  6.3 // 3 = 2.0. Index 2 is 'M'.
        magnitude = int(math.log10(number) // 3)

        # 4. Handle numbers larger than our largest suffix
        if magnitude >= len(self.SUFFIXES):
            magnitude = len(self.SUFFIXES) - 1

        # 5. Calculate the value relative to the suffix
        # 10 ** (magnitude * 3) creates the divisor (1000, 1000000, etc.)
        formatted_number = number / (10 ** (magnitude * 3))

        # 6. Format string
        # We format normally, and simple rstrips to clean output
        formatted_str = f"{formatted_number:.{self.decimals}f}".rstrip("0").rstrip(".")

        return f"{formatted_str}{self.SUFFIXES[magnitude]}"
