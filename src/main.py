"""Create subway time images."""

import time

import draw
from subway_client import fetch_status_data, fetch_subway_times
from display_connector import init, display_image, cleanup


def main() -> None:
    """Process the command line arguments and create a black image."""

    output_path = "outputs/output.png"

    init()

    while True:
        try:
            times = fetch_subway_times()
            alerts = fetch_status_data()

            draw.create_subway_time_image(output_path, times, alerts)
            print(f"Subway time image saved to: {output_path}")
            display_image(output_path)

            time.sleep(60)
        except KeyboardInterrupt:    
            cleanup()
            exit()


if __name__ == "__main__":
    main()
