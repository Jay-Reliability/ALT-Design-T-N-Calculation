# -*- coding: utf-8 -*-
import re
import streamlit as st
import numpy as np
from scipy.stats import chi2

# ==============================================================================================
# 1. Page Configuration
# ==============================================================================================
st.set_page_config(
    page_title="가속수명시험 시료수-시험시간 계산 프로그램 ⚡",
    page_icon="⚡",
    layout="wide",
)

# ==============================================================================================
# 2. Tone & Manner Styling (01_윈도우_GUI_시료수계산.py 스타일 완벽 재현)
# ==============================================================================================
st.markdown(
    """
    <style>
        /* 전체 배경 및 기본 폰트 */
        .stApp {
            background-color: #EEF2F6;
            color: #1F2933;
            font-family: "Malgun Gothic", "Apple SD Gothic Neo", "Segoe UI", sans-serif;
        }

        /* 상단 타이틀 바 디자인 */
        .window-title-bar {
            background: linear-gradient(180deg, #F8FAFC 0%, #E4EBF1 100%);
            border: 1px solid #B8C2CC;
            border-radius: 8px;
            padding: 12px 18px;
            margin-bottom: 14px;
            font-weight: 700;
            font-size: 13pt;
            color: #243B53;
            box-shadow: 0 2px 6px rgba(16, 42, 67, 0.06);
        }

        /* QGroupBox 스타일 컨테이너 */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #F8FAFC !important;
            border: 1px solid #B8C2CC !important;
            border-radius: 8px !important;
            padding: 14px !important;
        }

        .group-title {
            font-weight: bold;
            color: #243B53;
            font-size: 11pt;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 1px solid #E4E7EB;
        }

        /* 입력 라벨 및 입력창 스타일 */
        div[data-testid="stTextInput"] label p {
            color: #243B53 !important;
            font-weight: bold !important;
            font-size: 10pt !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            border: 1px solid #BCCCDC !important;
            border-radius: 6px !important;
            color: #1F2933 !important;
            font-size: 10pt !important;
            padding: 6px 10px !important;
        }

        /* 실행 버튼 및 텍스트 파일 저장 버튼 (Blue Tone: #2F80ED) */
        div.stButton > button[kind="primary"],
        div.stDownloadButton > button {
            background-color: #2F80ED !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 7px !important;
            padding: 10px 12px !important;
            font-weight: bold !important;
            width: 100% !important;
        }
        div.stButton > button[kind="primary"]:hover,
        div.stDownloadButton > button:hover {
            background-color: #1C64D1 !important;
        }
        div.stButton > button[kind="primary"]:active,
        div.stDownloadButton > button:active {
            background-color: #164E9E !important;
        }

        /* 종료/초기화 버튼 (Red Tone: #D92D20) */
        div.stButton > button[kind="secondary"] {
            background-color: #D92D20 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 7px !important;
            padding: 10px 11px !important;
            font-weight: 700 !important;
            width: 100% !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #B42318 !important;
        }
        div.stButton > button[kind="secondary"]:active {
            background-color: #7A271A !important;
        }

        /* QTextEdit 계산 결과 출력창 스타일 */
        .output-box {
            background-color: #FFFFFF;
            color: #102A43;
            border: 1px solid #BCCCDC;
            border-radius: 6px;
            font-family: Consolas, "Courier New", "Malgun Gothic", monospace;
            font-size: 10.5pt;
            line-height: 1.55;
            padding: 14px 16px;
            min-height: 470px;
            max-height: 600px;
            overflow-y: auto;
            white-space: pre;
        }

        /* 작업지도서 강조 스타일 (Bold & Blue Bold) */
        .section-title {
            font-weight: bold;
            color: #102A43;
        }
        .key-result {
            color: #0052CC;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================================
# 3. Calculation Function (01_윈도우_GUI_시료수계산.py 와 동일한 코드 로직)
# ==============================================================================================
def format_result_block(lb_str, r_str, cl_str, fail_r_str, beta_str, af_str, n_str):
    try:
        LB = float(lb_str)
        R = float(r_str)
        CL = float(cl_str)
        r = int(fail_r_str)
        beta = float(beta_str)
        AF = float(af_str)
        n = float(n_str)
    except ValueError as exc:
        raise ValueError("모든 변수에 유효한 숫자를 입력해주세요.") from exc

    if not (0 < R < 1 and 0 < CL < 1 and r >= 0 and beta > 0 and AF > 0 and n > 0 and LB > 0):
        raise ValueError(
            "신뢰도(R)와 신뢰수준(CL)은 0~1 사이, 허용고장수(r)는 0 이상의 정수, 나머지 변수는 양수여야 합니다."
        )

    dof = 2 * (r + 1)

    # chi2(CL, dof) : 신뢰수준과 허용고장수를 연결하는 통계적 패널티 값
    chi2_val = chi2.ppf(CL, dof)

    # 카이제곱 분포는 CL과 허용고장수 r을 필요 총 정규화 수명(A)이라는 값으로 변환
    A = chi2_val / (2 * (-np.log(R)))

    # n*(h*AF/LB)**beta = A 식에서 test time h를 구함
    test_time_month = (LB / AF) * (A / n) ** (1 / beta)
    test_time_day = test_time_month * 30

    h = test_time_month  # 시험시간
    samples = A / ((h * AF / LB) ** beta)

    # 입력 데이터 포맷팅 ("1. 데이터 입력값" 굵은 글씨)
    input_html = (
        '<span class="section-title">1. 데이터 입력값</span>\n'
        f"   - 수명목표 B10(개월) : {LB:g}\n"
        f"   - 신뢰도(R) : {R:g}\n"
        f"   - 신뢰수준(CL) : {CL:g}\n"
        f"   - 허용고장수(r) : {r:g}\n"
        f"   - 형상모수(β) : {beta:g}\n"
        f"   - 가속계수(AF) : {AF:g}\n"
        f"   - 시료수(n) : {n:g}\n\n"
    )

    # 계산 결과 포맷팅 ("2. 계산 결과 출력" 굵은 글씨 + 핵심 결과값 파랑색 굵은 글씨)
    output_html = (
        '<span class="section-title">2. 계산 결과 출력</span>\n'
        f"   - 자유도 {dof}, 신뢰수준 {CL}일 때 카이제곱 값: {chi2_val:.4f}\n"
        f'   - <span class="key-result">시료수 {n}</span>, A는 {A:.2f}일 때 <span class="key-result">시험시간은 : {test_time_month:.2f}개월</span>\n'
        f'   - <span class="key-result">시료수 {n}</span>, A는 {A:.2f}일 때 <span class="key-result">시험시간은 : {test_time_day:.2f}일</span>\n'
        f'   - <span class="key-result">시험시간 {h:.2f}개월</span>, A는 {A:.2f}일 때 <span class="key-result">시험시료수는 : {samples:.0f}개</span>\n'
        f"{'-' * 60}\n"
    )

    return input_html + output_html


# ==============================================================================================
# 4. Session State Initialization
# ==============================================================================================
if "output_logs" not in st.session_state:
    # 초기 로드 시 기본값(Default 7개 변수)으로 1회 계산 결과 표시
    default_block = format_result_block("120", "0.9", "0.9", "1", "2.5", "50", "50")
    st.session_state.output_logs = [default_block]
    st.session_state.is_initial_auto = True

# ==============================================================================================
# 5. Main Layout (좌측 입력 패널 38% : 우측 출력 패널 62%)
# ==============================================================================================
st.markdown(
    '<div class="window-title-bar">가속수명시험 시료수-시험시간 계산 프로그램 ⚡</div>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([3.8, 6.2], gap="medium")

with left_col:
    with st.container(border=True):
        st.markdown('<div class="group-title">데이터 입력 (7개 변수)</div>', unsafe_allow_html=True)

        inp_LB = st.text_input("수명목표 B10 (개월)", value="120", key="k_LB")
        inp_R = st.text_input("신뢰도 (R)", value="0.9", key="k_R")
        inp_CL = st.text_input("신뢰수준 (CL)", value="0.9", key="k_CL")
        inp_r = st.text_input("허용고장수 (r)", value="1", key="k_r")
        inp_beta = st.text_input("형상모수 (β)", value="2.5", key="k_beta")
        inp_AF = st.text_input("가속계수 (AF)", value="50", key="k_AF")
        inp_n = st.text_input("시료수 (n)", value="50", key="k_n")

    btn_execute = st.button("▶ 실행", type="primary", use_container_width=True)
    btn_exit = st.button("❌ 종료 (결과 초기화)", type="secondary", use_container_width=True)

    if btn_execute:
        try:
            new_block = format_result_block(
                inp_LB, inp_R, inp_CL, inp_r, inp_beta, inp_AF, inp_n
            )
            if st.session_state.get("is_initial_auto", False):
                st.session_state.output_logs = [new_block]
                st.session_state.is_initial_auto = False
            else:
                st.session_state.output_logs.append(new_block)
        except ValueError as err:
            st.error(f"입력 오류: {err}")
        except Exception as err:
            st.error(f"계산 중 오류가 발생했습니다: {err}")

    if btn_exit:
        st.session_state.output_logs = []
        st.session_state.is_initial_auto = False

with right_col:
    with st.container(border=True):
        st.markdown('<div class="group-title">계산 결과 출력</div>', unsafe_allow_html=True)
        combined_output = "\n".join(st.session_state.output_logs)
        st.markdown(
            f'<div class="output-box">{combined_output}</div>',
            unsafe_allow_html=True,
        )

    plain_text_output = re.sub(r"<[^>]+>", "", combined_output).replace("\n", "\r\n")
    st.download_button(
        label="💾 텍스트 파일 저장",
        data=plain_text_output.encode("utf-8-sig"),
        file_name="ALT_시료수_시험시간_계산결과.txt",
        mime="text/plain",
        use_container_width=True,
    )
