# 가속수명시험 시료수-시험시간 계산 프로그램 ⚡ (ALT Test Condition Design)

신뢰성 가속수명시험(ALT, Accelerated Life Test) 설계 시 **7개 핵심 설계 변수**를 입력하여 필요한 **시험시간(개월/일)** 및 **시험시료수(개)**를 산출하는 웹 애플리케이션입니다.

기존 윈도우 데스크톱 GUI 프로그램(`01_윈도우_GUI_시료수계산.py`)의 통계 계산 로직(`scipy.stats.chi2` 기반 카이제곱 분포 및 와이블 분포 무고장/허용고장 시험 설계식)과 UI/UX Tone & Manner를 웹 브라우저 및 Streamlit 환경에서 동일하게 구현하였습니다.

---

## 주요 기능 및 특징

1. **데이터 입력 (7개 변수)**
   - **수명목표 $B_{10}$ (개월)**: 기본값 `120`
   - **신뢰도 ($R$)**: 기본값 `0.9`
   - **신뢰수준 ($CL$)**: 기본값 `0.9`
   - **허용고장수 ($r$)**: 기본값 `1`
   - **형상모수 ($\beta$)**: 기본값 `2.5`
   - **가속계수 ($AF$)**: 기본값 `50`
   - **시료수 ($n$)**: 기본값 `50`

2. **계산 로직 및 수식**
   - 자유도: $\text{dof} = 2(r + 1)$
   - 카이제곱 통계량: $\chi^2_{CL, \text{dof}} = \text{chi2.ppf}(CL, \text{dof})$
   - 필요 총 정규화 수명($A$):
     $$A = \frac{\chi^2_{CL, \text{dof}}}{2 \cdot (-\ln R)}$$
   - 시험시간($h$, 개월 및 일):
     $$h_{\text{month}} = \frac{L_B}{AF} \cdot \left(\frac{A}{n}\right)^{1/\beta}, \quad h_{\text{day}} = 30 \cdot h_{\text{month}}$$
   - 시험시료수($n$):
     $$n = \frac{A}{(h \cdot AF / L_B)^\beta}$$

3. **시각적 강조 (UI/UX Tone & Manner)**
   - **1. 데이터 입력값** 및 **2. 계산 결과 출력** 섹션 헤더를 **굵은 글씨(Bold)**로 표시
   - 핵심 설계 결과인 **시료수**, **시험시간(개월/일)**, **시험시료수(개)** 항목을 **파란색 굵은 글씨(Blue Bold)**로 강조 표시

---

## 파일 구성

| 파일명 | 설명 |
| :--- | :--- |
| `ALT_Test_Condition_Design.html` | 별도 서버 없이 인터넷 브라우저에서 즉시 실행 가능한 단독(Standalone) HTML 프로그램 |
| `app.py` | Streamlit Community Cloud 배포 및 로컬 웹 서버 실행용 Python 애플리케이션 |
| `requirements.txt` | Streamlit 배포에 필요한 Python 패키지 목록 (`streamlit`, `numpy`, `scipy`) |
| `01_윈도우_GUI_시료수계산.py` | 원본 PyQt5 기반 윈도우 데스크톱 GUI 프로그램 |

---

## 실행 방법

### 1) 단독 HTML 파일 실행 (`ALT_Test_Condition_Design.html`)
별도의 설치 없이 `ALT_Test_Condition_Design.html` 파일을 더블클릭하여 Chrome, Edge 등 인터넷 브라우저에서 바로 실행합니다.

### 2) 로컬 PC에서 Streamlit 앱 실행 (`app.py`)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 3) GitHub 및 Streamlit Community Cloud 게시 방법
1. 본 디렉토리의 `app.py`, `requirements.txt`, `README.md` (필요 시 `ALT_Test_Condition_Design.html` 포함) 파일을 GitHub 저장소(Repository)에 업로드(Push)합니다.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에 로그인한 뒤 **Create app**을 클릭합니다.
3. 업로드한 GitHub Repository, Branch, 그리고 Main file path로 `app.py`를 선택한 후 **Deploy**를 클릭하면 웹에 즉시 게시됩니다.

---

## 기본값(Default) 실행 검증 결과

```text
1. 데이터 입력값
   - 수명목표 B10(개월) : 120
   - 신뢰도(R) : 0.9
   - 신뢰수준(CL) : 0.9
   - 허용고장수(r) : 1
   - 형상모수(β) : 2.5
   - 가속계수(AF) : 50
   - 시료수(n) : 50

2. 계산 결과 출력
   - 자유도 4, 신뢰수준 0.9일 때 카이제곱 값: 7.7794
   - 시료수 50.0, A는 36.92일 때 시험시간은 : 2.13개월
   - 시료수 50.0, A는 36.92일 때 시험시간은 : 63.77일
   - 시험시간 2.13개월, A는 36.92일 때 시험시료수는 : 50개
------------------------------------------------------------
```
