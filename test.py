import streamlit as st

st.set_page_config(page_title="퍼스널 컬러 패션 추천 👗", page_icon="🎨", layout="centered")

st.title("👗 퍼스널 컬러 자가진단 & 패션 추천 🎨")
st.write("간단한 자가진단을 통해 당신의 퍼스널 컬러를 찾아드리고, 어울리는 옷과 색상을 추천해드려요! ✨")

# -------------------------
# 1. 자가진단 질문
# -------------------------
st.header("📝 퍼스널 컬러 자가진단")

skin = st.radio("피부 톤을 골라주세요:", ["밝고 하얀 편", "노란기 도는 편", "붉은기 있는 편", "어두운 편"])
hair = st.radio("머리카락 색은 어떤가요?", ["밝은 갈색/금발", "흑색/진한 갈색", "붉은빛 갈색", "애쉬/차가운 톤"])
eyes = st.radio("눈동자 색은 어떤가요?", ["밝은 갈색/허니", "짙은 갈색/흑색", "푸른빛/회색", "녹색/헤이즐"])

# -------------------------
# 2. 퍼스널 컬러 진단 로직
# -------------------------
def diagnose_color(skin, hair, eyes):
    if skin == "밝고 하얀 편" and eyes in ["밝은 갈색/허니", "녹색/헤이즐"]:
        return "🌸 봄웜 (Spring Warm)"
    elif skin == "노란기 도는 편" and hair in ["밝은 갈색/금발", "붉은빛 갈색"]:
        return "🍂 가을웜 (Autumn Warm)"
    elif skin == "붉은기 있는 편" or eyes == "푸른빛/회색":
        return "🌊 여름쿨 (Summer Cool)"
    else:
        return "❄️ 겨울쿨 (Winter Cool)"

# -------------------------
# 3. 추천 데이터
# -------------------------
recommendations = {
    "🌸 봄웜 (Spring Warm)": {
        "colors": ["#FFB6B9", "#FFD3B6", "#FFEEAD", "#C1E1C1"],
        "tips": "화사하고 따뜻한 파스텔 톤이 잘 어울려요. 코랄, 베이지, 라이트옐로우 추천!",
        "examples": [
            "https://i.pinimg.com/564x/66/b0/41/66b0419077fa9dfb7e86d9f38c3d70f1.jpg",
            "https://i.pinimg.com/564x/37/8d/55/378d5576d7dc76f8f1c49d0bb60a7a1b.jpg",
            "https://i.pinimg.com/564x/3d/91/11/3d91116a7ec2d21c6bfb0c2f3f74efc2.jpg"
        ]
    },
    "🌊 여름쿨 (Summer Cool)": {
        "colors": ["#AEC6CF", "#77AADD", "#CBAACB", "#B5EAD7"],
        "tips": "맑고 시원한 컬러가 어울려요. 라벤더, 소라색, 민트 추천!",
        "examples": [
            "https://i.pinimg.com/564x/62/6e/39/626e3996b080df15c3c9d44b1fdbedb4.jpg",
            "https://i.pinimg.com/564x/08/28/2a/08282a35a5ee26c7dbe6f8873e19a7b7.jpg",
            "https://i.pinimg.com/564x/74/44/b3/7444b3c716a83cf40458f73a2d7b93d8.jpg"
        ]
    },
    "🍂 가을웜 (Autumn Warm)": {
        "colors": ["#D4A373", "#E6B566", "#C97C5D", "#8C5E58"],
        "tips": "깊고 풍부한 컬러가 어울려요. 카멜, 머스타드, 브라운톤 추천!",
        "examples": [
            "https://i.pinimg.com/564x/2f/d4/1a/2fd41a63aa9a7db6f2190f5a873b8b6a.jpg",
            "https://i.pinimg.com/564x/b1/f1/88/b1f188f50c6e4dcb6c4c1df91f82f3a4.jpg",
            "https://i.pinimg.com/564x/36/aa/2c/36aa2c1681fa7f09c1098c2734a1c153.jpg"
        ]
    },
    "❄️ 겨울쿨 (Winter Cool)": {
        "colors": ["#4B0082", "#4682B4", "#D8BFD8", "#000000"],
        "tips": "선명하고 강렬한 컬러가 어울려요. 블랙, 로열블루, 푸시아 추천!",
        "examples": [
            "https://i.pinimg.com/564x/25/d6/8a/25d68a45c5c7a8c7d788ff85ad44e10f.jpg",
            "https://i.pinimg.com/564x/65/c8/e7/65c8e74eb8f41bc06c8f9f228c3b056a.jpg",
            "https://i.pinimg.com/564x/f2/3e/3d/f23e3db44aef5d1f6c5fba94c1c853f2.jpg"
        ]
    }
}

# -------------------------
# 4. 결과 출력
# -------------------------
if st.button("퍼스널 컬러 진단하기 🎯"):
    result = diagnose_color(skin, hair, eyes)
    st.success(f"당신의 퍼스널 컬러는 👉 **{result}** 입니다!")

    data = recommendations[result]

    st.subheader(f"{result} 추천 컬러 팔레트 🎨")
    cols = st.columns(len(data["colors"]))
    for idx, c in enumerate(data["colors"]):
        cols[idx].markdown(
            f"<div style='background-color:{c}; height:80px; border-radius:10px'></div>", 
            unsafe_allow_html=True
        )

    st.write(f"✨ 스타일 TIP: {data['tips']}")

    st.subheader("👗 코디 예시 이미지")
    st.image(data["examples"], use_container_width=True)
