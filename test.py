# app.py
import streamlit as st
import random
import re
from urllib.parse import urlparse, parse_qs

# ===== 기본 설정 =====
st.set_page_config(page_title="Mood Music 🎵", page_icon="🎧", layout="centered")

st.title("🎼 Mood Music — 기분 기반 음악 추천기")
st.caption("기분과 강도를 선택하면, K-POP 포함 맞춤 노래를 추천해드려요! 💖")

# ===== 유틸 =====
YOUTUBE_THUMB = "https://img.youtube.com/vi/{}/hqdefault.jpg"

def extract_youtube_id(url: str) -> str | None:
    """
    다양한 유튜브 URL에서 영상 ID를 추출합니다.
    지원: youtu.be/<id>, youtube.com/watch?v=<id>, youtube.com/shorts/<id>
    """
    try:
        u = urlparse(url)
        if u.netloc in ("youtu.be", "www.youtu.be"):
            return u.path.strip("/")

        if "youtube.com" in u.netloc:
            # /watch?v=, /shorts/<id>
            if u.path.startswith("/watch"):
                q = parse_qs(u.query)
                return q.get("v", [None])[0]
            if u.path.startswith("/shorts/"):
                return u.path.split("/shorts/")[1].split("/")[0]
    except Exception:
        pass
    # 백업: 정규식
    m = re.search(r"(?:v=|be/|shorts/)([A-Za-z0-9_\-]{6,})", url)
    return m.group(1) if m else None

def show_card(title: str, url: str, tag: str):
    vid = extract_youtube_id(url)
    thumb = YOUTUBE_THUMB.format(vid) if vid else None
    with st.container(border=True):
        cols = st.columns([1, 2])
        with cols[0]:
            if thumb:
                st.image(thumb, use_container_width=True)
            else:
                st.write("🎵")
        with cols[1]:
            st.markdown(f"**{title}**  {tag}")
            st.markdown(f"[유튜브에서 듣기 ▶️]({url})")

def pick_songs(pool: list[dict], k: int) -> list[dict]:
    """중복 없이 k개 샘플링 (pool이 적으면 가능한 만큼)"""
    if len(pool) <= k:
        random.shuffle(pool)
        return pool
    return random.sample(pool, k)

# ===== 데이터 스키마 =====
# 항목: {"title": "...", "url": "...", "mood": "행복/슬픔/화남/평온/설렘/생각/피곤", "intensity": "low|high", "kpop": bool}
songs: list[dict] = [
    # === 행복 😀 ===
    {"title": "Pharrell Williams - Happy", "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs", "mood": "행복", "intensity": "high", "kpop": False},
    {"title": "Katrina & The Waves - Walking on Sunshine", "url": "https://www.youtube.com/watch?v=iPUmE-tne5U", "mood": "행복", "intensity": "high", "kpop": False},
    {"title": "Bruno Mars - Uptown Funk", "url": "https://www.youtube.com/watch?v=OPf0YbXqDm0", "mood": "행복", "intensity": "high", "kpop": False},
    {"title": "Jason Mraz - I'm Yours", "url": "https://www.youtube.com/watch?v=EkHTsc9PU2A", "mood": "행복", "intensity": "low", "kpop": False},
    {"title": "Maroon 5 - Sugar", "url": "https://www.youtube.com/watch?v=09R8_2nJtjg", "mood": "행복", "intensity": "low", "kpop": False},
    # 행복 K-POP
    {"title": "BTS - Dynamite", "url": "https://www.youtube.com/watch?v=gdZLi9oWNZg", "mood": "행복", "intensity": "high", "kpop": True},
    {"title": "NewJeans - Super Shy", "url": "https://www.youtube.com/watch?v=ArmDp-zijuc", "mood": "행복", "intensity": "high", "kpop": True},
    {"title": "IVE - I AM", "url": "https://www.youtube.com/watch?v=6ZUIwj3FgUY", "mood": "행복", "intensity": "high", "kpop": True},
    {"title": "RIIZE - Get A Guitar", "url": "https://www.youtube.com/watch?v=brP0xJ8pn6o", "mood": "행복", "intensity": "low", "kpop": True},
    {"title": "TWICE - ONE SPARK", "url": "https://www.youtube.com/watch?v=6eEZ7DJMzuk", "mood": "행복", "intensity": "low", "kpop": True},

    # === 슬픔 😢 ===
    {"title": "Adele - Someone Like You", "url": "https://www.youtube.com/watch?v=hLQl3WQQoQ0", "mood": "슬픔", "intensity": "high", "kpop": False},
    {"title": "Billie Eilish - everything i wanted", "url": "https://www.youtube.com/watch?v=EgBJmlPo8Xw", "mood": "슬픔", "intensity": "low", "kpop": False},
    {"title": "Lewis Capaldi - Someone You Loved", "url": "https://www.youtube.com/watch?v=bCuhuePlP8o", "mood": "슬픔", "intensity": "high", "kpop": False},
    # 슬픔 K-POP
    {"title": "아이유 - 밤편지", "url": "https://www.youtube.com/watch?v=BzYnNdJhZQw", "mood": "슬픔", "intensity": "low", "kpop": True},
    {"title": "BIBI - Bam Yang Gang (밤양갱)", "url": "https://www.youtube.com/watch?v=3eC3z8vKxxA", "mood": "슬픔", "intensity": "low", "kpop": True},
    {"title": "JUNGKOOK - Seven (feat. Latto)", "url": "https://www.youtube.com/watch?v=QU9c0053UAU", "mood": "슬픔", "intensity": "high", "kpop": True},

    # === 화남 😡 ===
    {"title": "Eminem - Lose Yourself", "url": "https://www.youtube.com/watch?v=_Yhyp-_hX2s", "mood": "화남", "intensity": "high", "kpop": False},
    {"title": "Linkin Park - Numb", "url": "https://www.youtube.com/watch?v=kXYiU_JCYtU", "mood": "화남", "intensity": "high", "kpop": False},
    {"title": "Billie Eilish - bad guy", "url": "https://www.youtube.com/watch?v=DyDfgMOUjCI", "mood": "화남", "intensity": "low", "kpop": False},
    # 화남 K-POP
    {"title": "(G)I-DLE - Super Lady", "url": "https://www.youtube.com/watch?v=RbS9mO9CfBM", "mood": "화남", "intensity": "high", "kpop": True},
    {"title": "LE SSERAFIM - Eve, Psyche & The Bluebeard’s wife", "url": "https://www.youtube.com/watch?v=UBURTj20HXI", "mood": "화남", "intensity": "high", "kpop": True},
    {"title": "Stray Kids - LALALALA", "url": "https://www.youtube.com/watch?v=JsOOis4bBFg", "mood": "화남", "intensity": "high", "kpop": True},

    # === 편안 😌 ===
    {"title": "Norah Jones - Don’t Know Why", "url": "https://www.youtube.com/watch?v=tO4dxvguQDk", "mood": "편안", "intensity": "low", "kpop": False},
    {"title": "Coldplay - Fix You", "url": "https://www.youtube.com/watch?v=k4V3Mo61fJM", "mood": "편안", "intensity": "high", "kpop": False},
    {"title": "Lauv - Paris in the Rain", "url": "https://www.youtube.com/watch?v=GgELa5RMy2w", "mood": "편안", "intensity": "low", "kpop": False},
    # 편안 K-POP
    {"title": "Crush - Beautiful", "url": "https://www.youtube.com/watch?v=-FlxM_0S2lA", "mood": "편안", "intensity": "low", "kpop": True},
    {"title": "AKMU - Love Lee", "url": "https://www.youtube.com/watch?v=Uo9Fz6FQxAg", "mood": "편안", "intensity": "low", "kpop": True},
    {"title": "NewJeans - How Sweet", "url": "https://www.youtube.com/watch?v=Q3x-bx3Hix0", "mood": "편안", "intensity": "high", "kpop": True},

    # === 설렘 😍 ===
    {"title": "Taylor Swift - Love Story", "url": "https://www.youtube.com/watch?v=8xg3vE8Ie_E", "mood": "설렘", "intensity": "high", "kpop": False},
    {"title": "Bruno Mars - Just The Way You Are", "url": "https://www.youtube.com/watch?v=LjhCEhWiKXk", "mood": "설렘", "intensity": "low", "kpop": False},
    # 설렘 K-POP
    {"title": "ILLIT - Magnetic", "url": "https://www.youtube.com/watch?v=3j7JPyVT2D8", "mood": "설렘", "intensity": "high", "kpop": True},
    {"title": "SEVENTEEN - Super", "url": "https://www.youtube.com/watch?v=-GQg25oP0S4", "mood": "설렘", "intensity": "high", "kpop": True},
    {"title": "ZICO - SPOT! (feat. JENNIE)", "url": "https://www.youtube.com/watch?v=5cZP3Xjs4sQ", "mood": "설렘", "intensity": "high", "kpop": True},

    # === 생각 많음 🤔 ===
    {"title": "Radiohead - Creep", "url": "https://www.youtube.com/watch?v=XFkzRNyygfk", "mood": "생각", "intensity": "high", "kpop": False},
    {"title": "Lauv - Modern Loneliness", "url": "https://www.youtube.com/watch?v=TA4EklQ_-vY", "mood": "생각", "intensity": "low", "kpop": False},
    # 생각 K-POP
    {"title": "IU - Love wins all", "url": "https://www.youtube.com/watch?v=oxKCPjcvbys", "mood": "생각", "intensity": "low", "kpop": True},
    {"title": "WOODZ - Journey", "url": "https://www.youtube.com/watch?v=N2nO5r0VBR0", "mood": "생각", "intensity": "high", "kpop": True},

    # === 피곤 🥱 ===
    {"title": "John Legend - All of Me", "url": "https://www.youtube.com/watch?v=450p7goxZqg", "mood": "피곤", "intensity": "high", "kpop": False},
    {"title": "Ed Sheeran - Photograph", "url": "https://www.youtube.com/watch?v=nSDgHBxUbVQ", "mood": "피곤", "intensity": "low", "kpop": False},
    # 피곤 K-POP
    {"title": "백예린 - 그건 아마 우리의 잘못은 아닐 거야", "url": "https://www.youtube.com/watch?v=2GI8l2554xM", "mood": "피곤", "intensity": "low", "kpop": True},
    {"title": "태연 - 그대라는 시", "url": "https://www.youtube.com/watch?v=VYOjWnS4cMY", "mood": "피곤", "intensity": "low", "kpop": True},

    # === 요즘 K-POP 핫 트랙 (분산 배치 외 추가 슬롯) ===
    {"title": "aespa - Supernova", "url": "https://www.youtube.com/watch?v=Os_heh8vPfs", "mood": "행복", "intensity": "high", "kpop": True},
    {"title": "TXT - Deja Vu", "url": "https://www.youtube.com/watch?v=UaI2Zg8EoK0", "mood": "설렘", "intensity": "high", "kpop": True},
]

# ===== 사이드바: 옵션 =====
with st.sidebar:
    st.header("🎛️ 추천 옵션")
    mood = st.selectbox(
        "지금 기분은 어떤가요? 🌈",
        ["😀 행복해요", "😢 슬퍼요", "😡 화나요", "😌 편안해요", "😍 설레요", "🤔 생각이 많아요", "🥱 피곤해요"]
    )
    score = st.slider("감정 강도 (0~100) 🎚️", 0, 100, 60)
    only_kpop = st.checkbox("K-POP만 보기 🇰🇷", value=False)
    n_recs = st.slider("추천 개수 (1~5) 🎵", 1, 5, 3)
    seed_opt = st.checkbox("랜덤 고정(재현성)", value=False)
    seed_val = st.number_input("시드 값", min_value=0, value=42, step=1, disabled=not seed_opt)
    st.markdown("---")
    reroll = st.button("🔁 다시 추천 받기")

if seed_opt:
    random.seed(int(seed_val))
elif reroll:
    # reroll 클릭 때마다 시드를 달리해 변화를 유도
    random.seed()

# ===== 필터링 로직 =====
mood_map = {
    "😀 행복해요": "행복",
    "😢 슬퍼요": "슬픔",
    "😡 화나요": "화남",
    "😌 편안해요": "편안",
    "😍 설레요": "설렘",
    "🤔 생각이 많아요": "생각",
    "🥱 피곤해요": "피곤",
}
mood_key = mood_map[mood]
intensity_key = "high" if score >= 50 else "low"

pool = [s for s in songs if s["mood"] == mood_key and s["intensity"] == intensity_key]
if only_kpop:
    pool = [s for s in pool if s["kpop"]]

# 백업: 해당 강도에 곡이 부족하면 반대 강도에서 보충
if len(pool) < n_recs:
    alt = [s for s in songs if s["mood"] == mood_key and s["intensity"] != intensity_key]
    if only_kpop:
        alt = [s for s in alt if s["kpop"]]
    pool = pool + alt

st.markdown("---")
emoji_title = {
    "행복": "😀",
    "슬픔": "😢",
    "화남": "😡",
    "편안": "😌",
    "설렘": "😍",
    "생각": "🤔",
    "피곤": "🥱",
}.get(mood_key, "🎵")

st.subheader(f"{emoji_title} 오늘의 추천 음악 Top {n_recs}")

if not pool:
    st.info("조건에 맞는 곡이 아직 없네요. 옵션을 바꿔보거나 K-POP 전용을 해제해보세요!")
else:
    picks = pick_songs(pool, n_recs)
    for s in picks:
        tag = "🇰🇷 K-POP" if s["kpop"] else "🌍 Global"
        show_card(s["title"], s["url"], f"`{tag}`")

# ===== 푸터 =====
st.markdown("---")
st.caption(
    "🔎 팁: 사이드바에서 감정 강도/추천 개수/랜덤 고정을 바꿔보세요. "
    "유튜브 썸네일은 공개 미리보기를 사용합니다."
)
