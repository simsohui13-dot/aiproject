import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="서울시 연령별 인구수 시각화 대시보드",
    layout="wide"
)

# 2. 한글 폰트 설정 (운영체제별 깨짐 방지)
def set_font():
    system_name = platform.system()
    if system_name == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif system_name == 'Darwin':  # Mac
        plt.rc('font', family='AppleGothic')
    else:  # Linux (Streamlit Cloud 환경)
        plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False

set_font()

# 3. 데이터 로드 (pages 폴더 기준 상위 폴더의 poopulation.csv 경로 지정)
@st.cache_data
def load_data():
    # pages 폴더 안에 있으므로 상위 폴더(../)로 이동하여 파일 로드
    file_path = os.path.join(os.path.dirname(__file__), '..', 'poopulation.csv')
    df = pd.read_csv(file_path, encoding='cp949')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.title("📊 서울시 지역별·성별·연도별 연령별 인구 꺾은선 그래프")
st.markdown("사이드바에서 **행정구역, 성별, 연도**를 선택하면 해당 조건의 연령별 인구수 변화를 핫핑크 그래프로 확인할 수 있습니다.")

# 4. 사이드바 필터 설정
st.sidebar.header("🔍 조회 옵션 선택")

# 행정구역 선택
regions = df['행정구역'].unique()
selected_region = st.sidebar.selectbox("행정구역 선택", regions)

# 성별 선택 (총인구수, 남, 여)
gender_options = {
    "총인구": "거주자",
    "남성": "남_거주자",
    "여성": "여_거주자"
}
selected_gender_label = st.sidebar.selectbox("성별 선택", list(gender_options.keys()))
gender_code = gender_options[selected_gender_label]

# 연도 선택 (2020 ~ 2025)
years = [str(y) for y in range(2020, 2026)]
selected_year = st.sidebar.selectbox("연도 선택", years)

# 5. 데이터 필터링 및 전처리
age_columns_prefix = f"{selected_year}_{gender_code}_"
target_cols = [
    col for col in df.columns 
    if col.startswith(age_columns_prefix) and '세' in col and '총인구수' not in col and '연령구간인구수' not in col
]

region_row = df[df['행정구역'] == selected_region]

if not region_row.empty and target_cols:
    ages = [col.split('_')[-1] for col in target_cols]
    
    populations = []
    for col in target_cols:
        val = region_row[col].values[0]
        if isinstance(val, str):
            val = val.replace(',', '')
        populations.append(int(val))
    
    # 6. Matplotlib 꺾은선 그래프 시각화
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 핫핑크 색상 (deeppink) 및 마커 설정
    ax.plot(ages, populations, marker='o', color='deeppink', linewidth=2.5, markersize=6, label=f"{selected_region} ({selected_year}년)")
    
    ax.set_title(f"[{selected_year}년] {selected_region} - {selected_gender_label} 연령별 인구수", fontsize=14, pad=15)
    ax.set_xlabel("나이 (연령대)", fontsize=12)
    ax.set_ylabel("인구수 (명)", fontsize=12)
    
    # 가로축(X축) 10살 단위 구분선 (격자 표시)
    ax.set_xticks(range(len(ages)))
    ax.set_xticklabels(ages, rotation=45)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # 세로축(Y축) 1000만 단위 포맷팅 및 격자선 설정
    import matplotlib.ticker as ticker
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.legend()
    plt.tight_layout()
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 상세 데이터 테이블 표시
    with st.expander("📋 연령별 상세 데이터 보기"):
        chart_df = pd.DataFrame({"연령대": ages, "인구수": populations})
        st.dataframe(chart_df, use_container_width=True)
else:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
