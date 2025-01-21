"""Color constants."""

from typing import Tuple


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert a hex color to an RGB tuple where each value is ranges from 0 to 1."""
    return (
        int(hex_color[1:3], 16) / 255,
        int(hex_color[3:5], 16) / 255,
        int(hex_color[5:7], 16) / 255,
    )


SUBWAY_RED = hex_to_rgb("#EE352E")
SUBWAY_ORANGE = hex_to_rgb("#FF6319")
SUBWAY_YELLOW = hex_to_rgb("#FCCC0A")

NEUTRAL_000 = hex_to_rgb("#FFFFFF")
NEUTRAL_100 = hex_to_rgb("#F8F3EF")
NEUTRAL_200 = hex_to_rgb("#E4DBD4")
NEUTRAL_300 = hex_to_rgb("#B6A99F")
NEUTRAL_900 = hex_to_rgb("#000000")

STATUS_OK = hex_to_rgb("#34915A")
STATUS_WARNING = hex_to_rgb("#E2B244")
