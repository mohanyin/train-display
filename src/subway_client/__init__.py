# pylint: disable=import-error
"""Client for fetching subway times from the MTA API."""

from typing import Dict, List

import requests
from google.transit import gtfs_realtime_pb2

FEED_NQRW = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"
FEED_BDFM = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"
FEED_123 = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"


def fetch_subway_data(feed_url: str) -> gtfs_realtime_pb2.FeedMessage:
    """Fetch subway data from the MTA API."""
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(feed_url, timeout=10)
    feed.ParseFromString(response.content)
    return feed


def get_subway_data_for_stop(
    feed: gtfs_realtime_pb2.FeedMessage, stop_id: str, route_id: str
) -> List[int]:
    """Get subway data for a specific stop."""
    times = []

    for entity in feed.entity:
        if (
            entity.HasField("trip_update")
            and entity.trip_update.stop_time_update
            and entity.trip_update.trip.route_id == route_id
        ):
            for stop_time_update in entity.trip_update.stop_time_update:
                if (
                    stop_time_update.stop_id == stop_id
                    and entity.trip_update.trip.route_id == route_id
                ):
                    departure_time = stop_time_update.departure.time
                    times.append(departure_time)
    times.sort()
    return times


def fetch_subway_times() -> Dict[str, List[int]]:
    """Fetch subway times for all stops."""
    data_123 = fetch_subway_data(FEED_123)
    times = {
        "B": get_subway_data_for_stop(fetch_subway_data(FEED_BDFM), "D25N", "B"),
        "Q": get_subway_data_for_stop(fetch_subway_data(FEED_NQRW), "D25N", "Q"),
        "2": get_subway_data_for_stop(data_123, "237N", "2"),
        "3": get_subway_data_for_stop(data_123, "237N", "3"),
    }
    return times
