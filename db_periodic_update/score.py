import numpy as np
import pandas as pd


# 증가하면 안전 점수가 낮아지는 변수를 증가하면 안전 점수가 증가하게 변경한다.
def decrease_variable(x):
    return max(x) - x
# 변수의 최대값이 1이 되도록 normalize 한다.
def normalize(x):
    return (x - min(x)) / (max(x) - min(x))
'''
안전 점수 구하기
[input] 각 국가의 정보다 들어있는 딕셔너리들의 리스트
    [
        {
            'iso_code': (value),
            'total_caeses_per_1million_population' : (value),
            'recovered_ratio': (value),
            'critical_ratio': (value),
            'fully_vaccinated': (value),
            'caution': (value),
            'homicide_rate': (value),
            'safety_index': (value),
            'numbeo_index': (value),
            'last_terrorism': (value),
            'previous_terrorism': (value),
        },
        ...
    ]


[output] pd.DataFrame
Columns
    iso_code
    country_kr
    score
'''
def SafetyScore(data):
    df_score = pd.DataFrame(data)
    '''
    코로나 안전 점수 score1 계산하기

    1. 증가하면 안전 점수가 낮아지는 변수는 decrease_variable() 함수를 이용하여 증가하면 안전 점수가 증가도록 변경한다.
    2. 각 변수의 공분산을 구하여 공분산에 해당하는 고유값과 고유벡터를 구하고, 여기서 얻은 고유값을 각 변수의 가중치로하여 안전점수를 계산한다.
    '''
    X = np.zeros((len(df_score), 5))
    X[:, 0] = df_score['total_caeses_per_1million_population']
    X[:, 0] = decrease_variable(X[:, 0])
    X[:, 0] = normalize(X[:, 0])

    X[:, 1] = df_score['recovered_ratio']
    X[:, 1] = normalize(X[:, 1])

    X[:, 2] = df_score['critical_ratio']
    X[:, 2] = decrease_variable(X[:, 2])
    X[:, 2] = normalize(X[:, 2])

    X[:, 3] = df_score['fully_vaccinated']
    X[:, 3] = normalize(X[:, 3])

    X[:, 4] = df_score['caution']
    X[:, 4] = decrease_variable(X[:, 4])
    X[:, 4] = normalize(X[:, 4])
    # 편차
    X_cen = X - X.mean(axis=0)
    # 분산
    X_cov = np.dot(X_cen.T, X_cen)
    # 고유값, 고유벡터
    w, v = np.linalg.eig(X_cov)
    # 가중치
    rate = w/w.sum()

    df_score['score1'] = (
        rate[0] * X[:, 0] + \
        rate[1] * X[:, 1] + \
        rate[2] * X[:, 2] + \
        rate[3] * X[:, 3] + \
        rate[4] * X[:, 4]
    ) * 100
    '''
    여행 안전 점수 score2 계산하기

    방식은 score1 과 동일하다.
    '''
    X = np.zeros((len(df_score), 5))

    X[:, 0] = df_score['homicide_rate']
    X[:, 0] = decrease_variable(X[:, 0])
    X[:, 0] = normalize(X[:, 0])

    X[:, 1] = df_score['safety_index']
    X[:, 1] = normalize(X[:, 1])

    X[:, 2] = df_score['numbeo_index']
    X[:, 2] = normalize(X[:, 2])

    X[:, 3] = df_score['last_terrorism']
    X[:, 3] = decrease_variable(X[:, 3])
    X[:, 3] = normalize(X[:, 3])

    X[:, 4] = df_score['previous_terrorism']
    X[:, 4] = decrease_variable(X[:, 4])
    X[:, 4] = normalize(X[:, 4])

    X_cen = X - X.mean(axis=0) 
    X_cov = np.dot(X_cen.T, X_cen)
    w2, v2 = np.linalg.eig(X_cov)
    rate = w/w.sum()

    df_score['score2'] = (
        rate[0] * X[:, 0] + \
        rate[1] * X[:, 1] + \
        rate[2] * X[:, 2] + \
        rate[3] * X[:, 3] + \
        rate[4] * X[:, 4]
    ) * 100
    # score1 과 score2를 1:1의 비율로 더하여 score를 구한다.
    df_score['score'] = round(((df_score['score1'] + df_score['score2']) / 2), 2)
    # 여행 안전 경보 4단계인 나라는 입국 금지 이므로 안전 점수를 0으로 만들어준다.
    for i in range(len(df_score)):
        if df_score['caution'][i] == 4:
            df_score['score'][i] = 0

    return df_score
