import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import DecisionBoundaryDisplay

# 1. 페이지 기본 설정
st.set_page_config(page_title="붓꽃(Iris) 품종 예측기", page_icon="🌸", layout="centered")
st.title("🌸 붓꽃(Iris) 품종 예측 및 시각화")
st.write("꽃잎의 길이와 너비를 입력하면 **랜덤 포레스트(Random Forest)** 알고리즘이 품종을 예측하고 분류 기준을 시각화해 줍니다.")

# 2. 데이터 로드 및 캐싱
@st.cache_data
def load_data():
    # cp949 및 utf-8 인코딩 자동 대응
    try:
        df = pd.read_csv("iris.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("iris.csv", encoding="utf-8")
    return df

df = load_data()

# 특성과 타겟 분리 (꽃잎길이, 꽃잎너비만 사용)
X = df[['꽃잎길이', '꽃잎너비']]
y = df['품종']

# 품종 이름을 숫자로 매핑 (결정 경계 시각화를 위함)
species_list = sorted(y.unique())
species_to_num = {name: idx for idx, name in enumerate(species_list)}
y_num = y.map(species_to_num)

# 3. 모델 학습 (가장 많이 쓰이는 랜덤 포레스트 분류기)
@st.cache_resource
def train_model(X, y_num):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_num)
    return model

model = train_model(X, y_num)

# 4. 사용자 입력 UI (사이드바 또는 메인 화면)
st.subheader("📏 꽃잎 크기 입력")
col1, col2 = st.columns(2)

with col1:
    petal_length = st.slider(
        "꽃잎길이 (Petal Length, cm)",
        min_value=float(X['꽃잎길이'].min() - 0.5),
        max_value=float(X['꽃잎길이'].max() + 0.5),
        value=3.5,
        step=0.1
    )

with col2:
    petal_width = st.slider(
        "꽃잎너비 (Petal Width, cm)",
        min_value=float(X['꽃잎너비'].min() - 0.5),
        max_value=float(X['꽃잎너비'].max() + 0.5),
        value=1.2,
        step=0.1
    )

# 5. 예측 수행
user_input = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎길이', '꽃잎너비'])
pred_num = model.predict(user_input)[0]
pred_proba = model.predict_proba(user_input)[0]
predicted_species = species_list[pred_num]

# 결과 출력
st.divider()
st.subheader("🔍 예측 결과")
st.success(f"입력하신 붓꽃의 예측 품종은 **{predicted_species}** 입니다! (확률: {pred_proba[pred_num]*100:.1f}%)")

# 품종별 예측 확률 막대 표시
proba_df = pd.DataFrame({
    "품종": species_list,
    "예측 확률(%)": np.round(pred_proba * 100, 1)
})
st.dataframe(proba_df, hide_index=True, use_container_width=True)

# 6. 결정 경계(Decision Boundary) 및 사용자 위치 시각화
st.subheader("📊 분류 근거 시각화 (결정 경계)")
st.caption("배경 색상은 모델이 학습한 각 품종의 영역을 의미합니다. 초록색 별(★)이 어느 색 영역에 속해 있는지 확인해 보세요.")

fig, ax = plt.subplots(figsize=(8, 6))

# 결정 경계 그리기 (모델이 구역을 나눈 기준 시각화)
DecisionBoundaryDisplay.from_estimator(
    model,
    X,
    cmap=plt.cm.Pastel1,
    response_method="predict",
    ax=ax,
    xlabel="Petal Length (cm)",
    ylabel="Petal Width (cm)",
    alpha=0.8
)

# 기존 데이터 산점도 표시
colors = ['#e41a1c', '#377eb8', '#ff7f00'] # 빨강, 파랑, 주황
for idx, species in enumerate(species_list):
    subset = df[df['품종'] == species]
    ax.scatter(
        subset['꽃잎길이'],
        subset['꽃잎너비'],
        c=colors[idx],
        label=species,
        edgecolors='black',
        s=50,
        alpha=0.85
    )

# 사용자가 입력한 값 -> 초록색 별로 강조
ax.scatter(
    petal_length,
    petal_width,
    c='limegreen',
    marker='*',
    s=450,
    edgecolors='black',
    linewidth=1.5,
    label='Your Input (User)',
    zorder=10
)

# 그래프 스타일링 (Streamlit Cloud 리눅스 환경 한글 깨짐 방지를 위해 영문 라벨 사용)
ax.set_title("Iris Classification Decision Boundary & Your Input", fontsize=13, fontweight='bold')
ax.set_xlabel("Petal Length (cm)", fontsize=11)
ax.set_ylabel("Petal Width (cm)", fontsize=11)
ax.legend(loc="upper left", frameon=True)
ax.grid(True, linestyle='--', alpha=0.4)

st.pyplot(fig)
