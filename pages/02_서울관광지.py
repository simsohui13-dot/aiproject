import pandas as pd
import pydeck as pdk
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="외국인 선호 서울 관광지 Top 10",
    page_icon="🗺️",
    layout="wide",
)

# 제목 및 소개
st.title("🇰🇷 외국인이 가장 사랑하는 서울 주요 관광지 TOP 10")
st.markdown(
    "스트림릿(Streamlit)과 Pydeck을 활용해 서울의 대표적인 외국인 핫플 위치와 설명을 한눈에 볼 수 있는 대시보드입니다."
)

# 외국인 선호 서울 관광지 Top 10 데이터 (위도, 경도, 이름, 설명)
tourist_spots = [
    {
        "name": "1. 경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 시대의 가장 크고 웅장한 법궁으로, 한복을 입고 방문하는 외국인 관광객들의 필수 코스입니다.",
    },
    {
        "name": "2. 북촌 한옥마을",
        "lat": 37.5826,
        "lon": 126.9838,
        "desc": "도심 속에서 고즈넉한 한국 전통 기와집과 골목길의 풍경을 감상할 수 있는 대표 명소입니다.",
    },
    {
        "name": "3. N서울타워 (남산타워)",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울의 중심 남산 정상에 위치해 서울 전경을 360도로 조망할 수 있으며, 사랑의 자물쇠로 유명합니다.",
    },
    {
        "name": "4. 명동 쇼핑가",
        "lat": 37.5636,
        "lon": 126.9834,
        "desc": "K-뷰티 화장품 쇼핑과 다양한 길거리 음식을 동시에 즐길 수 있는 세계적인 쇼핑 천국입니다.",
    },
    {
        "name": "5. 동대문디자인플라자(DDP)",
        "lat": 37.5665,
        "lon": 127.0092,
        "desc": "세계적인 건축가 자하 하디드가 설계한 독창적인 유선형 건축물로, 패션과 디자인의 성지입니다.",
    },
    {
        "name": "6. 홍대 거리 (홍대입구)",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "젊음의 에너지, 버스킹 공연, 독특한 카페와 클럽 문화를 즐길 수 있는 홍대권 트렌드 중심지입니다.",
    },
    {
        "name": "7. 롯데월드 & 롯데월드타워",
        "lat": 37.5111,
        "lon": 127.1059,
        "desc": "세계 최고 수준의 높이를 자랑하는 롯데월드타워(서울스카이)와 대형 실내 테마파크가 있는 송파 랜드마크입니다.",
    },
    {
        "name": "8. 국립중앙박물관",
        "lat": 37.5239,
        "lon": 126.9800,
        "desc": "한국의 유구한 역사와 문화를 한눈에 볼 수 있는 세계적인 규모의 박물관으로 서구권 관광객에게도 인기입니다.",
    },
    {
        "name": "9. 반포 한강공원",
        "lat": 37.5118,
        "lon": 126.9921,
        "desc": "한강의 야경과 함께 '치맥' 문화를 즐길 수 있으며, 달빛무지개분수가 외국인들에게 큰 감동을 줍니다.",
    },
    {
        "name": "10. 이태원 & 해방촌",
        "lat": 37.5345,
        "lon": 126.9944,
        "desc": "다양한 국적의 문화를 맛볼 수 있는 세계 음식점과 트렌디한 루프탑 카페가 모여 있는 다문화 거리입니다.",
    },
]

df = pd.DataFrame(tourist_spots)

# Pydeck을 이용한 서울 지도 설정 (중심 좌표: 서울시청 기준)
view_state = pdk.ViewState(
    latitude=37.555, longitude=126.97, zoom=11.5, pitch=30
)

# 지도 위에 표시할 마커 레이어 설정
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_color="[200, 30, 0, 160]",  # 붉은색 계열 마커
    get_radius=300,  # 마커 크기
    pickable=True,
    auto_highlight=True,
)

# 툴팁 설정 (마우스 오버시 이름 표시)
tooltip = {
    "html": "<b>{name}</b>",
    "style": {"background": "grey", "color": "white"},
}

# 지도 렌더링
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/light-v9",
)

st.subheader("📍 서울 관광지 지도 (마우스로 위치를 확인해보세요)")
st.pydeck_chart(r)

# --- 지도 밑 관광지 상세 설명 섹션 ---
st.markdown("---")
st.subheader("📖 관광지 상세 설명 가이드")

# 2열 레이아웃으로 깔끔하게 설명 배치
col1, col2 = st.columns(2)

for i, row in df.iterrows():
    # 짝수 번호는 왼쪽 컬럼, 홀수 번호는 오른쪽 컬럼에 배치
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        with st.container(border=True):
            st.markdown(f"### {row['name']}")
            st.write(row["desc"])
            st.caption(f"위도: {row['lat']} | 경도: {row['lon']}")
