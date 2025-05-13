from src.config.configuration import Configuration


def get_number_aliens_x(ai_configuration: Configuration, alien_width: int) -> int:
    """Calculates how many aliens can fit in a single row.

    Args:
        ai_configuration (Settings): Game configuration settings
        alien_width (int): Width of an alien sprite

    Returns:
        int: Number of aliens that can fit in a row

    The calculation takes into account the screen width and leaves space
    for margins on both sides.
    """
    available_space_x = ai_configuration.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_configuration: Configuration, ship_height: int, alien_height: int) -> int:
    """Calculates how many rows of aliens can fit on the screen.

    Args:
        ai_configuration (Settings): Game configuration settings
        ship_height (int): Height of the ship sprite
        alien_height (int): Height of an alien sprite

    Returns:
        int: Number of rows of aliens that can fit on the screen

    The calculation takes into account the screen height, ship height,
    and leaves space for margins.
    """
    available_space_y = ai_configuration.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
