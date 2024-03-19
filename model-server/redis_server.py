from redis import Redis
from json import dumps, loads

redis_server = Redis(host='localhost', port=6379, decode_responses=True)


def save_session(session_id: str, data):
    return redis_server.set(f"session:{session_id}", dumps({
        "session_id": session_id,
        **data
    }))

def get_session(session_id: str):
    data = redis_server.get(f"session:{session_id}")

    return loads(data)