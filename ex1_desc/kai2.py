'''
카이제곱검정 중 일원카이제곱
: 관찰도수가 기대도수와 일치하는 지를 검정하는 방법
: 종류 : 적합도/선호도 검정
- 범주형 변수가 한 가지로, 관찰도수가 기대도수에 일치하는지 검정한다.

적합도 검정
: 자연현상이나 각종 실험을 통해 관찰되는 도수들이 귀무가설 하의 분포(범주형 자료의 각 수준별 비율)에 얼마나 일치하는가에 대한
분석을 적합도 검정이라 한다.
: 관측값들이 어떤 이론적 분포를 따르고 있는지를 검정으로 한 개의 요인을 대상으로 함.
예) 꽃 색깔의 표현 분리 비율이 3:1이 맞는가?
예) 종자의 발아시험 데이터가 이항분포의 적합한가?

<적합도 검정실습>
주사위를 60 회 던져서 나온 관측도수 / 기대도수가 아래와 같이 나온 경우에 이 주사위는 적합한 주사위가 맞는가를 일원카이제곱 검정으로 분석.
주사위 눈금 1 2 3 4 5 6
관측도수 4 6 17 16 8 9
기대도수 10 10 10 10 10 10
가설검정은 수집된 데이터를 근거로 기존에 인식된 생각을 기준으로 새롭게 제기된 주장을 대립가설로 만들어 검증하는 것이다.
'''

# 귀무: 기대치와 관찰치는 차이가 없다. 주사위는 게임에 적합하다.
# 대립: 기대치와 관찰치는 차이가 있다. 주사위는 게임에 적합하지 않다.

# 실험에 의해 수집된 집단이 한 개이므로, 일원카이제곱 검정을 실시하도록 한다.
import pandas as pd
import scipy.stats as stats

obs_data=[4, 6, 17, 16, 8, 9]
result=stats.chisquare(obs_data) #(관찰값, 기대값, 자유도, 진행방향)
print(result) #(statistic=14.200000000000001, pvalue=0.014387678176921308)
print('검정통계량 : %.5f, p-value : %.5f' %result)

# 해석1(카이제곱분포표) : df : (6-1), c.v :11.07, chi2:14.2 이므로 귀무 기각
# 해석2(p-value) : pvalue = 0.01439 <0.05 이므로 귀무 기각 
# => 주사위는 게임에 적합하지 않다.
# 결국, 위 검정은 관찰된 빈도가 기대되는 빈도와 유의한 차이가 있는지를 검증한것. 우연히 발생된 데이터가 아닌 의미있는 데이터, 기존의 생각은 정상이 아니다라고 결론 내릴수 있다.

print('선호도 검정')

# 5가지 종류의 스포츠 음료에 대한 선호도 차이 분석
data1=pd.read_csv('../testdata_utf8/drinkdata.csv')
print(data1)
print()
# 귀무 : 스포츠 음료의 선호도에 차이가 없다.
# 대립 : 스포츠 음료의 선호도에 차이가 있다.
print(sum(data1['관측도수'])) #254
print(stats.chisquare(data1['관측도수'])) #statistic=20.488188976377952, pvalue=0.00039991784008227264
# 해석 : pvalue=0.00039991784008227264 < 유의수준 : 0.05 이므로 귀무기각. 대립채택
# 스포츠 음료의 선호도에 차이가 있다고 할 수 있다. 그러므로, 어떠한 조치(의사결정)를 하는데 있어 참고 자료로 활용




 







