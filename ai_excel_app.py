#ai_excel_app
import streamlit as st
from openai import OpenAI
import os
import pandas as pd

PASSWORD = "1234"  # 你可以改成自己想要的密码
password_input = st.text_input("Enter password:", type="password")
if password_input != PASSWORD:
    st.warning("Wrong password. Access denied!")
    st.stop()  # 密码错误，停止程序
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Batch Text Rewriter")

uploaded_file = st.file_uploader(
    "Upload a TXT, CSV, or Excel file",
    type=["txt", "csv", "xlsx"]
)

mode = st.selectbox("Select mode", ["formal", "casual", "correct"])

if uploaded_file is not None:

    # 读取文件
    if uploaded_file.name.endswith(".txt"):
        lines = uploaded_file.read().decode("utf-8").splitlines()

    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        lines = df.iloc[:, 0].astype(str).tolist()

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        lines = df.iloc[:, 0].astype(str).tolist()

    results = []
    progress = st.progress(0)

    for i, line in enumerate(lines):

        line = line.strip()
        if not line:
            continue

        if mode == "formal":
            system_prompt = "Rewrite the sentence in a formal and professional way."
        elif mode == "casual":
            system_prompt = "Rewrite the sentence in a casual and natural way."
        else:
            system_prompt = "Correct the grammar of the sentence."

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": line}
            ]
        )

        result = response.choices[0].message.content
        results.append(result)

        progress.progress((i + 1) / len(lines))

    st.text_area("Results", "\n".join(results), height=300)

    if results:
        result_text = "\n".join(results)
        st.download_button(
            label="Download results",
            data=result_text,
            file_name="rewritten_results.txt",
            mime="text/plain"

        )
