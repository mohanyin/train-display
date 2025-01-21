"""Drawing utils."""

import math
from typing import Tuple

# pylint: disable=no-member
# missing types because of C bindings
import cairo


def draw_stroke_or_fill(
    ctx: cairo.Context,
    *,
    stroke: Tuple[float, float, float] | None = None,
    fill: Tuple[float, float, float] | None = None,
) -> None:
    """Draw a stroke or fill."""
    if fill:
        ctx.set_source_rgb(*fill)
        ctx.fill()

    if stroke:
        ctx.set_line_width(1)
        ctx.set_source_rgb(*stroke)
        ctx.stroke()


def draw_circle(
    ctx: cairo.Context,
    *,
    x: float,
    y: float,
    radius: float,
    fill: Tuple[float, float, float],
) -> None:
    """Draw a circle."""
    ctx.set_source_rgb(*fill)
    ctx.arc(x + radius, y + radius, radius, 0, 2 * math.pi)
    draw_stroke_or_fill(ctx, fill=fill)


# todo: make a position class
# pylint: disable=too-many-arguments
def draw_rounded_rectangle(
    ctx: cairo.Context,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    radius: float,
    fill: Tuple[float, float, float] | None = None,
    stroke: Tuple[float, float, float] | None = None,
) -> None:
    """Draw a rounded rectangle."""
    # Make sure radius doesn't exceed half of the minimum dimension
    radius = min(radius, width / 2, height / 2)

    # Top right corner
    ctx.move_to(x + radius, y)
    ctx.line_to(x + width - radius, y)
    ctx.arc(x + width - radius, y + radius, radius, -math.pi / 2, 0)

    # Bottom right corner
    ctx.line_to(x + width, y + height - radius)
    ctx.arc(x + width - radius, y + height - radius, radius, 0, math.pi / 2)

    # Bottom left corner
    ctx.line_to(x + radius, y + height)
    ctx.arc(x + radius, y + height - radius, radius, math.pi / 2, math.pi)

    # Top left corner
    ctx.line_to(x, y + radius)
    ctx.arc(x + radius, y + radius, radius, math.pi, 3 * math.pi / 2)

    ctx.close_path()

    draw_stroke_or_fill(ctx, fill=fill, stroke=stroke)


# todo: make a position class
# pylint: disable=too-many-arguments
def draw_text(
    ctx: cairo.Context,
    *,
    text: str,
    x: float,
    y: float,
    width: float | None = None,
    height: float,
    font_size: float,
    color: Tuple[float, float, float],
    center: bool = False,
) -> None:
    """Draw text."""
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    ctx.set_source_rgb(*color)

    text_extents = ctx.text_extents(text)
    _width = width or 0
    text_x = round(
        x - (text_extents.width / 2 + text_extents.x_bearing) + _width / 2
        if center
        else x
    )
    text_y = round(y - (text_extents.height / 2 + text_extents.y_bearing) + height / 2)

    ctx.move_to(text_x, text_y)
    ctx.show_text(text)
