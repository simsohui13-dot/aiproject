import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# 한글 폰트 설정 (기본 sans-serif 사용 및 마이너스 부호 깨짐 방지)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="월별 기온 변화 및 미래 예측", layout="wide")

st.title("🌡️ 1907-2025 월별 평균기온 추이 및 미래 예측")
st.markdown("""
이 애플리케이션은 **1907년부터 2025년까지의 기온 데이터**를 바탕으로 선택한 월의 기온 변화를 시각화하고, 
**3가지 대표 Machine Learning 알고리즘**을 활용해 미래 평균기온을 예측 및 비교합니다.
""")

# 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('temperature.csv', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv('temperature.csv', encoding='cp949')
    
    # 1907년 10월부터 시작하는 날짜 데이터 생성 및 연도/월 추출
    df['Date'] = pd.date_range(start='1907-10-01', periods=len(df), freq='MS')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # 1907년부터 2025년까지 데이터 필터링
    df = df[(df['Year'] >= 1907) & (df['Year'] <= 2025)]
    return df

try:
    data = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 사이드바 사용자 입력
st.sidebar.header("⚙️ 옵션 설정")
selected_month = st.sidebar.selectbox("분석 및 예측할 월(Month)을 선택하세요:", list(range(1, 13)), index=7)
predict_target_year = st.sidebar.slider("예측할 미래 연도를 선택하세요:", min_value=2026, max_value=2100, value=2050, step=1)

# 선택한 월 데이터 필터링 및 결측치 제거
month_df = data[data['Month'] == selected_month].dropna(subset=['평균기온(℃)']).copy()

# 데이터 분할 (X: 연도, y: 평균기온)
X = month_df[['Year']].values
y = month_df['평균기온(℃)'].values

# 머신러닝 모델 학습
linear_model = LinearRegression()
linear_model.fit(X, y)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

svr_model = SVR(kernel='rbf', C=100, gamma=0.001)
svr_model.fit(X, y)

# 예측 범위 연도 설정 (1907년 ~ 목표 예측 연도)
future_years = np.arange(1907, predict_target_year + 1).reshape(-1, 1)

# 예측 수행
pred_linear = linear_model.predict(future_years)
pred_rf = rf_model.predict(future_years)
pred_svr = svr_model.predict(future_years)

# ---------------------------------------------------------
# 그래프 시각화
# ---------------------------------------------------------
st.subheader(f"📊 {selected_month}월 평균기온 추이 및 머신러닝 예측 비교 (1907년 ~ {predict_target_year}년)")

fig, ax = plt.subplots(figsize=(13, 6))

# 1. 실제 데이터 플롯
ax.scatter(X, y, color='black', alpha=0.5, label='Actual Data (1907-2025)', zorder=3)

# 2. 알고리즘별 예측 선 플롯
ax.plot(future_years, pred_linear, label='Linear Regression (선형 추세)', color='red', linewidth=2.5)
ax.plot(future_years, pred_rf, label='Random Forest (구간 평균/계단형)', color='green', linewidth=2, linestyle='--')
ax.plot(future_years, pred_svr, label='SVR (곡선/비선형 감쇄)', color='blue', linewidth=2, linestyle=':')

# 3. 예측 목표 연도 수직선 표시
ax.axvline(x=predict_target_year, color='gray', linestyle='--', alpha=0.7)
ax.axvline(x=2025, color='orange', linestyle=':', label='End of History (2025)')

# 4. 목표 연도 예측값 포인트 강조
target_idx = predict_target_year - 1907
ax.scatter([predict_target_year]*3, [pred_linear[target_idx], pred_rf[target_idx], pred_svr[target_idx]], 
           color=['red', 'green', 'blue'], s=80, zorder=5)

ax.set_title(f"{selected_month} Month Average Temperature Forecast ({predict_target_year})", fontsize=14, pad=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Average Temperature (°C)", fontsize=12)
ax.legend(loc='upper left', frameon=True)
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# ---------------------------------------------------------
# 예측 결과 요약 표
# ---------------------------------------------------------
st.markdown(f"### 🎯 {predict_target_year}년 {selected_month}월 알고리즘별 예측 결과")
col1, col2, col3 = st.columns(3)
col1.metric("선형 회귀 (Linear Regression)", f"{pred_linear[target_idx]:.2f} °C")
col2.metric("랜덤 포레스트 (Random Forest)", f"{pred_rf[target_idx]:.2f} °C")
col3.metric("서포트 벡터 회귀 (SVR)", f"{pred_svr[target_idx]:.2f} °C")

st.divider()

# ---------------------------------------------------------
# 알고리즘 작동 방식 설명
# ---------------------------------------------------------
st.markdown("### 🧠 그래프를 통해 보는 알고리즘 작동 원리 및 특징")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 🔴 1. 선형 회귀 (Linear Regression)")
    st.markdown("""
    * **그래프 상 형태:** 일정한 기울기를 가진 **직선** 형태
    * **작동 원리:** 데이터 전체의 지구 온난화 및 기온 상승 경향(온난화 추세)을 하나의 직선 방정식($y = ax + b$)으로 학습합니다.
    * **미래 예측 특징:** 학습 범위(2025년)를 벗어난 먼 미래에도 데이터 전체의 **지속적인 장기 상승/하락 추세를 수평선 너머까지 외삽(Extrapolation)** 하여 반영합니다.
    """)

with col_b:
    st.markdown("#### 🟢 2. 랜덤 포레스트 (Random Forest)")
    st.markdown("""
    * **그래프 상 형태:** 최근 구간에서 평평하게 유지되는 **계단형(Step-like)** 형태
    * **작동 원리:** 여러 개의 의사결정 나무(Decision Tree)가 데이터를 특정 연도 구간으로 쪼개어 평균값을 구합니다.
    * **미래 예측 특징:** 트리 기반 모델은 **학습 데이터 범위 밖(2026년 이후)을 스스로 추론(Extrapolation)하지 못하므로**, 가장 최근(2025년 부근)에 학습된 구간의 평균값을 미래에도 그대로 유지하는 수평선을 그립니다.
    """)

with col_c:
    st.markdown("#### 🔵 3. 서포트 벡터 회귀 (SVR - RBF Kernel)")
    st.markdown("""
    * **그래프 상 형태:** 국소적인 변화를 반영하는 **부드러운 곡선** 형태
    * **작동 원리:** 데이터 주변에 수용 범위(Margin)를 두고 비선형 패턴을 곡선 형태로 피팅합니다.
    * **미래 예측 특징:** RBF 커널 특성상 관측 데이터 범위(1907~2025)에서 멀어질수록 데이터 영향력이 줄어들어 **전체 데이터의 평균값 위치로 점차 수렴(Flattening)**하는 곡선을 보여줍니다.
    """)
