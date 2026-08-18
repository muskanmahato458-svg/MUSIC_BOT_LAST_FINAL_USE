import random
import html as _html

_SMALLCAPS = {
    "a": "ᴧ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "є", "f": "ғ", "g": "ɢ",
    "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ϻ", "n": "η",
    "o": "σ", "p": "ᴩ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "υ",
    "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ",
}

# Processing / "searching" ke waqt dikhne wala random emoji (sirf emoji, koi text nahi)
PROCESSING_EMOJIS = ["🧪", "🦋", "🔍"]


def smallcaps(text: str) -> str:
    """Har letter ko smallcaps mein badalta hai (lowercase style — labels ke liye)."""
    return "".join(_SMALLCAPS.get(ch.lower(), ch) if ch.isalpha() else ch for ch in text)


def smallcaps_title(text: str) -> str:
    """Har word ka pehla letter normal capital, baaki smallcaps — headings ke liye."""
    out = []
    new_word = True
    for ch in text:
        if ch.isalpha():
            out.append(ch.upper() if new_word else _SMALLCAPS.get(ch.lower(), ch))
            new_word = False
        else:
            out.append(ch)
            new_word = ch in " -_/\n"
    return "".join(out)


def fancy_italic(text: str) -> str:
    """A-Z/a-z ko Mathematical Sans-Serif Bold Italic unicode mein badalta hai
    (jaise 𝙌𝙪𝙚𝙚𝙣 𝙭 𝙢𝙪𝙨𝙞𝙘 style) — baaki characters (space, emoji) waise hi rehte hain."""
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr(0x1D63C + (ord(ch) - ord("A"))))
        elif "a" <= ch <= "z":
            out.append(chr(0x1D656 + (ord(ch) - ord("a"))))
        else:
            out.append(ch)
    return "".join(out)


def random_processing_text() -> str:
    """Sirf ek random emoji deta hai (3 me se) — koi text nahi."""
    return random.choice(PROCESSING_EMOJIS)


def format_duration(seconds) -> str:
    """Seconds ko MM:SS ya H:MM:SS format mein badalta hai. Already-string ho to wahi wapas."""
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return str(seconds) if seconds else "??:??"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def duration_to_seconds(duration_str: str) -> int:
    """'4:38' ya '1:04:38' jaisi string ko seconds mein badalta hai."""
    if not duration_str:
        return 0
    parts = str(duration_str).split(":")
    try:
        parts = [int(p) for p in parts]
    except ValueError:
        return 0
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def esc(text) -> str:
    """Dynamic text (song title, user name, etc) ko HTML-safe banata hai, taaki
    blockquote/expandable_blockquote ke andar daalne par `<`/`&` jaise
    characters formatting todd na de."""
    return _html.escape(str(text), quote=False)


def blockquote(text: str) -> str:
    """Telegram ka native ' blockquote (quote-style box, chhoti quote-icon
    ke saath) — jaise screenshot mein 'PLAYBACK ACTIVATED' waala box."""
    return f"<blockquote>{text}</blockquote>"


def expandable_blockquote(text: str) -> str:
    """Collapsible/expandable blockquote — chhota dikhta hai, arrow (⌄) tap
    karne par pura content expand hota hai (jaise screenshot ke 'MELODY'
    details box mein dikha tha)."""
    return f"<blockquote expandable>{text}</blockquote>"


def format_uptime(seconds) -> str:
    """Seconds ko 'ʜʜ:ᴍᴍ:ss' jaisa smallcaps uptime string banata hai
    (jaise '12ʜ:4ᴍ:10s') — Now Playing/group start message ke liye."""
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        seconds = 0
    h, rem = divmod(max(seconds, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{h}ʜ:{m}ᴍ:{s}s"
        
