"""Create subway time images."""

import time
import logging

import draw
import subway_client
from display_connector import DisplayConnector

logger = logging.getLogger(__name__)
output_path = "outputs/output.png"


def main() -> None:
    """Check subway times, generate image, and write to display"""

    display_connector = DisplayConnector()
    display_connector.init()

    while True:
        try:
            times = subway_client.fetch_subway_times()
            alerts = subway_client.fetch_status_data()

            draw.create_subway_time_image(output_path, times, alerts)
            logger.info(f"Subway time image saved to: {output_path}")
            display_connector.display_image(output_path)

            time.sleep(60)
        except KeyboardInterrupt:    
            display_connector.cleanup()
            exit()
        except Exception as e:
            logger.warning(e)


if __name__ == "__main__":
    main()
