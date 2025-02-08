# pylint: disable=import-error
"""Client for fetching subway times from the MTA API."""

from datetime import datetime
from typing import Dict, List

import requests
from google.transit import gtfs_realtime_pb2

FEED_NQRW = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"
FEED_BDFM = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"
FEED_123 = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"

STATUS_URL = (
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json"
)


def find_alert_for_line(line: str, alerts: Dict) -> Dict | None:
    """Find the alert for a given line."""
    for alert in alerts:
        entities = alert["alert"]["informed_entity"]
        for entity in entities:
            now = int(datetime.now().timestamp())
            active_period = alert["alert"].get("active_period", [None])[0]
            if entity.get("route_id") == line and entity.get("agency_id") == "MTASBWY":
                if active_period is None or (
                    active_period.get("start", 0)
                    <= now
                    <= active_period.get("end", float("inf"))
                ):
                    return alert["alert"]
    return None


def fetch_status_data() -> Dict:
    """Fetch status data from the MTA API."""
    response = requests.get(STATUS_URL, timeout=10).json()
    alerts = response["entity"]
    return {
        "2": find_alert_for_line("2", alerts),
        "3": find_alert_for_line("3", alerts),
        "B": find_alert_for_line("B", alerts),
        "Q": find_alert_for_line("Q", alerts),
    }


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
                departure_time = stop_time_update.departure.time
                if (
                    stop_time_update.stop_id == stop_id
                    and entity.trip_update.trip.route_id == route_id
                    and departure_time > int(datetime.now().timestamp())
                ):
                    times.append(departure_time)
    times.sort()
    return times


def fetch_subway_times() -> Dict[str, Dict[str, List[int]]]:
    """Fetch subway times for all stops."""
    data_123 = fetch_subway_data(FEED_123)
    data_bdfm = fetch_subway_data(FEED_BDFM)
    data_nqrw = fetch_subway_data(FEED_NQRW)

    times = {
        "N": {
            "B": get_subway_data_for_stop(data_bdfm, "D25N", "B"),
            "Q": get_subway_data_for_stop(data_nqrw, "D25N", "Q"),
            "2": get_subway_data_for_stop(data_123, "237N", "2"),
            "3": get_subway_data_for_stop(data_123, "237N", "3"),
        },
        "S": {
            "B": get_subway_data_for_stop(data_bdfm, "D25S", "B"),
            "Q": get_subway_data_for_stop(data_nqrw, "D25S", "Q"),
            "2": get_subway_data_for_stop(data_123, "237S", "2"),
            "3": get_subway_data_for_stop(data_123, "237S", "3"),
        },
    }
    return times
