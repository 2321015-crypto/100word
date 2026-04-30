
import streamlit as st
import pandas as pd

st.set_page_config(page_title="동의어/반의어 퀴즈", layout="centered")

st.title("📚 동의어 / 반의어 퀴즈 생성기")

st.write("CSV 파일을 업로드하고 단어를 입력하면 퀴즈를 보여줍니다.")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("파일 로드 완료!")
    st.dataframe(df.head())

    word_input = st.text_input("단어 입력", placeholder="예: 빠르다")

    if st.button("퀴즈 생성"):

        if word_input.strip() == "":
            st.warning("단어를 입력해주세요.")
        else:
            found_rows = df[
                (df['word'].str.contains(word_input, na=False, case=False)) |
                (df['synonym'].str.contains(word_input, na=False, case=False)) |
                (df['antonym'].str.contains(word_input, na=False, case=False))
            ]

            if not found_rows.empty:
                st.subheader(f"🔎 '{word_input}' 관련 퀴즈")

                for _, row in found_rows.iterrows():
                    st.markdown("---")
                    st.write(f"📌 문제 유형: {row['quiz_type']}")
                    st.write(f"❓ 문제: {row['question']}")
                    st.write(f"✅ 정답: {row['answer']}")
            else:
                st.error("해당 단어의 퀴즈를 찾을 수 없습니다.")
else:
    st.info("CSV 파일을 업로드해주세요.")
