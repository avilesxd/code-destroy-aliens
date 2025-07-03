class NumberFormatter:
    """
    A class that converts large positive numbers into a compact, human-readable
    string using suffixes like 'k', 'm', 'b', and 't'.

    Example:
        1500       -> '1.5k'
        2000000    -> '2m'
        3500000000 -> '3.5b'

    Useful for displaying scores, currency, or statistics in games or applications.
    """

    SUFFIXES = [
        (1_000_000_000_000, "t"),  # Trillion
        (1_000_000_000, "b"),  # Billion
        (1_000_000, "m"),  # Million
        (1_000, "k"),  # Thousand
    ]

    def __init__(self, decimals: int = 1):
        """
        Initialize the formatter.

        Args:
            decimals (int): Number of decimal places to include in the result (default is 1).
        """
        self.decimals = decimals

    def format(self, number: int | float) -> str:
        """
        Convert a positive number into a compact string with a suffix.

        Args:
            number (int | float): A positive number to format.

        Returns:
            str: A shortened string representation of the number.
        """
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float")

        if number < 0:
            raise ValueError("Number must be non-negative")

        if number < 1000:
            return str(number)

        for value, suffix in self.SUFFIXES:
            if number >= value:
                formatted = number / value
                # Format with the desired number of decimals and strip trailing zeros and dots.
                formatted_str = f"{formatted:.{self.decimals}f}".rstrip("0").rstrip(".")
                return f"{formatted_str}{suffix}"

        # Fallback, though this line should not be reached for numbers >= 1000
        return str(number)
