
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 맞춤 추천기",
    page_icon="📚",
    layout="centered"
)

# MBTI 데이터 베이스 (한국 작가 도서 2권 & 로맨스 장르 영화 2편)
MBTI_DATA = {
    "INTJ": {
        "books": [
            {"title": "지구 끝의 아시안", "author": "김초엽", "desc": "정교한 세계관 속 고독과 이성을 다룬 한국 SF 소설"},
            {"title": "새의 선물", "author": "은희경", "desc": "세상을 냉철하게 관찰하는 주인공의 깊이 있는 서사"}
        ],
        "movies": [
            {"title": "이터널 선샤인 (Eternal Sunshine)", "desc": "기억과 사랑의 본질을 지적으로 파헤치는 SF 로맨스"},
            {"title": "그녀 (Her)", "desc": "인공지능과의 사랑을 통해 관계를 독창적으로 탐구하는 로맨스"}
        ]
    },
    "INTP": {
        "books": [
            {"title": "물고기는 존재하지 않는다", "author": "룰루 밀러 (번역서)", "desc": "질서와 혼돈, 진실을 추구하는 탐구적 서사"},
            {"title": "우리가 빛의 속도로 갈 수 없다면", "author": "김초엽", "desc": "과학적 논리와 다정한 감성이 결합된 한국 SF"}
        ],
        "movies": [
            {"title": "미드나잇 인 파리", "desc": "예술과 철학, 시간에 대한 호기심을 자극하는 로맨틱 코미디"},
            {"title": "500일의 서머", "desc": "사랑의 과정을 객관적이고 사실적인 시선으로 분석하는 로맨스"}
        ]
    },
    "INFJ": {
        "books": [
            {"title": "소년이 온다", "author": "한강", "desc": "인간의 내면과 역사적 상처를 깊이 있게 어루만지는 소설"},
            {"title": "모순", "author": "양귀자", "desc": "삶과 인간관계의 복잡한 본질을 통찰하는 한국 문학"}
        ],
        "movies": [
            {"title": "비포 선라이즈 (Before Sunrise)", "desc": "두 사람의 깊은 대화와 영혼의 교감을 담아낸 클래식 로맨스"},
            {"title": "어바웃 타임 (About Time)", "desc": "시간 여행을 통해 삶과 사랑의 진정한 의미를 찾아가는 이야기"}
        ]
    },
    "INFP
