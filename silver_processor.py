from pathlib import Path
import json


BRONZE_DIR = Path("bronze")
BRONZE_DIR.mkdir(exist_ok=True)


def read_bronze_events() -> list[dict[str, str | int]]:
    """
    Read each file in bronze and return all the events in a list
    """

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


def is_valid_event(event: dict[str, str | int]) -> bool:
    """
    Returns if the event object is valid based on rules
    """

    eventid_exists = "event_id" in event and event["event_id"] is not None
    units_exists = "units" in event and type(event["units"]) == int and event["units"] > 0
    timestamp_exists = "timestamp" in event

    return eventid_exists and units_exists and timestamp_exists


def deduplicate_events(events: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    """
    Deduplicates events and returns a list of unique events based on event ids
    """

    unique_event_ids = set()
    unique_events = []

    for event in events:
        eventid_exists = "event_id" in event and event["event_id"] is not None

        if eventid_exists and event["event_id"] not in unique_event_ids:
            unique_event_ids.add(event["event_id"])
            unique_events.append(event)

    return unique_events

def write_silver_events(events: list[dict[str, str | int]]) -> None:
    """
    Writes events to silver layer
    """

    SILVER_DIR = Path("silver")
    SILVER_DIR.mkdir(exist_ok=True)

    output_file = SILVER_DIR / "processed_events.json"
    with open(output_file, "w") as o:
        for event in events:
            json.dump(event, o)
            o.write("\n")

    return

if __name__ == "__main__":
    bronze_events = read_bronze_events()
    total_read = len(bronze_events)

    valid_events = []

    for event in bronze_events:
        if is_valid_event(event):
            valid_events.append(event)

    valid_events = deduplicate_events(valid_events)
    valid_kept = len(valid_events)

    write_silver_events(valid_events)

    print("Total read:", total_read)
    print("Valid Events:", valid_kept)
    print("Events dropped:", total_read - valid_kept)

