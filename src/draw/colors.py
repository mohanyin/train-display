"""Color constants."""

from typing import Tuple


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert a hex color to an RGB tuple where each value is ranges from 0 to 1."""
    return (
        int(hex_color[1:3], 16) / 255,
        int(hex_color[3:5], 16) / 255,
        int(hex_color[5:7], 16) / 255,
    )


SUBWAY_RED = hex_to_rgb("#FF0000")
SUBWAY_ORANGE = hex_to_rgb("#FF7F00")
SUBWAY_YELLOW = hex_to_rgb("#FFFD01")

NEUTRAL_000 = hex_to_rgb("#FFFFFF")
NEUTRAL_100 = hex_to_rgb("#F8F8F8")
NEUTRAL_200 = hex_to_rgb("#ECECEC")
NEUTRAL_300 = hex_to_rgb("#B6B6B6")
NEUTRAL_900 = hex_to_rgb("#000000")

STATUS_OK = hex_to_rgb("#00BF00")
STATUS_WARNING = hex_to_rgb("#FFFD01")
