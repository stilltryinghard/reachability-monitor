import httpx

import buffer
import core_client
from prober import check_resource


def flush_buffer() -> None:
    """Дослать накопленное из буфера. При обрыве - остановиться, сохранить хвост"""
    pending = buffer.read_all()
    if not pending:
        return
    not_sent = []
    stopped = False
    for i, payload in enumerate(pending):
        if stopped:
            not_sent.append(payload) # после обрыва — всё в хвост, не пытаемся
            continue
        try:
            core_client.send_payload(payload)
        except httpx.ConnectError:
            not_sent.append(payload) # этот не ушёл
            stopped = True    # канал лёг, дальше не шлём
    buffer.replace_all(not_sent)
    
    
def run_once() -> None:
    # 1. Сначала пробуем дослать буфер (вдруг канал вернулся)
    flush_buffer()
    
    #2. Тянем список ресурсов.
    resources = core_client.fetch_resources()
    
    # 3. Мерим и шлем каждый. при обрыве - в буфер.
    for res in resources:
        outcome = check_resource(res["url"])
        payload = core_client.build_payload(res["_id"], outcome)
        try:
            core_client.send_payload(payload)
            print(f"{res['_id']}: {outcome['result']} (sent)")
        except httpx.ConnectError:
            buffer.add(payload)
            print(f"{res['_id']}: {outcome['result']} (buffered)")
            
            
if __name__ == "__main__":
    run_once()