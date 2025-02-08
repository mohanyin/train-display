"""Draw subway time image."""

import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple, TypedDict

# pylint: disable=no-member
# missing types because of C bindings
import cairo

from draw import colors, pencil

WIDTH: int = 800
HEIGHT: int = 480


class Line(TypedDict):
    """Information about a subway line."""

    name: str
    color: Tuple[float, float, float]
    background: Tuple[float, float, float]


class Status(Enum):
    """Status of a subway line."""

    OK = "ok"
    DELAYED = "delayed"


class LeaveInstructions(Enum):
    """Instructions for when to leave."""

    NOW = "now"
    SOON = "soon"
    NO_INSTRUCTIONS = "no_instructions"


def draw_station_status(ctx: cairo.Context, *, x: int, y: int, status: Status) -> None:
    """Draw the status lights of a station."""
    if status == Status.OK:
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 36,
            y=y + 100,
            width=16,
            height=16,
            radius=4,
            fill=colors.STATUS_OK,
        )
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 36,
            y=y + 124,
            width=16,
            height=16,
            radius=4,
            fill=colors.NEUTRAL_200,
        )
    else:
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 36,
            y=y + 100,
            width=16,
            height=16,
            radius=4,
            fill=colors.NEUTRAL_200,
        )
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 36,
            y=y + 124,
            width=16,
            height=16,
            radius=4,
            fill=colors.STATUS_WARNING,
        )


def draw_leave_instructions(
    ctx: cairo.Context, *, x: int, y: int, leave: LeaveInstructions
) -> None:
    """Draw the leave instructions for a station."""
    pencil.draw_rounded_rectangle(
        ctx,
        x=x + 92,
        y=y + 28,
        width=284,
        height=48,
        radius=8,
        stroke=colors.NEUTRAL_200,
    )

    leave_text_color = (
        colors.NEUTRAL_300
        if leave == LeaveInstructions.NO_INSTRUCTIONS
        else colors.NEUTRAL_900
    )
    pencil.draw_text(
        ctx,
        text="LEAVE",
        x=x + 100,
        y=y + 44,
        height=16,
        width=64,
        font_size=16,
        color=leave_text_color,
        center=True,
    )

    if leave == LeaveInstructions.NOW:
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 202,
            y=y + 36,
            width=64,
            height=32,
            radius=4,
            fill=colors.STATUS_OK,
        )
        pencil.draw_text(
            ctx,
            text="NOW",
            x=x + 202,
            y=y + 44,
            height=16,
            width=64,
            font_size=16,
            color=colors.NEUTRAL_900,
            center=True,
        )
    else:
        pencil.draw_text(
            ctx,
            text="NOW",
            x=x + 202,
            y=y + 44,
            height=16,
            width=64,
            font_size=16,
            color=colors.NEUTRAL_300,
            center=True,
        )

    if leave == LeaveInstructions.SOON:
        pencil.draw_rounded_rectangle(
            ctx,
            x=x + 304,
            y=y + 36,
            width=64,
            height=32,
            radius=4,
            fill=colors.STATUS_WARNING,
        )
        pencil.draw_text(
            ctx,
            text="SOON",
            x=x + 304,
            y=y + 44,
            height=16,
            width=64,
            font_size=16,
            color=colors.NEUTRAL_900,
            center=True,
        )
    else:
        pencil.draw_text(
            ctx,
            text="SOON",
            x=x + 304,
            y=y + 44,
            height=16,
            width=64,
            font_size=16,
            color=colors.NEUTRAL_300,
            center=True,
        )


def timestamp_to_minutes(timestamp: int) -> int:
    """Convert a timestamp to minutes until the time."""
    return (timestamp - int(datetime.now().timestamp())) // 60


def find_next_train_times(times: List[int], min_minutes: int) -> List[int] | None:
    """Find the next train times."""
    now = int(datetime.now().timestamp())
    for i, time in enumerate(times):
        if time > now + min_minutes * 60:
            return [timestamp_to_minutes(time), timestamp_to_minutes(times[i + 1])]
    return None


# pylint: disable=too-many-arguments
def draw_station(
    ctx: cairo.Context,
    *,
    x: int,
    y: int,
    station: str,
    reverseDir: str,
    line: Line,
    status: Status,
    times: Dict[str, List[int]],
    walk_time: int,
) -> None:
    """Draw all details for a station."""
    train_times = find_next_train_times(times["N"], walk_time)
    reverse_train_times = find_next_train_times(times["S"], walk_time)

    pencil.draw_circle(ctx, x=x + 20, y=y + 28, radius=24, fill=line["background"])
    pencil.draw_text(
        ctx,
        text=line["name"],
        x=x + 20,
        y=y + 28,
        width=48,
        height=48,
        font_size=32,
        color=line["color"],
        center=True,
    )

    if train_times is not None and train_times[0] < walk_time + 2:
        draw_leave_instructions(ctx, x=x, y=y, leave=LeaveInstructions.NOW)
    elif train_times is not None and train_times[0] < walk_time + 5:
        draw_leave_instructions(ctx, x=x, y=y, leave=LeaveInstructions.SOON)
    else:
        draw_leave_instructions(ctx, x=x, y=y, leave=LeaveInstructions.NO_INSTRUCTIONS)
    draw_station_status(ctx, x=x, y=y, status=status)

    pencil.draw_rounded_rectangle(
        ctx,
        x=x + 92,
        y=y + 124,
        width=184,
        height=92,
        radius=8,
        fill=colors.NEUTRAL_000,
    )
    pencil.draw_text(
        ctx,
        text=station,
        x=x + 92,
        y=y + 100,
        height=16,
        font_size=16,
        color=colors.NEUTRAL_900,
    )
    minutes_until = train_times[0] if train_times is not None else "--"
    pencil.draw_text(
        ctx,
        text=str(minutes_until),
        x=x + 104,
        y=y + 136,
        height=68,
        font_size=84,
        color=colors.NEUTRAL_900,
    )
    pencil.draw_text(
        ctx,
        text="min.",
        x=x + 232,
        y=y + 160,
        height=20,
        font_size=16,
        color=colors.NEUTRAL_900,
    )

    pencil.draw_text(
        ctx,
        text="NEXT",
        x=x + 300,
        y=y + 122,
        height=16,
        font_size=12,
        color=colors.NEUTRAL_900,
    )
    minutes_until_next = train_times[1] if train_times is not None else "--"
    pencil.draw_text(
        ctx,
        text=str(minutes_until_next) + " min.",
        x=x + 300,
        y=y + 141,
        height=16,
        font_size=16,
        color=colors.NEUTRAL_900,
    )

    pencil.draw_text(
        ctx,
        text=reverseDir,
        x=x + 300,
        y=y + 177,
        height=16,
        font_size=12,
        color=colors.NEUTRAL_900,
    )
    minutes_until_reverse = (
        reverse_train_times[0] if reverse_train_times is not None else "--"
    )
    pencil.draw_text(
        ctx,
        text=str(minutes_until_reverse) + " min.",
        x=x + 300,
        y=y + 196,
        height=16,
        font_size=16,
        color=colors.NEUTRAL_900,
    )


def generate_subway_time_image(
    times: Dict[str, Dict[str, List[int]]], alerts: Dict
) -> cairo.ImageSurface:
    """Generate a subway time image."""
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    ctx.set_source_rgb(*colors.NEUTRAL_100)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    draw_station(
        ctx,
        x=0,
        y=0,
        station="WAKEFIELD - 241ST",
        reverseDir="FLATBUSH",
        line={
            "name": "2",
            "color": colors.NEUTRAL_000,
            "background": colors.SUBWAY_RED,
        },
        status=Status.OK if alerts["2"] is None else Status.DELAYED,
        times={
            "N": times["N"]["2"],
            "S": times["S"]["2"],
        },
        walk_time=10,
    )
    draw_station(
        ctx,
        x=0,
        y=HEIGHT // 2,
        station="HARLEM - 148 ST",
        reverseDir="NEW LOTS",
        line={
            "name": "3",
            "color": colors.NEUTRAL_000,
            "background": colors.SUBWAY_RED,
        },
        status=Status.OK if alerts["3"] is None else Status.DELAYED,
        times={
            "N": times["N"]["3"],
            "S": times["S"]["3"],
        },
        walk_time=10,
    )
    draw_station(
        ctx,
        x=WIDTH // 2,
        y=0,
        station="145 ST",
        reverseDir="BRIGHTON",
        line={
            "name": "B",
            "color": colors.NEUTRAL_000,
            "background": colors.SUBWAY_ORANGE,
        },
        status=Status.OK if alerts["B"] is None else Status.DELAYED,
        times={
            "N": times["N"]["B"],
            "S": times["S"]["B"],
        },
        walk_time=8,
    )
    draw_station(
        ctx,
        x=WIDTH // 2,
        y=HEIGHT // 2,
        station="96 ST",
        reverseDir="CONEY ISL",
        line={
            "name": "Q",
            "color": colors.NEUTRAL_900,
            "background": colors.SUBWAY_YELLOW,
        },
        status=Status.OK if alerts["Q"] is None else Status.DELAYED,
        times={
            "N": times["N"]["Q"],
            "S": times["S"]["Q"],
        },
        walk_time=8,
    )

    return surface


def create_subway_time_image(
    output_path: str, times: Dict[str, Dict[str, List[int]]], alerts: Dict
) -> None:
    """Create a subway time image and save it to the specified path.

    Args:
        output_path: The path where the image will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    surface = generate_subway_time_image(times, alerts)
    surface.write_to_png(output_path)
