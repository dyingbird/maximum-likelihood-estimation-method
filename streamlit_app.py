import streamlit as st
import numpy as np
import koreanize_matplotlib.pyplot as plt
import requests
import json

# 폰트 설정 (한글 사용 안 함)
plt.rcParams['font.family'] = 'DejaVu Sans'

# Apps Script 웹 앱 URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw0lpPAvap4Wu8IROeYxKxJXJmscDz9zuvPYz-P9EaPILctrGh6zkjwl4Ak2kCTaWO-/exec"  # 여기에 웹 앱 URL을 입력하세요.

# 세션 상태 초기화
if 'N_true' not in st.session_state:
    st.session_state['N_true'] = np.random.randint(50, 151)
    st.session_state['n'] = np.random.randint(4, 7)
    tank_numbers = np.arange(1, st.session_state['N_true'] + 1)
    st.session_state['observed_numbers'] = np.random.choice(
        tank_numbers, size=st.session_state['n'], replace=False)
    st.session_state['observed_numbers'].sort()
    st.session_state['user_guess'] = None

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
user_guess_input = st.text_input("당신이 추측한 전체 전차 수를 입력하세요", value="", key='user_guess_input')

submit_clicked = st.button("추측 제출")

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

        # 계산 과정 보여주기
        st.subheader("계산 과정")
        st.write(f"표본 크기 (n): {n}")
        st.write(f"관측된 최대 일련번호 (X_max): {X_max}")

        st.write("**최대 우도 추정치 (MLE) 계산**")
        st.latex(r'''
            \hat{N}_{\text{MLE}} = X_{\text{max}} = %d
            ''' % N_MLE)

        st.write("**불편 추정량 계산**")
        st.latex(r'''
            \hat{N}_{\text{unbiased}} = X_{\text{max}} + \left( \dfrac{X_{\text{max}}}{n} \right) - 1 = %d + \left( \dfrac{%d}{%d} \right) - 1 = %.2f
            ''' % (X_max, X_max, n, N_unbiased))

        # 각 추정치와 실제 값의 차이 계산
        diff_user = abs(N_true - user_guess)
        diff_MLE = abs(N_true - N_MLE)
        diff_unbiased = abs(N_true - N_unbiased)

        # 차이 값을 딕셔너리에 저장
        differences = {
            '당신의 추측': diff_user,
            '최대 우도 추정치 (MLE)': diff_MLE,
            '불편 추정량': diff_unbiased
        }

        # 가장 작은 차이를 찾기
        min_diff_value = min(differences.values())
        closest_estimate = [name for name, diff in differences.items() if diff == min_diff_value]

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

        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(estimate_names, estimate_values, color=['blue', 'orange', 'green', 'red'])
        ax.set_ylabel('number of tanks')
        ax.set_title('Comparison of tank count estimates')
        ax.bar_label(bars)
        plt.tight_layout()

        st.pyplot(fig)

        # 결과 요약
        st.subheader("결과 요약")
        st.write(f"당신의 추측: {user_guess}")
        st.write(f"최대 우도 추정치 (MLE): {N_MLE}")
        st.write(f"불편 추정량: {N_unbiased:.2f}")
        st.write(f"실제 전차 수: {N_true}")

        # 실제 전차 수와의 차이 계산
        st.subheader("추정치와 실제 전차 수의 차이 비교")
        
        # 계산 과정과 결과 표시
        st.write(f"당신의 추측과의 차이: |{N_true} - {user_guess}| = {diff_user}")
        st.write(f"최대 우도 추정치와의 차이: |{N_true} - {N_MLE}| = {diff_MLE}")
        st.write(f"불편 추정량과의 차이: |{N_true} - {N_unbiased:.2f}| = {diff_unbiased:.2f}")

        st.write("")

        # 가장 작은 차이를 보이는 추정치 표시
        st.write(f"가장 작은 차이를 보이는 값은 **{' , '.join(closest_estimate)}** 입니다.")

        # 데이터를 Apps Script 웹 앱에 전송
        data = {
            "observed_numbers": observed_numbers_str,
            "sample_size": int(n),
            "max_observed": int(X_max),
            "user_guess": int(user_guess),
            "mle_estimate": int(N_MLE),
            "unbiased_estimate": float(N_unbiased),
            "true_value": int(N_true),
            "diff_user": int(diff_user),
            "diff_mle": int(diff_MLE),
            "diff_unbiased": float(diff_unbiased)
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEB_APP_URL, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            st.success("결과가 성공적으로 저장되었습니다.")
        else:
            st.error(f"데이터를 저장하는 중 오류가 발생했습니다. 상태 코드: {response.status_code}")

    except ValueError:
        st.error("올바른 숫자를 입력했는지 확인하세요.")

elif st.session_state['user_guess'] is not None:
    st.write("이미 추측을 제출하셨습니다. 새로고침하여 새로운 문제를 풀어보세요.")
else:
    st.info("전체 전차 수에 대한 당신의 추측을 입력하고 '추측 제출' 버튼을 눌러주세요.")
