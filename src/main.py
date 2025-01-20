"""Create black images using Cairo."""

import os
import sys

# pylint: disable=no-member
# missing types because of C bindings
import cairo

WIDTH: int = 800
HEIGHT: int = 480


def create_black_image(output_path: str) -> None:
    """Create a black image and save it to the specified path.

    Args:
        output_path: The path where the image will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create a new surface
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    # Fill the entire surface with black
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    # Save the image
    surface.write_to_png(output_path)


def main() -> None:
    """Process the command line arguments and create a black image."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    create_black_image(output_path)
    print(f"Black image saved to: {output_path}")


if __name__ == "__main__":
    main()
