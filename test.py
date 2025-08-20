import streamlit as st

# ===============================
# 앱 기본 설정
# ===============================
st.set_page_config(page_title="🐶 강아지 행동 설명 앱", page_icon="🐾", layout="wide")
st.title("🐶 강아지 행동 설명 앱")
st.write("강아지 정보를 입력하고, 행동을 기록하면 맞춤 분석과 피드백을 제공합니다 📝")

# ===============================
# 세션 상태 초기화
# ===============================
if "dog_profile" not in st.session_state:
    st.session_state.dog_profile = {}
if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# 강아지 프로필 입력
# ===============================
st.header("🐾 강아지 프로필 입력")

dog_name = st.text_input("강아지 이름을 입력하세요", value=st.session_state.dog_profile.get("이름", ""))
dog_age = st.number_input("강아지 나이 (살)", min_value=0, max_value=30, step=1,
                          value=st.session_state.dog_profile.get("나이", 0))
dog_breed = st.text_input("견종을 입력하세요", value=st.session_state.dog_profile.get("견종", ""))
dog_weight = st.number_input("몸무게 (kg)", min_value=0.0, step=0.1,
                             value=st.session_state.dog_profile.get("몸무게", 0.0))
dog_personality = st.selectbox("성격을 선택하세요", ["활발함", "얌전함", "겁많음", "사교적", "호기심 많음"],
                               index=0)

if st.button("✅ 프로필 저장하기"):
    st.session_state.dog_profile = {
        "이름": dog_name,
        "나이": dog_age,
        "견종": dog_breed,
        "몸무게": dog_weight,
        "성격": dog_personality
    }
    st.success(f"🐶 {dog_name}의 프로필이 저장되었습니다!")

# ===============================
# 행동 데이터
# ===============================
dog_behaviors = {
    "꼬리": {
        "🐕‍🦺 꼬리를 크게 흔듦": {"의미": "😍 기쁨과 반가움의 신호예요.", "대처법": "같이 놀아주고 교감을 해주세요 🐾", "긍정": True},
        "🐕 꼬리를 천천히 흔듦": {"의미": "🤔 경계하거나 주의를 기울이는 상태예요.", "대처법": "안심할 수 있게 도와주세요.", "긍정": False},
        "😟 꼬리를 다리 사이에 넣음": {"의미": "😨 불안, 두려움, 복종을 의미해요.", "대처법": "달래주고 환경을 안정시켜 주세요.", "긍정": False},
        "😠 꼬리를 뻣뻣하게 세움": {"의미": "⚠️ 긴장, 위협 신호예요.", "대처법": "자극적인 상황을 피하세요.", "긍정": False},
    },
    # ... (생략: 기존 귀/몸짓/소리/표정/습관/식사/사회성 데이터 동일)
}

# ===============================
# 프로필이 입력되었을 때만 행동 분석 기능 활성화
# ===============================
if st.session_state.dog_profile:
    st.markdown("---")
    st.header(f"📂 {st.session_state.dog_profile['이름']}의 행동 기록")

    category = st.radio("카테고리를 선택하세요:", list(dog_behaviors.keys()))
    behavior = st.selectbox("🐾 행동을 선택하세요:", list(dog_behaviors[category].keys()))

    if behavior:
        info = dog_behaviors[category][behavior]
        st.subheader(f"{behavior}")
        st.write(f"**의미:** {info['의미']}")
        st.write(f"**대처법:** {info['대처법']}")

        if st.button("📌 이 행동 기록하기"):
            st.session_state.history.append({"행동": behavior, **info})
            st.success(f"{st.session_state.dog_profile['이름']}의 행동이 기록되었습니다!")

    # ===============================
    # 기록 분석
    # ===============================
    if st.session_state.history:
        st.markdown("---")
        st.subheader(f"📊 {st.session_state.dog_profile['이름']}의 오늘 행동 리포트")

        positive = sum(1 for h in st.session_state.history if h["긍정"])
        negative = len(st.session_state.history) - positive

        for idx, h in enumerate(st.session_state.history, 1):
            st.write(f"{idx}. {h['행동']} → {h['의미']}")

        st.write(f"✅ 긍정 행동 수: {positive}")
        st.write(f"⚠️ 부정/스트레스 행동 수: {negative}")

        # 스트레스 지수 결과
        if negative > positive:
            st.error("😟 스트레스 지수가 높아요. 강아지를 안정시켜 주세요!")
        else:
            st.success("🥰 행복 지수가 높아요. 잘 돌보고 계시네요!")

        # 맞춤 피드백
        st.markdown("### 📝 맞춤 피드백")

        feedback = []
        if negative >= 3:
            feedback.append("⚠️ 스트레스 신호가 자주 보입니다. 산책이나 놀이 시간을 늘려주세요.")
        if any("낑낑거림" in h["행동"] for h in st.session_state.history):
            feedback.append("🩺 낑낑거림이 잦으면 불안 또는 통증일 수 있으니 관찰이 필요합니다.")
        if any("토함" in h["행동"] for h in st.session_state.history):
            feedback.append("🚑 토하는 행동이 반복되면 반드시 수의사 상담을 권장합니다.")
        if positive >= 3 and negative == 0:
            feedback.append("🎉 아주 행복한 하루를 보냈어요! 지금처럼만 돌봐주세요.")
        if not feedback:
            feedback.append("🙂 특별한 문제는 없지만 꾸준한 교감과 돌봄이 필요합니다.")

        for fb in feedback:
            st.write(fb)
