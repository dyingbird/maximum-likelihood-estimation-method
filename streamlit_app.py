import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 폰트 설정 (한글 사용 안 함)
plt.rcParams['font.family'] = 'DejaVu Sans'

# 세션 상태 초기화
if 'N_true' not in st.session_state or 'restart' in st.session_state:
    st.session_state['N_true'] = np.random.randint(50, 151)
    st.session_state['n'] = np.random.randint(4, 7)
    tank_numbers = np.arange(1, st.session_state['N_true'] + 1)
    st.session_state['observed_numbers'] = np.random.choice(
        tank_numbers, size=st.session_state['n'], replace=False)
    st.session_state['observed_numbers'].sort()
    st.session_state['user_guess'] = None
    if 'restart' in st.session_state:
        del st.session_state['restart']

st.title("전차 문제 시뮬레이션")

st.write("""
1부터 시작하여 어떤 숫자까지 차례대로 넘버링된 전차가 있습니다. 실제 전차 생산량은 숨겨져 있습니다.
아래에 제시된 전차의 일련번호 표본을 보고 전체 전차 수를 추측해보세요.
""")

# 관측된 전차 일련번호 표시 (쉼표로 구분하여 표시)
st.subheader("관측된 전차의 일련번호")
observed_numbers_str = ', '.join(map(str, st.session_state['observed_numbers']))
st.write(f"{observed_numbers_str}")

# 사용자로부터 전체 전차 수 추측 입력 받기
st.subheader("전체 전차 수를 추측해보세요:")
user_guess_input = st.text_input("당신이 추측한 전체 전차 수를 입력하세요", value="")

submit_clicked = st.button("추측 제출")
restart_clicked = st.button("다시 시작")

if submit_clicked and st.session_state['user_guess'] is None:
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
            'Maximum likelihood\nestimate': N_MLE,
            'Unbiased bias\nestimate': N_unbiased,
            'Actual number\nof tanks': N_true
        }

        estimate_names = list(estimates.keys())
        estimate_values = list(estimates.values())

        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(estimate_names, estimate_values, color=['blue', 'orange', 'green', 'red'])
        ax.set_ylabel('number of tanks')
        ax.set_title('Comparison of tank count estimates')
        ax.bar_label(bars)
        plt.tight_layout()

        st.pyplot(fig)

    except ValueError:
        st.error("올바른 숫자를 입력했는지 확인하세요.")

elif restart_clicked:
    st.session_state['restart'] = True
    st.experimental_rerun()

elif st.session_state['user_guess'] is not None:
    st.write("이미 추측을 제출하셨습니다. 새로운 문제를 풀려면 '다시 시작' 버튼을 눌러주세요.")
else:
    st.info("전체 전차 수에 대한 당신의 추측을 입력하고 '추측 제출' 버튼을 눌러주세요.")
