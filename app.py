
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="동의어/반의어 퀴즈", layout="centered")

st.title("📘 동의어 / 반의어 퀴즈 웹앱")

st.write("CSV 파일을 업로드하거나 URL에서 불러와서 퀴즈를 검색할 수 있습니다.")

# ---------------------------
# 데이터 로드 함수
# ---------------------------
def load_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    return pd.read_csv(pd.io.common.StringIO(r.text))

df = None

option = st.radio("데이터 로드 방식 선택", ["파일 업로드", "URL 로드"])

if option == "파일 업로드":
    file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if file:
        df = pd.read_csv(file)

elif option == "URL 로드":
    url = st.text_input("CSV URL 입력", 
        "https://drive.google.com/uc?export=download&id=1IkpRvaUO2QUewRSh6Ap6ZiIH_tCmcRuh")
    if st.button("불러오기"):
        try:
            df = load_from_url(url)
            st.success("데이터 로드 완료")
        except Exception as e:
            st.error(f"로드 실패: {e}")

# ---------------------------
# 데이터 표시
# ---------------------------
if df is not None:
    st.subheader("📊 데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("🔍 퀴즈 검색")

    word = st.text_input("단어 입력")

    if st.button("퀴즈 생성"):
        if word.strip() == "":
            st.warning("단어를 입력해주세요.")
        else:
            result = df[
                df.astype(str).apply(
                    lambda row: row.str.contains(word, case=False, na=False).any(),
                    axis=1
                )
            ]

            if not result.empty:
                st.success(f"'{word}' 검색 결과")
                for _, row in result.iterrows():
                    st.write(f"**[{row.get('quiz_type','')}] {row.get('question','')}**")
                    st.write(f"👉 답: {row.get('answer','')}")
                    st.write("---")
            else:
                st.error("검색 결과가 없습니다.")
else:
    st.info("CSV를 먼저 업로드하거나 URL로 불러와주세요.")
