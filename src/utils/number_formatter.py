class NumberFormatter:
    SUFFIXES = [
        (1_000_000_000_000, "t"),
        (1_000_000_000, "b"),
        (1_000_000, "m"),
        (1_000, "k"),
    ]

    def __init__(self, decimals: int = 1):
        self.decimals = decimals

    def format(self, number: int | float) -> str:
        if number < 1000:
            return str(number)

        for value, suffix in self.SUFFIXES:
            if number >= value:
                formatted = number / value
                formatted_str = f"{formatted:.{self.decimals}f}".rstrip("0").rstrip(".")
                return f"{formatted_str}{suffix}"

        return str(number)
