#!/usr/bin/env python
# coding: utf-8

# ### 데이터 불러오기

# In[1]:


# KBO 2019시즌 타자 기록지 데이터를 불러오겠습니다. 

import pandas as pd
file  = './data/KBO_2019_player_gamestats.csv'
raw = pd.read_csv(file, encoding = 'cp949')


# In[3]:


# 데이터를 살펴보겠습니다. 
# 타자/게임별 기록이 저장되어 있습니다. 

raw.head()


# In[4]:


raw.info()


# In[5]:


raw.columns


# In[15]:


# 타자 데이터 분석에 활용할 컬럼만 선택하겠습니다. 

columns_select = ['팀', '이름', '생일','일자', '상대','타수','안타','홈런', '루타', '타점','볼넷', '사구', '희비']
data = raw[columns_select]
data.head()


# ## Q) KBO 최고의 타자는??? 

# - 선수별 기록 집계하기

# In[16]:


# 피벗테이블을 이용해, 선수별 주요 기록을 정리하겠습니다. 
data_player = data.pivot_table(index = ['팀','이름','생일'], 
                               values = ['타수','안타','홈런','루타','타점','볼넷','사구','희비'], 
                               aggfunc = 'sum')

data_player


# In[17]:


# 타수가 0인 데이터도 보이는 것 같네요, 타수가 적은 선수는 제외하겠습니다. 
# 어느 정도가 적은지 판단하기 위해, 타수 데이터의 분포를 살펴보겠습니다. 
# sns.histplot() 을 이용할 수도 있고,   판다스에서 기본적으로 내장된 시리즈.hist()를 이용해 살펴볼 수도 있습니다. 

data_player['타수'].hist()


# In[18]:


# 타수가 50보다 큰 선수들만 선택하겠습니다. 
# reset_index() 를 이용해 현재 인덱스로 설정된 팀/이름/생일 데이터를 컬럼으로 변경하겠습니다. 

cond = data_player['타수'] > 50
data_player = data_player[cond].reset_index()    # 다중 인덱스 --> 컬럼으로 변경하기
data_player


# In[19]:


# 타율/출루율/장타율/OPS를 계산하는 함수를 만들어보겠습니다. 
# 데이터 프레임을 입력하면, 해당 데이터 프레임에서 인덱스별 실적을 계산하여 반환해주는 함수입니다. 

def cal_hit(df):
    '''
    - 타율 : 타격에 성공해서 진루하는 비율 --> 안타 / 타수
    - 출루율: 살아서 진루하는 비율 -->  (안타+볼넷+몸에맞는볼)/(타수+볼넷+몸에맞는볼+희생플라이)
    - 장타율 : 타율에 진루한 베이스 가중치 추가 -->   루타 / 타수
    '''
    
    df['타율'] = df['안타'] / df['타수']
    df['출루율'] = (df['안타'] + df['볼넷'] + df['사구']) / (df['타수'] + df['사구'] + df['희비'])
    df['장타율'] = df['루타'] / df['타수']
    df['OPS'] = df['출루율'] + df['장타율']
    return df


# In[20]:


# data_player에 있는 선수별 실적을 이용해 타율, 출루율, 장타율, OPS 를 계산한 데이터프레임을 가져오겠습니다. 

player_stat = cal_hit(data_player)
player_stat


# In[21]:


# 출루율/장타율/OPS/타율 기준으로 KBO 최고 타자는 누구인지 성적순으로 정렬해보겠습니다. 
# 출루율을 기준으로 정렬을 하며, 만약 동률일 경우 그다음 기준인 장타율을, 이후에는 OPS, 타율을 기준으로 정렬하였습니다. 

player_stat = player_stat.sort_values(by = ['출루율','장타율','OPS', '타율'], ascending = False)
player_stat = player_stat.reset_index(drop = True)
player_stat.head(20)


# In[25]:


# 아래 코드는 seaborn, matplotlib으로 시각화를 진행할때 데이터에 한글이 들어있다면 copy&paste 한 뒤 사용하시면 됩니다. 
# 이미지 상에 들어있는 한글을 표시하기 위한 한글 폰트를 지정하고, 필요한 라이브러리를 불러들이는 코드입니다. 

import matplotlib
from matplotlib import font_manager, rc
import platform
import matplotlib.pyplot as plt
import seaborn as sns

# 이미지 한글 표시 설정
if platform.system() == 'Windows':  # 윈도우인 경우 맑은고딕
    font_name = font_manager.FontProperties(fname = "c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family = font_name)
else:    # Mac 인 경우 애플고딕
    rc('font', family = 'AppleGothic')

#그래프에서 마이너스 기호가 표시되도록 하는 설정입니다.
matplotlib.rcParams['axes.unicode_minus'] = False   


# In[26]:


# 팀별 선수 출루율 분포를 boxplot을 이용해 살펴보겠습니다. 
sns.boxplot(data = player_stat, x = '팀', y = '출루율')


# In[27]:


# 팀별 선수 출루율 분포를 swarmplot과 boxplot을 이용해 살펴보겠습니다. 

sns.swarmplot(data = player_stat, x = '팀', y = '출루율')
sns.boxplot(data = player_stat, x = '팀', y = '출루율')       


# In[17]:


# swarmplot과 boxplot을 함께 사용할 경우, 색상이 겹쳐 시각적으로 구분하기가 어렵습니다. 
# 그럴때에는 박스플랏을 색상을 제거하고 간단하게 표시하면 깔끔하게 표현할 수 있습니다. 

sns.swarmplot(data = player_stat, x = '팀', y = '출루율')
sns.boxplot(data = player_stat, x = '팀', y = '출루율',
            showcaps = False,             # 박스 상단 가로라인 보이지 않기
            whiskerprops = {'linewidth':0}, # 박스 상단 세로 라인 보이지 않기 
            showfliers = False,           # 박스 범위 벗어난 아웃라이어 표시하지 않기
            boxprops = {'facecolor':'None'}, # 박스 색상 지우기
           )


# In[28]:


# 타자별 2019년 기록 데이터를 저장하겠습니다. 
# MS-엑셀에서도 파일을 조회할 수 있도록 encoding = 'cp949' 로 저장을 하였으며, 
# index 에 들어있는 0부터 시작하는 번호는 저장하지 않도록 index = False 를 사용하였습니다. 

file = './data/player_stat.csv'
player_stat.to_csv(file, encoding = 'cp949', index = False)

