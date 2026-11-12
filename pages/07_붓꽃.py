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

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import DecisionBoundaryDisplay

# 1. 페이지 기본 설정
st.set_page_config(page_title="멀티 알고리즘 붓꽃 예측기", page_icon="🌸", layout="centered")
st.title("🌸 붓꽃(Iris) 품종 예측 및 알고리즘 비교 시각화")
st.write("사용자가 원하는 분류 알고리즘을 선택하고, 꽃잎 크기를 입력해 품종이 어떻게 분류되는지 확인해 보세요.")

# 2. 데이터 로드 및 캐싱
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("iris.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("iris.csv", encoding="utf-8")
    return df

df = load_data()

# 특성과 타겟 분리 (꽃잎길이, 꽃잎너비 사용)
X = df[['꽃잎길이', '꽃잎너비']]
y = df['품종']

species_list = sorted(y.unique())
species_to_num = {name: idx for idx, name in enumerate(species_list)}
y_num = y.map(species_to_num)

# 3. 사이드바 - 알고리즘 선택 및 설명
st.sidebar.header("⚙️ 설정 패널")
algo_option = st.sidebar.selectbox(
    "분류 알고리즘 선택",
    ("랜덤 포레스트 (Random Forest)", "서포트 벡터 머신 (SVM)", "K-최근접 이웃 (KNN)")
)

st.sidebar.divider()
st.sidebar.subheader("📖 알고리즘 설명")

if algo_option == "랜덤 포레스트 (Random Forest)":
    st.sidebar.write(
        "**Random Forest**\n\n"
        "여러 개의 결정 트리(Decision Tree)를 앙상블(묶음)하여 "
        "다수의 투표를 통해 최종 품종을 예측하는 알고리즘입니다. "
        "과적합이 적고 정확도가 높아 가장 널리 사용됩니다."
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)

elif algo_option == "서포트 벡터 머신 (SVM)":
    st.sidebar.write(
        "**Support Vector Machine (SVM)**\n\n"
        "데이터들 사이의 경계선(초평면)을 찾아내어, "
        "각 품종 간의 여백(Margin)이 최대가 되도록 분류하는 강력한 알고리즘입니다. "
        "비선형 경계도 유연하게 잘 찾아냅니다."
    )
    model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)

else:  # KNN
    st.sidebar.write(
        "**K-Nearest Neighbors (KNN)**\n\n"
        "새로운 데이터와 가장 가까운 K개의 주변 데이터를 살펴본 후, "
        "가장 많이 등장하는 품종으로 분류하는 직관적인 알고리즘입니다. "
        "데이터의 지역적 특성을 잘 반영합니다."
    )
    model = KNeighborsClassifier(n_neighbors=5)

# 4. 사용자 입력 값 범위 확장 설정 UI
st.subheader("📏 사용자 입력 범위 및 크기 설정")
st.write("슬라이더의 최소/최대 범위를 조정하여 데이터 범위 바깥의 가상 수치도 테스트해 볼 수 있습니다.")

col_r1, col_r2 = st.columns(2)
with col_r1:
    min_len = st.number_input("꽃잎길이 최소값", value=float(X['꽃잎길이'].min() - 1.0), step=0.5)
    max_len = st.number_input("꽃잎길이 최대값", value=float(X['꽃잎길이'].max() + 1.0), step=0.5)
with col_r2:
    min_wid = st.number_input("꽃잎너비 최소값", value=float(X['꽃잎너비'].min() - 0.5), step=0.5)
    max_wid = st.number_input("꽃잎너비 최대값", value=float(X['꽃잎너비'].max() + 0.5), step=0.5)
