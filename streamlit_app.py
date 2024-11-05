import streamlit as st
import numpy as np

st.title("전차 문제 최대 우도 추정")

st.write("""
전차 문제는 제한된 표본으로부터 모집단의 최대값을 추정하는 통계적 문제입니다. 여기서는 관측된 전차의 일련번호를 기반으로 전체 전차 수를 추정합니다.
""")

# 사용자 입력
st.header("관측 데이터 입력")
data_input = st.text_input("관측된 전차의 일련번호를 쉼표로 구분하여 입력하세요 (예: 20,32,17,25)")

if data_input:
    try:
        # 문자열 입력을 숫자 리스트로 변환
        observed_numbers = [int(x.strip()) for x in data_input.split(',')]
        n = len(observed_numbers)
        X_max = max(observed_numbers)

        # 최대 우도 추정치 계산
        N_MLE = X_max

        # 불편 추정량 계산
        N_unbiased = X_max + (X_max / n) - 1

        # 결과 출력
        st.subheader("결과")
        st.write(f"관측된 데이터: {observed_numbers}")
        st.write(f"표본 크기 n: {n}")
        st.write(f"관측된 최대값 X_max: {X_max}")
        st.write(f"최대 우도 추정치 N_MLE: {N_MLE}")
        st.write(f"불편 추정량 N_unbiased: {N_unbiased:.2f}")

        # 추정치 비교 그래프
        st.subheader("추정치 비교")
        estimates = {'MLE 추정치': N_MLE, '불편 추정량': N_unbiased}
        st.bar_chart(list(estimates.values()))

    except ValueError:
        st.error("올바른 숫자를 입력했는지 확인하세요.")
else:
    st.info("관측된 전차의 일련번호를 입력하면 결과가 여기에 표시됩니다.")
