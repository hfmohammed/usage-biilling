from pathlib import Path
import json


BRONZE_DIR = Path("bronze")
BRONZE_DIR.mkdir(exist_ok=True)


def read_bronze_events() -> list[dict[str, str]]:
    events = []
    event_files = [p for p in BRONZE_DIR.iterdir() if p.is_file() and p.name.startswith("events_")]
    for event_file in event_files:
        with open(event_file) as file_input:
            while True:
                event_str = file_input.readline().strip()
                if not event_str:
                    break

                event_json = json.loads(event_str)
                events.append(event_json)
    
    
    print(type(events[0]), events[0])
    return events


def is_valid_event(event: dict[str, str]) -> bool:
    eventid_exists = "event_id" in event and event["event_id"] is not None
    units_exists = "units" in event and type(event["units"]) == int and event["units"] > 0
    timestamp_exists = "timestamp" in event
    return eventid_exists and units_exists and timestamp_exists


if __name__ == "__main__":
    bronze_events = read_bronze_events()
    for i in bronze_events:
        print(is_valid_event(i))