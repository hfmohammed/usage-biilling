import uuid
import datetime
from pathlib import Path
import json


BRONZE_DIR = Path("bronze")
BRONZE_DIR.mkdir(exist_ok=True)


def generate_event() -> dict[str, str | int]:
    """
    Generate random event
    """

    event = {
        "event_id": str(uuid.uuid4()),
        "customer_id": "customer_0",
        "service": "api_req",
        "units": 23,
        "timestamp": datetime.datetime.now().isoformat()
    }

    return event


def write_event(event: dict[str, str | int]) -> None:
    """
    output the event to Bronze layer
    
    :param event: event object
    :type event: dict[str, str]
    """

    date = event["timestamp"].split("T")[0]
    file_path = BRONZE_DIR / f"events_{date}.json"

    print(file_path)
    with open(file_path, "a") as f:
        json.dump(event, f)
        f.write("\n")

    return


if __name__ == "__main__":
    event = generate_event()
    write_event(event)
