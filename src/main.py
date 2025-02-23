"""Create subway time images."""

import time
import logging

import draw
from subway_client import fetch_status_data, fetch_subway_times
from display_connector import init, display_image, cleanup

logger = logging.getLogger(__name__)


def main() -> None:
    """Process the command line arguments and create a black image."""

    output_path = "outputs/output.png"

    init()

    while True:
        try:
            times = fetch_subway_times()
            alerts = fetch_status_data()

            draw.create_subway_time_image(output_path, times, alerts)
            logger.info(f"Subway time image saved to: {output_path}")
            display_image(output_path)

            time.sleep(60)
        except KeyboardInterrupt:    
            cleanup()
            exit()
        except Exception as e:
            logger.warning(e)


if __name__ == "__main__":
    main()
