import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="월별 기온 분석 대시보드",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온 분석 대시보드")
st.markdown("특정 월을 선택하여 연도별 최고 기온과 최저 기온 변화를 확인해보세요.")

# 데이터 로드 함수 (캐싱 적용, 한글 깨짐 방지 cp949 인코딩)
@st.cache_data
def load_data():
    file_path = "temperature.csv"
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='utf-8')
    return df

try:
    df = load_data()
    
    # 데이터 전처리: '일시' 컬럼 파싱 (예: 'Oct-07' 형태 처리)
    # 데이터셋의 날짜 형식이 'MMM-YY' 형태이므로 파싱 후 연도와 월 추출
    df['일시_dt'] = pd.to_datetime(df['일시'], format='%b-%y', errors='coerce')
    
    # 파싱에 실패할 경우를 대비해 표준 포맷 시도
    if df['일시_dt'].isnull().all():
        df['일시_dt'] = pd.to_datetime(df['일시'], errors='coerce')
        
    df['연도'] = df['일시_dt'].dt.year
    df['월'] = df['일시_dt'].dt.month

    # 사이드바: 월 선택 기능
    st.sidebar.header("🔍 검색 필터")
    
    # 월 이름 매핑 (1월~12월)
    month_dict = {
        1: "1월", 2: "2월", 3: "3월", 4: "4월", 
        5: "5월", 6: "6월", 7: "7월", 8: "8월", 
        9: "9월", 10: "10월", 11: "11월", 12: "12월"
    }
    
    available_months = sorted(df['월'].dropna().unique())
    selected_month_num = st.sidebar.selectbox(
        "분석할 월을 선택하세요:",
        options=available_months,
        format_func=lambda x: month_dict.get(x, f"{x}월")
    )
    
    # 선택된 월 데이터 필터링
    filtered_df = df[df['월'] == selected_month_num].sort_values('연도')

    # 메인 화면 구성
    st.subheader(f"📅 {month_dict.get(selected_month_num, f'{selected_month_num}월')} 연도별 기온 분석")
    
    if filtered_df.empty:
        st.warning("선택한 월에 해당하는 데이터가 없습니다.")
    else:
        # matplotlib 한글 폰트 깨짐 방지 설정 (시스템 기본 폰트 활용)
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.unicode_minus'] = False

        # 그래프 생성 (요청사항 3, 4, 5번 반영)
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 최고기온 그래프: 핫핑크 (#FF69B4)
        ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], 
                color='#FF69B4', marker='o', linewidth=2, label='최고기온')
        
        # 최저기온 그래프: 하늘색 (#87CEEB)
        ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], 
                color='#87CEEB', marker='s', linewidth=2, label='최저기온')
        
        # 그래프 제목 및 축 이름 설정
        ax.set_title("월별 기온분석", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("연도", fontsize=12)
        ax.set_ylabel("온도 (℃)", fontsize=12)
        
        # 범례 표시
        ax.legend(loc='upper left', frameon=True)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # 스트림릿에 그래프 출력
        st.pyplot(fig)

        # 데이터 테이블 확인용 Expander
        with st.expander("📋 선택된 월의 상세 데이터 보기"):
            display_df = filtered_df[['일시', '연도', '월', '평균기온(℃)', '최고기온(℃)', '최저기온(℃)']]
            st.dataframe(display_df, use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 기온 분석 대시보드",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 다차원 분석 대시보드")
st.markdown("데이터를 바탕으로 월별, 연도별, 그리고 두 연도 간 비교 시각화를 제공합니다.")

# 2. 데이터 로드 함수 (캐싱 및 한글 깨짐 방지)
@st.cache_data
def load_data():
    file_path = "temperature.csv"
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='utf-8')
    return df

try:
    df = load_data()
    
    # 데이터 전처리: '일시' 컬럼을 날짜 형식으로 변환 및 연도/월 분리
    df['일시_dt'] = pd.to_datetime(df['일시'], format='%b-%y', errors='coerce')
    if df['일시_dt'].isnull().all():
        df['일시_dt'] = pd.to_datetime(df['일시'], errors='coerce')
        
    df['연도'] = df['일시_dt'].dt.year
    df['월'] = df['일시_dt'].dt.month

    # Matplotlib 한글 폰트 깨짐 방지 설정
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False

    # 3. 사이드바 메뉴 선택
    st.sidebar.header("📊 분석 메뉴 선택")
    menu = st.sidebar.radio(
        "원하는 분석 항목을 선택하세요:",
        [
            "1. 월별 평균기온 (1~12월)", 
            "2. 특정 연도 최저·최고기온", 
            "3. 2개 연도 비교 분석"
        ]
    )

    # -------------------------------------------------------------------------
    # [기능 1] 가로축이 1월부터 12월이고, 서울의 월별 평균기온 그래프
    # -------------------------------------------------------------------------
    if menu == "1. 월별 평균기온 (1~12월)":
        st.subheader("📈 서울 월별 평균기온 그래프 (1월 ~ 12월)")
        st.markdown("모든 연도의 데이터를 월별(1~12월)로 평균 내어 기온 변화를 살펴봅니다.")
        
        # 월별 평균 계산
        monthly_avg = df.groupby('월')['평균기온(℃)'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_avg['월'], monthly_avg['평균기온(℃)'], color='#FF5733', marker='o', linewidth=2.5, label='월별 평균기온')
        
        ax.set_title("서울 월별 평균기온 분석", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("월 (Month)", fontsize=12)
        ax.set_ylabel("평균기온 (℃)", fontsize=12)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels([f"{i}월" for i in range(1, 13)])
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.5)
        
        st.pyplot(fig)

    # -------------------------------------------------------------------------
    # [기능 2] 연도 1개 선택하면 연도별 최저기온과 최고기온 그래프 (한 그래프)
    # -------------------------------------------------------------------------
    elif menu == "2. 특정 연도 최저·최고기온":
        st.subheader("📉 특정 연도의 월별 최저기온 및 최고기온 비교")
        
        available_years = sorted(df['연도'].dropna().unique())
        selected_year = st.sidebar.selectbox("분석할 연도를 선택하세요:", options=available_years)
        
        year_df = df[df['연도'] == selected_year].sort_values('월')
        
        if year_df.empty:
            st.warning("선택한 연도에 해당하는 데이터가 없습니다.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 최고기온: 핫핑크, 최저기온: 하늘색
            ax.plot(year_df['월'], year_df['최고기온(℃)'], color='#FF69B4', marker='o', linewidth=2, label='최고기온')
            ax.plot(year_df['월'], year_df['최저기온(℃)'], color='#87CEEB', marker='s', linewidth=2, label='최저기온')
            
            ax.set_title(f"{selected_year}년 월별 기온분석 (최고/최저)", fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel("월 (Month)", fontsize=12)
            ax.set_ylabel("온도 (℃)", fontsize=12)
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels([f"{i}월" for i in range(1, 13)])
            ax.legend(loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.5)
            
            st.pyplot(fig)

    # -------------------------------------------------------------------------
    # [기능 3] 연도 2개 선택하면 2개 연도의 비교 그래프
    # -------------------------------------------------------------------------
    elif menu == "3. 2개 연도 비교 분석":
        st.subheader("📊 두 연도 간 월별 평균기온 비교 분석")
        
        available_years = sorted(df['연도'].dropna().unique())
        col1, col2 = st.sidebar.columns(2)
        with col1:
            year1 = st.selectbox("첫 번째 연도", options=available_years, index=0)
        with col2:
            year2 = st.selectbox("두 번째 연도", options=available_years, index=min(1, len(available_years)-1))
            
        df_y1 = df[df['연도'] == year1].sort_values('월')
        df_y2 = df[df['연도'] == year2].sort_values('월')
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.plot(df_y1['월'], df_y1['평균기온(℃)'], color='#3498DB', marker='o', linewidth=2, label=f'{year1}년 평균기온')
        ax.plot(df_y2['월'], df_y2['평균기온(℃)'], color='#E74C3C', marker='s', linewidth=2, label=f'{year2}년 평균기온')
        
        ax.set_title(f"연도별 기온분석 ({year1}년 vs {year2}년)", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("월 (Month)", fontsize=12)
        ax.set_ylabel("평균기온 (℃)", fontsize=12)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels([f"{i}월" for i in range(1, 13)])
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.5)
        
        st.pyplot(fig)

except FileNotFoundError:
    st.error("🚨 `temperature.csv` 파일을 찾을 수 없습니다. GitHub 저장소에 파일을 업로드했는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

except FileNotFoundError:
    st.error("🚨 `temperature.csv` 파일을 찾을 수 없습니다. GitHub 저장소 루트 디렉토리에 파일을 업로드했는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
