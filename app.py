import streamlit as st
import pandas as pd
import os
import requests

st.title("동의어 / 반의어 퀴즈 앱")

FILE_PATH = "quiz.csv"
DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=1IkpRvaUO2QUewRSh6Ap6ZiIH_tCmcRuh"

@st.cache_data
def load_data():
    if not os.path.exists(FILE_PATH):
        try:
            r = requests.get(DOWNLOAD_URL)
            with open(FILE_PATH, "wb") as f:
                f.write(r.content)
        except:
            return None
    try:
        return pd.read_csv(FILE_PATH)
    except:
        return None

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

if df is not None:
    st.success("데이터 로드 완료")
    st.dataframe(df.head())

    word = st.text_input("단어 입력")

    if st.button("퀴즈 생성"):
        if not word.strip():
            st.warning("단어를 입력하세요")
        else:
            found = df[
                df['word'].str.contains(word, case=False, na=False) |
                df['synonym'].str.contains(word, case=False, na=False) |
                df['antonym'].str.contains(word, case=False, na=False)
            ]

            if not found.empty:
                for _, row in found.iterrows():
                    st.write(f"**문제 유형:** {row['quiz_type']}")
                    st.write(f"문제: {row['question']}")
                    st.write(f"정답: {row['answer']}")
                    st.caption(f"단어: {row['word']} | 동의어: {row['synonym']} | 반의어: {row['antonym']}")
                    st.divider()
            else:
                st.error("검색 결과 없음")
else:
    st.error("데이터를 불러올 수 없습니다.")
