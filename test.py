# streamlit_app.py
# 실행 방법:
#   1) 이 파일을 streamlit_app.py 로 저장
#   2) 터미널에서: streamlit run streamlit_app.py
#   3) 선택: 같은 폴더에 books.csv 두면 자동으로 데이터 사용 (컬럼: title,author,category,description,image_url)

import random
import io
from typing import List, Dict

import pandas as pd
import streamlit as st

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(page_title="책 추천 앱", page_icon="📚", layout="wide")

# ----------------------
# 샘플 데이터 (books.csv 없을 때 사용)
# ----------------------
SAMPLE_DATA: List[Dict] = [
    {
        "title": "아주 작은 습관의 힘",
        "author": "제임스 클리어",
        "category": "자기계발",
        "description": "작은 습관이 인생을 바꾸는 법을 과학적으로 풀어낸 베스트셀러.",
        "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=640"
    },
    {
        "title": "달리기를 말할 때 내가 하고 싶은 이야기",
        "author": "무라카미 하루키",
        "category": "힐링/마음 치유",
        "description": "달리기를 통해 일상과 자신을 성찰하는 에세이.",
        "image_url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=640"
    },
    {
        "title": "사피엔스",
        "author": "유발 하라리",
        "category": "전문 지식",
        "description": "인류의 역사와 진화를 거시적으로 살피는 통찰.",
        "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=640"
    },
    {
        "title": "예술가처럼 훔쳐라",
        "author": "오스틴 클레온",
        "category": "창의력/영감",
        "description": "창의적으로 일하고 살아가는 10가지 원칙.",
        "image_url": "https://images.unsplash.com/photo-1496317556649-f930d733eea0?w=640"
    },
    {
        "title": "대화의 기술",
        "author": "데일 카네기",
        "category": "인간관계/커뮤니케이션",
        "description": "관계를 좋게 만드는 대화법과 태도.",
        "image_url": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=640"
    },
    {
        "title": "부의 인문학",
        "author": "김경준",
        "category": "전문 지식",
        "description": "돈과 시장을 인문학적으로 이해하는 시선.",
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=640"
    },
    {
        "title": "나는 나로 살기로 했다",
        "author": "김수현",
        "category": "힐링/마음 치유",
        "description": "타인의 기대에서 벗어나 나답게 사는 법.",
        "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=640"
    },
    {
        "title": "메모의 마법",
        "author": "마에다 유지",
        "category": "자기계발",
        "description": "메모만 잘해도 삶이 달라지는 구조화 방법.",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=640"
    },
    {
        "title": "스토리텔링의 기술",
        "author": "낸시 두아르테",
        "category": "창의력/영감",
        "description": "사람을 움직이는 프레젠테이션과 이야기 구조.",
        "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0ea?w=640"
    },
]

PLACEHOLDER_IMG = "https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?w=640"

# ----------------------
# 유틸 함수
# ----------------------

def load_books(uploaded_file) -> pd.DataFrame:
    """파일 업로드가 있으면 사용, 없으면 로컬 books.csv 시도, 둘 다 없으면 샘플 사용"""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception:
            st.warning("업로드한 CSV를 읽는 중 문제가 발생했어요. 샘플 데이터를 사용합니다.")
    # 로컬 파일 시도
    try:
        df = pd.read_csv("books.csv")
        return df
    except Exception:
        return pd.DataFrame(SAMPLE_DATA)


def sanitize_df(df: pd.DataFrame) -> pd.DataFrame:
    needed = ["title", "author", "category", "description", "image_url"]
    for col in needed:
        if col not in df.columns:
            df[col] = ""
    # 빈 이미지 처리
    df["image_url"] = df["image_url"].fillna("").replace({"": PLACEHOLDER_IMG})
    return df[needed].copy()


def add_to_wishlist(book_row: pd.Series):
    """중복 방지 후 위시리스트에 추가"""
    key = (book_row["title"], book_row["author"])
    if "wishlist" not in st.session_state:
        st.session_state["wishlist"] = {}
    if key in st.session_state["wishlist"]:
        st.toast("이미 내 책장에 있어요 🙌", icon="✅")
    else:
        st.session_state["wishlist"][key] = book_row.to_dict()
        st.toast(f"'{book_row['title']}' 추가 완료! ❤️", icon="❤️")


def remove_from_wishlist(key_tuple):
    if "wishlist" in st.session_state and key_tuple in st.session_state["wishlist"]:
        del st.session_state["wishlist"][key_tuple]
        st.toast("삭제했어요 🗑️", icon="🗑️")


def wishlist_dataframe() -> pd.DataFrame:
    items = list(st.session_state.get("wishlist", {}).values())
    return pd.DataFrame(items) if items else pd.DataFrame(columns=["title","author","category","description","image_url"])    


def download_wishlist_button():
    df = wishlist_dataframe()
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ 내 책장 CSV 다운로드", data=csv, file_name="my_wishlist.csv", mime="text/csv")
    else:
        st.caption("내 책장이 비어 있어요.")


# ----------------------
# 사이드바
# ----------------------
with st.sidebar:
    st.header("📂 데이터 불러오기")
    uploaded = st.file_uploader("books.csv 업로드 (선택)", type=["csv"])    
    st.markdown("""
    **CSV 형식 가이드**
    - 컬럼: `title, author, category, description, image_url`
    - 이미지가 없으면 자동 플레이스홀더 사용
    """)

# 데이터 로드 & 정제
raw_df = load_books(uploaded)
df = sanitize_df(raw_df)

# 앱 상태 초기화
if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = {}

# ----------------------
# 상단 제목 / 스타일
# ----------------------
st.markdown(
    """
    <style>
      .book-card {border-radius: 16px; padding: 16px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.05); height: 100%;}
      .book-title {font-weight: 800; font-size: 1.05rem;}
      .muted {opacity: 0.7; font-size: 0.9rem;}
      .desc {margin-top: .25rem; line-height: 1.5;}
      .pill {display:inline-block; padding: 4px 10px; border-radius: 999px; background: #f1f5f9; font-size: 0.8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 필요 기반 카테고리 책 추천")
st.caption("카테고리별 추천을 받고, 마음에 드는 책은 ❤️ 찜해서 '내 책장'에서 다시 확인하세요.")

# ----------------------
# 컨트롤 영역
# ----------------------
left, right = st.columns([2,1])
with left:
    categories = sorted(df["category"].dropna().unique().tolist())
    selected_cat = st.selectbox("지금 필요한 카테고리", options=categories, index=0 if categories else None)
    keywords = st.text_input("키워드(선택): 제목/설명에서 검색", placeholder="예: 습관, 동기부여, 역사…")
with right:
    n_reco = st.slider("추천 개수", 1, 9, 6)
    random_seed = st.number_input("랜덤 시드(재현성)", value=42, step=1)

random.seed(int(random_seed))

# ----------------------
# 추천 로직
# ----------------------
filtered = df[df["category"] == selected_cat] if selected_cat else df.copy()
if keywords:
    kw = keywords.strip().lower()
    mask = (
        df["title"].str.lower().str.contains(kw, na=False) |
        df["description"].str.lower().str.contains(kw, na=False)
    )
    filtered = filtered[mask]

if filtered.empty:
    st.warning("해당 조건에 맞는 책을 찾지 못했어요. 다른 카테고리나 키워드를 시도해보세요.")
else:
    # 무작위 순서 섞기 후 상위 n개
    sampled = filtered.sample(frac=1.0, random_state=random_seed).head(n_reco)

    st.subheader("🔎 추천 결과")

    # 3열 카드 레이아웃
    rows = (len(sampled) + 2) // 3
    cards = list(sampled.to_dict(orient="records"))
    idx = 0
    for _ in range(rows):
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        for c in cols:
            if idx >= len(cards):
                break
            book = cards[idx]
            with c:
                with st.container(border=False):
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    imurl = book.get("image_url") or PLACEHOLDER_IMG
                    st.image(imurl, use_column_width=True)
                    st.markdown(f"<div class='pill'>{book['category']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='book-title'>{book['title']}</div>")
                    st.markdown(f"<div class='muted'>✍️ {book['author']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='desc'>{book['description']}</div>", unsafe_allow_html=True)
                    add_key = f"add_{book['title']}_{book['author']}_{idx}"
                    if st.button("❤️ 찜하기", key=add_key, use_container_width=True):
                        add_to_wishlist(pd.Series(book))
                    st.markdown("</div>", unsafe_allow_html=True)
            idx += 1

# ----------------------
# 탭: 내 책장
# ----------------------
st.markdown("---")
st.subheader("📖 내 책장 (찜한 책)")

wdf = wishlist_dataframe()
if wdf.empty:
    st.info("아직 찜한 책이 없어요. 위에서 마음에 드는 책을 ❤️ 추가해보세요!")
else:
    # 보기/관리 옵션
    sort_by = st.selectbox("정렬 기준", ["title", "author", "category"]) 
    asc = st.toggle("오름차순", value=True)
    view_df = wdf.sort_values(by=sort_by, ascending=asc).reset_index(drop=True)

    # 다운로드 버튼
    download_wishlist_button()

    # 카드 그리드
    cards = list(view_df.to_dict(orient="records"))
    rows = (len(cards) + 2) // 3
    idx = 0
    for _ in range(rows):
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        for c in cols:
            if idx >= len(cards):
                break
            b = cards[idx]
            key_tuple = (b["title"], b["author"])            
            with c:
                with st.container(border=False):
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    st.image(b.get("image_url") or PLACEHOLDER_IMG, use_column_width=True)
                    st.markdown(f"<div class='pill'>{b['category']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='book-title'>{b['title']}</div>")
                    st.markdown(f"<div class='muted'>✍️ {b['author']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='desc'>{b['description']}</div>", unsafe_allow_html=True)
                    rem_key = f"remove_{b['title']}_{b['author']}_{idx}"
                    if st.button("🗑️ 삭제", key=rem_key, use_container_width=True):
                        remove_from_wishlist(key_tuple)
                        st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            idx += 1

# ----------------------
# 바닥글
# ----------------------
st.caption("Tip: 좌측 사이드바에서 CSV를 업로드해 나만의 도서 DB로 바꿔보세요!")
