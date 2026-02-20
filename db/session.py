import redis
from typing import Any
import json, pickle
import os

r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=False
)

def get_session(session_id: str):
    if r.exists(session_id) == 0:
        return []
    else:
        return pickle.loads(r.get(session_id))
    
def set_session(session_id: str, history: list[Any]):
    r.set(session_id, pickle.dumps(history))
