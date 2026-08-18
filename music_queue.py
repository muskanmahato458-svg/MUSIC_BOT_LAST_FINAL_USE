"""
Har chat ke liye music queue aur current-playing track memory mein rakhta hai.
Bot restart hone par yeh khali ho jaata hai — jo ki theek hai, kyunki VC bhi
restart ke baad dobara se join karni padegi.
"""

# chat_id -> list of track dicts: {video_id, title, duration, thumbnail, requested_by, stream_url}
_queues: dict[int, list] = {}

# chat_id -> currently playing track dict (ya None)
_now_playing: dict[int, dict] = {}

# chat_id -> "playing" | "paused"
_state: dict[int, str] = {}

# chat_id -> autoplay on/off (⚙️ More Settings -> Toggle Autoplay button ke liye)
_autoplay: dict[int, bool] = {}

# chat_id -> recently played video_ids (autoplay same gaana dobara na chune isliye)
_recent: dict[int, list] = {}
_RECENT_LIMIT = 15


def get_queue(chat_id: int) -> list:
    return _queues.setdefault(chat_id, [])


def push(chat_id: int, track: dict) -> int:
    """Queue ke end mein track daalta hai, uska position (1-indexed) return karta hai."""
    q = get_queue(chat_id)
    q.append(track)
    return len(q)


def pop_next(chat_id: int):
    """Queue se agla track nikaal kar deta hai, agar khali hai to None."""
    q = get_queue(chat_id)
    if not q:
        return None
    return q.pop(0)


def set_now_playing(chat_id: int, track):
    if track is None:
        _now_playing.pop(chat_id, None)
        _state.pop(chat_id, None)
    else:
        _now_playing[chat_id] = track
        _state[chat_id] = "playing"


def get_now_playing(chat_id: int):
    return _now_playing.get(chat_id)


def is_playing(chat_id: int) -> bool:
    return chat_id in _now_playing


def set_state(chat_id: int, state: str):
    _state[chat_id] = state


def get_state(chat_id: int) -> str:
    return _state.get(chat_id, "playing")


def clear(chat_id: int):
    _queues.pop(chat_id, None)
    _now_playing.pop(chat_id, None)
    _state.pop(chat_id, None)
    _recent.pop(chat_id, None)
    # NOTE: autoplay preference jaanbujh kar clear nahi hoti (/stop ke baad
    # bhi yaad rehti hai, taaki har baar dobara ON na karna pade)


def set_autoplay(chat_id: int, value: bool):
    _autoplay[chat_id] = bool(value)


def get_autoplay(chat_id: int) -> bool:
    return _autoplay.get(chat_id, False)


def remember_played(chat_id: int, video_id):
    """Autoplay ke liye — recently played video_ids yaad rakhta hai taaki
    turant wahi gaana dobara suggest na ho."""
    if not video_id:
        return
    hist = _recent.setdefault(chat_id, [])
    if video_id in hist:
        hist.remove(video_id)
    hist.append(video_id)
    if len(hist) > _RECENT_LIMIT:
        del hist[: len(hist) - _RECENT_LIMIT]


def recent_played(chat_id: int) -> list:
    return list(_recent.get(chat_id, []))
    
