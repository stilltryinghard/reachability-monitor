from prober import check_resource
from sender import send_measurement

#пока список ресурсов захардкодил
RESOURCES = [
    {"resource_id": "github", "url": "https://github.com"},
]


def run_once() -> None:
    for res in RESOURCES:
        outcome = check_resource(res["url"])
        send_measurement(res["resource_id"], outcome)
        print(f"{res['resource_id']}: {outcome['result']}")
        

if __name__ == "__main__":
    run_once()