"""Create subway time images."""

import sys

import draw


def main() -> None:
    """Process the command line arguments and create a black image."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    draw.create_subway_time_image(output_path)
    print(f"Subway time image saved to: {output_path}")


if __name__ == "__main__":
    main()
