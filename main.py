import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="국가별 MBTI Top10", layout="centered")

st.title("🌍 국가별 MBTI 유형 Top 10 시각화")

# 파일 불러오기
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# 파일 업로드 or 기본 파일 경로
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data("countriesMBTI_16types.csv")  # 기본 파일 경로로 설정해주세요

# 국가 선택
countries = df["Country"].tolist()
selected_country = st.selectbox("국가를 선택하세요", countries)

# 해당 국가의 MBTI 비율 상위 10개 추출
def get_top10_mbti(df, country):
    row = df[df["Country"] == country].iloc[0]
    mbti_scores = row.drop("Country").sort_values(ascending=False)[:10]
    return pd.DataFrame({
        "MBTI": mbti_scores.index,
        "비율": mbti_scores.values
    })

top10_df = get_top10_mbti(df, selected_country)

# Altair 그래프
chart = alt.Chart(top10_df).mark_bar().encode(
    x=alt.X("비율:Q", title="비율", scale=alt.Scale(domain=[0, top10_df["비율"].max() * 1.1])),
    y=alt.Y("MBTI:N", sort="-x", title="MBTI 유형"),
    color=alt.Color("MBTI:N", legend=None),
    tooltip=["MBTI", "비율"]
).properties(
    width=600,
    height=400,
    title=f"{selected_country}의 MBTI 유형 Top 10"
)

st.altair_chart(chart, use_container_width=True)
