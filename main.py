import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="MBTI 직업 추천기",
    page_icon="🎯",
    layout="centered"
)

# --- 스타일 ---
st.markdown("""
    <style>
    .job-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .job-title {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
    }
    .job-desc {
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# --- MBTI 직업 추천 데이터 ---
mbti_jobs = {
    "INTJ": [
        ("데이터 과학자 📊", "논리적 분석과 장기 전략 수립에 강점"),
        ("전략 컨설턴트 💼", "큰 그림을 보고 효율적인 솔루션 제공"),
        ("연구원 🔬", "깊이 있는 탐구와 혁신적인 발견")
    ],
    "ENTP": [
        ("창업가 🚀", "새로운 아이디어를 시도하고 문제 해결"),
        ("마케팅 디렉터 📢", "사람들의 관심을 끌어내는 전략 기획"),
        ("기획 PD 🎬", "창의적인 프로젝트와 컨텐츠 제작")
    ],
    "ISFJ": [
        ("간호사 🏥", "세심하고 헌신적인 케어 제공"),
        ("교사 📚", "학생들의 성장과 발전을 돕는 역할"),
        ("사회복지사 🤝", "타인의 삶을 개선하는 일")
    ],
    "ENFP": [
        ("크리에이티브 디자이너 🎨", "새롭고 독창적인 아이디어 실현"),
        ("홍보 담당자 📣", "사람들을 연결하고 브랜드를 알림"),
        ("여행 가이드 🗺️", "즐겁고 활기찬 경험을 제공")
    ]
}

# --- 앱 제목 ---
st.title("🎯 MBTI 기반 직업 추천")
st.markdown("당신의 **MBTI**를 선택하면 어울리는 직업을 추천해 드립니다!")

# --- MBTI 선택 ---
mbti_list = list(mbti_jobs.keys())
user_mbti = st.selectbox("📌 당신의 MBTI를 선택하세요:", mbti_list)

# --- 결과 표시 ---
if user_mbti:
    st.subheader(f"💡 {user_mbti} 유형에게 어울리는 직업")
    jobs = mbti_jobs[user_mbti]
    for job, desc in jobs:
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">{job}</div>
            <div class="job-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 추가 기능 ---
st.markdown("---")
st.caption("✨ 만든 사람: 당신의 멋진 AI 조수")

