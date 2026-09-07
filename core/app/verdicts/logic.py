from datetime import datetime, timedelta


def decide_verdict(
    external: dict | None, #Последний замер снаружи
    internal: dict | None, #Последний замер внутри
    now: datetime, #Текущее время - для проверки свежести замера
    freshness_sec: int = 300, #порог свежести - 5 минут
) -> str:
    """
    Функция принимает на вход два замера и текущее время и возвращает вердикт о доступности ресурса."""

    #С Снаружи не мерили - судитиь не о чем.
    if external is None:
        return "no_data"
    
    
    # Изнутри замера нет или он протух - не можем судить про РФ
    if internal is None:
        return "no_data"
    if (now - internal["measured_at"]) > timedelta(seconds=freshness_sec):
        return "no_data"
    
    # Оба замера есть и внутренний свежий - сравниваем
    external_ok = external["result"] == "ok"
    internal_ok = internal["result"] == "ok"
    
    if not external_ok:
        return "down"
    if internal_ok:
        return "available"
    return "blocked"