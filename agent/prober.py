import httpx


def check_resource(url: str) -> dict:
    """Проверка доступности ресурса по указанному URL"""
    try:
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url, timeout=10)
        return {
            "result": "ok",
            "details": {
                "status_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "redirected": len(response.history) > 0,
                "redirect_chain": [str(r.url) for r in response.history],
                "final_url": str(response.url),
            },
        }
    except httpx.TimeoutException:
        return {"result": "timeout", "details": {"error": "timeout"}}
    except httpx.ConnectError:
        return {"result": "connection_error", "details": {"error": "connection_refused"}}
    except httpx.RequestError:
        return {"result": "request_error", "details": {"error": "network error"}}