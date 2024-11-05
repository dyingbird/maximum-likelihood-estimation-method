import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 폰트 설정 추가
plt.rcParams['font.family'] = 'DejaVu Sans'

# 세션 상태 초기화
if 'N_true' not in st.session_state:
    # 실제 전차 수 (50에서 150 사이의 랜덤 값)
    st.session_state['N_true'] = np.random.randint(50, 151)
    
if 'n' not in st.session_state:
    # 표본 크기 (4에서 6 사이의 랜덤 값)
    st.session_state['n'] = np.random.randint(4, 7)
    
if 'observed_numbers' not in st.session_state:
    # 실제 전차 일련번호 리스트
    tank_numbers = np.arange(1, st.session_state['N_true'] + 1)
    # 표본 추출 (중복 없이 랜덤 추출)
    st.session_state['observed_numbers'] = np.random.choice(
        tank_numbers, size=st.session_state['n'], replace=False)
    st.session_state['observed_numbers'].sort()

# 사용자 입력 저장을 위한 상태 변수 초기화
if 'user_guess' not in st.session_state:
    st.session_state['user_guess'] = None

st.title("전차 문제 시뮬레이션")

st.write("""
1부터 시작하여 어떤 숫자까지 차례대로 넘버링된 전차가 있습니다. 실제 전차 생산량은 숨겨져 있습니다.
아래에 제시된 전차의 일련번호 표본을 보고 전체 전차 수를 추측해보세요.
""")

# 관측된 전차 일련번호 표시
st.subheader("관측된 전차의 일련번호")
st.write(f"{st.session_state['observed_numbers']}")

# 사용자로부터 전체 전차 수 추측 입력 받기
st.subheader("전체 전차 수를 추측해보세요:")
user_guess_input = st.text_input("당신이 추측한 전체 전차 수를 입력하세요", value="")

if st.button("추측 제출"):
    try:
        user_guess = int(user_guess_input)
        st.session_state['user_guess'] = user_guess

        # 최대 우도 추정치 계산
        X_max = max(st.session_state['observed_numbers'])
        n = st.session_state['n']
        N_MLE = X_max

        # 불편 추정량 계산
        N_unbiased = X_max + (X_max / n) - 1

        # 실제 전차 수
        N_true = st.session_state['N_true']

        # 결과 출력
        st.subheader("결과")
        st.write(f"당신의 추측: {user_guess}")
        st.write(f"최대 우도 추정치 (MLE): {N_MLE}")
        st.write(f"불편 추정량: {N_unbiased:.2f}")
        st.write(f"실제 전차 수: {N_true}")

        # 추정치 비교 그래프
        st.subheader("추정치 비교 그래프")
        estimates = {
            'your guess': user_guess,
            'maximum likelihood\nestimate': N_MLE,
            'unbiased\nestimator': N_unbiased,
            'Actual number\nof tanks': N_true
        }

        estimate_names = list(estimates.keys())
        estimate_values = list(estimates.values())

        fig, ax = plt.subplots()
        bars = ax.bar(estimate_names, estimate_values, color=['blue', 'orange', 'green', 'red'])
        ax.set_ylabel('number of tanks')
        ax.set_title('Comparison of tank count estimates')
        ax.bar_label(bars)
        st.pyplot(fig)

    except ValueError:
        st.error("올바른 숫자를 입력했는지 확인하세요.")
else:
    if st.session_state['user_guess'] is not None:
        st.write("이미 추측을 제출하셨습니다. 앱을 다시 실행하려면 '다시 시작' 버튼을 눌러주세요.")
    else:
        st.info("전체 전차 수에 대한 당신의 추측을 입력하고 '추측 제출' 버튼을 눌러주세요.")

# 다시 시작 버튼 추가
if st.button("다시 시작"):
    st.session_state.clear()
    st.experimental_rerun()
