from core_client import fetch_resources, send_measurement
from prober import check_resource


def run_once() -> None:
    resources = fetch_resources()
    for res in resources:
        outcome = check_resource(res["url"])
        send_measurement(res["_id"], outcome)
        print(f"{res['_id']}: {outcome['result']}")
        

if __name__ == "__main__":
    run_once()