import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="국가별 MBTI 16형 분석", page_icon="🌍", layout="wide"
)

st.title("🌍 국가별 MBTI 16형 분포 대시보드")
st.write(
    "국가를 선택하면 해당 국가의 16가지 MBTI 비율을 시각화합니다. (1위: **빨간색**, 나머지: **파란색 그라데이션**)"
)


# 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
  return pd.read_csv("countriesMBTI_16types.csv")


df = load_data()

# 16가지 MBTI 컬럼 리스트
mbti_cols = [
    "INFJ",
    "ISFJ",
    "INTP",
    "ISFP",
    "ENTP",
    "INFP",
    "ENTJ",
    "ISTP",
    "INTJ",
    "ESFP",
    "ESTJ",
    "ENFP",
    "ESTP",
    "ISTJ",
    "ENFJ",
    "ESFJ",
]

# 국가 선택 드롭다운
country_list = sorted(df["Country"].unique())
selected_country = st.selectbox("🌐 분석할 국가를 선택하세요:", country_list)

if selected_country:
  # 데이터 정제 및 정렬 (비율이 높은 순서대로 내림차순 정렬)
  country_row = df[df["Country"] == selected_country]
  plot_data = (
      country_row.melt(
          id_vars=["Country"],
          value_vars=mbti_cols,
          var_name="MBTI",
          value_name="Ratio",
      )
      .sort_values(by="Ratio", ascending=False)
      .reset_index(drop=True)
  )

  # 색상 설정 (1등: 빨간색, 나머지: 파란색 그라데이션)
  # 비율 순서대로 정렬되어 있으므로 첫 번째(인덱스 0)는 빨간색, 나머지는 파란색 팔레트 적용
  colors = ["#ff4b4b"] + sns.color_palette("Blues_r", len(plot_data) - 1)

  # Matplotlib 그래프 생성
  fig, ax = plt.subplots(figsize=(12, 6))
  bars = ax.bar(
      plot_data["MBTI"], plot_data["Ratio"], color=colors, edgecolor="grey"
  )

  # 그래프 디자인 요소 추가
  ax.set_title(
      f"[{selected_country}] MBTI 유형별 비율 분포 (Top 1: 빨간색)",
      fontsize=15,
      fontweight="bold",
      pad=15,
  )
  ax.set_xlabel("MBTI 유형", fontsize=12)
  ax.set_ylabel("비율", fontsize=12)
  plt.xticks(rotation=45, fontsize=10)

  # 막대 위에 정확한 수치(소수점 4자리 등) 표시
  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height:.3f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),  # 3포인트 위로 오프셋
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8,
    )

  sns.despine()
  st.pyplot(fig)

  # 데이터프레임 표 형태로도 제공
  with st.expander("📄 상세 데이터 표 보기"):
    st.dataframe(plot_data, use_container_width=True)

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI별 국가 순위 분석", page_icon="🏆", layout="wide"
)

st.title("🏆 MBTI 유형별 국가 순위 대시보드")
st.write(
    "원하는 MBTI 유형을 선택하면, 해당 성향의 비율이 높은 국가를 **1위부터 순서대로** 막대그래프로 보여줍니다. (1위: **빨간색**, 나머지: **파란색 그라데이션**)"
)


# 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
  return pd.read_csv("countriesMBTI_16types.csv")


df = load_data()

# 16가지 MBTI 컬럼 리스트
mbti_cols = [
    "INFJ",
    "ISFJ",
    "INTP",
    "ISFP",
    "ENTP",
    "INFP",
    "ENTJ",
    "ISTP",
    "INTJ",
    "ESFP",
    "ESTJ",
    "ENFP",
    "ESTP",
    "ISTJ",
    "ENFJ",
    "ESFJ",
]

# 사이드바 또는 상단에서 MBTI 선택 및 표시할 국가 수 조절
col1, col2 = st.columns([2, 1])
with col1:
  selected_mbti = st.selectbox("🧬 분석할 MBTI 유형을 선택하세요:", mbti_cols)
with col2:
  top_n = st.slider(
      "표시할 국가 수 (Top N):", min_value=5, max_value=50, value=15
  )

if selected_mbti:
  # 선택한 MBTI 기준으로 내림차순 정렬 후 상위 N개 추출
  plot_data = (
      df[["Country", selected_mbti]]
      .sort_values(by=selected_mbti, ascending=False)
      .head(top_n)
      .reset_index(drop=True)
  )

  # 색상 설정 (1등: 빨간색, 나머지: 파란색 그라데이션)
  colors = ["#ff4b4b"] + sns.color_palette("Blues_r", len(plot_data) - 1)

  # Matplotlib 그래프 생성 (국가별 비교가 잘 보이도록 가로형 막대그래프나 세로형 중 선택 가능)
  fig, ax = plt.subplots(figsize=(12, 6))
  bars = ax.bar(
      plot_data["Country"],
      plot_data[selected_mbti],
      color=colors,
      edgecolor="grey",
  )

  # 그래프 디자인 요소 추가
  ax.set_title(
      f"'{selected_mbti}' 비율 Top {top_n} 국가 순위 (1위: 빨간색)",
      fontsize=15,
      fontweight="bold",
      pad=15,
  )
  ax.set_xlabel("국가", fontsize=12)
  ax.set_ylabel("비율", fontsize=12)
  plt.xticks(rotation=45, ha="right", fontsize=10)

  # 막대 위에 정확한 수치 표시
  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height:.3f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8,
    )

  sns.despine()
  st.pyplot(fig)

  # 데이터프레임 표 형태로도 제공
  with st.expander("📄 상세 데이터 표 보기"):
    st.dataframe(plot_data, use_container_width=True)
