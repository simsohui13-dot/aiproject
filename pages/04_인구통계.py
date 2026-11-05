import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import platform
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="서울시 연령대별 인구 상위 행정구 분석",
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

# 3. 데이터 로드 (상위 폴더의 poopulation.csv 경로 지정)
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'poopulation.csv')
    df = pd.read_csv(file_path, encoding='cp949')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.title("🏙️ 연령대별 인구 상위 행정구 막대 그래프 분석")
st.markdown("연도, 성별, 그리고 **10살 단위 연령대**를 선택하면 해당 연령 인구가 많은 순서대로 행정구 막대 그래프를 그려줍니다.")

# 4. 사이드바 설정
st.sidebar.header("🔍 조회 옵션 선택")

# 연도 선택 (2020 ~ 2025)
years = [str(y) for y in range(2020, 2026)]
selected_year = st.sidebar.selectbox("연도 선택", years, index=len(years)-1)

# 성별 선택
gender_options = {
    "총인구": "거주자",
    "남성": "남_거주자",
    "여성": "여_거주자"
}
selected_gender_label = st.sidebar.selectbox("성별 선택", list(gender_options.keys()))
gender_code = gender_options[selected_gender_label]

# 연령대 옵션 동적 추출 (CSV 파일 형식에 맞춰 '년' 문자 추가)
sample_prefix = f"{selected_year}년_{gender_code}_"
sample_cols = [
    col for col in df.columns 
    if col.startswith(sample_prefix) and '세' in col and '총인구수' not in col and '연령구간인구수' not in col
]

# 연령대 컬럼 검사
if not sample_cols:
    st.error(f"[{selected_year}년 {selected_gender_label}]에 해당하는 연령별 데이터를 찾을 수 없습니다.")
    st.stop()

age_options = [col.split('_')[-1] for col in sample_cols]
selected_age = st.sidebar.selectbox("연령대 선택 (10살 단위)", age_options)

# 5. 데이터 가공 및 필터링
sub_df = df[df['행정구역'].str.contains('구') & ~df['행정구역'].str.contains('서울특별시$')].copy()

if sub_df.empty:
    sub_df = df.copy()

target_col = f"{selected_year}년_{gender_code}_{selected_age}"

if target_col not in sub_df.columns:
    st.error(f"지정한 데이터 컬럼({target_col})이 존재하지 않습니다.")
    st.stop()

# 인구수 데이터를 숫자로 변환 (콤마 제거)
def clean_population(val):
    if pd.isna(val):
        return 0
    if isinstance(val, str):
        val = val.replace(',', '').strip()
        return int(val) if val.isdigit() else 0
    return int(val)

sub_df['인구수'] = sub_df[target_col].apply(clean_population)

# 행정구역 이름 정렬
def parse_region_name(x):
    parts = x.split()
    if len(parts) >= 2:
        return parts[1]
    return x

sub_df['구 이름'] = sub_df['행정구역'].apply(parse_region_name)

# 인구수 기준으로 내림차순 정렬
sub_df = sub_df.sort_values(by='인구수', ascending=False).reset_index(drop=True)

# 6. 상위 몇 개 구를 보여줄지 선택
top_n = st.sidebar.slider("출력할 행정구 개수 선택", min_value=5, max_value=len(sub_df), value=min(10, len(sub_df)))
plot_df = sub_df.head(top_n)

# 7. 핫핑크 색상 막대그래프 시각화
st.subheader(f"📊 [{selected_year}년] {selected_gender_label} - '{selected_age}' 인구 상위 {top_n}개 행정구")

if plot_df.empty or plot_df['인구수'].sum() == 0:
    st.warning("선택한 조건에 해당하는 인구 데이터가 존재하지 않습니다.")
else:
    fig, ax = plt.subplots(figsize=(12, 6))

    # 핫핑크 컬러 적용 ('deeppink')
    bars = ax.bar(plot_df['구 이름'], plot_df['인구수'], color='deeppink', alpha=0.85, edgecolor='black', linewidth=0.6)

    ax.set_title(f"{selected_year}년 {selected_age} 인구 상위 행정구 현황", fontsize=15, pad=15, fontweight='bold')
    ax.set_xlabel("행정구", fontsize=12)
    ax.set_ylabel("인구수 (명)", fontsize=12)

    # X축 레이블 45도 회전
    plt.xticks(rotation=45, ha='right', fontsize=11)

    # 세로축(Y축) 콤마 포맷팅 및 격자선 추가
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 막대 위에 정확한 인구수 숫자 표출
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

# 8. 하단 데이터 테이블 제공
with st.expander("📋 전체 자치구 순위 데이터 표로 보기"):
    st.dataframe(sub_df[['구 이름', '인구수']], use_container_width=True)
