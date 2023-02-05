#!/usr/bin/env python
# coding: utf-8

# ### 데이터 불러오기

# In[8]:


# 2019년 선수별/경기별 기록 데이터를 불러오겠습니다. 

import pandas as pd

file  = './data/KBO_2019_player_gamestats.csv'
raw = pd.read_csv(file, encoding = 'cp949')
raw.head()


# ## Q) 꾸준한 선수? Vs 여름에 힘떨어지는 선수?

# - 월별 기록 정리하기

# In[9]:


# '일자' 컬럼에서 월에 해당하는 값만 선택하여 '월' 컬럼을 추가하겠습니다. 
# 시리즈에서 반복문을 통해 하나씩 계산/점검을 진행하는 방식을 이용하였습니다. 

month_list = []
for monthdate in raw['일자']:
    month, date = monthdate.split('-')
    month_list.append(month)
raw['월'] = month_list


# In[10]:


raw.head()


# In[11]:


raw.info()


# In[12]:


# 분석에 활용할 컬럼만 선택하겠습니다. 
columns_select = ['팀','이름','생일','일자','상대','타수','안타','홈런','루타','타점','볼넷','사구','희비','월']

data = raw[columns_select]
data.head()


# In[13]:


# 피벗 테이블을 이용해 월별 실적을 집계하겠습니다. 
# fill_value = 0 옵션을 이용해 데이터가 비어있는 경우 0을 입력하도록 하였습니다. (해당 월에 실적이 전혀 없으므로 0으로 정리)

data_player_month = data.pivot_table(index = ['팀','이름','생일','월'], 
                                     values = ['타수','안타','홈런','루타','타점','볼넷','사구','희비'], 
                                     aggfunc = 'sum', fill_value = 0)

data_player_month


# In[14]:


# 현재 인덱스로 정리된 팀/이름/생일/월 데이터를 컬럼으로 변경하겠습니다. 
data_player_month = data_player_month.reset_index()
data_player_month


# In[15]:


# 데이터프레임에 포함된 타자의 타율/출루율/장타율/OPS 데이터를 정리하는 함수입니다. 
def cal_hit(df):
    '''
    - 타율 : 공을 쳐서 나가는 비율 --> 안타 / 타수
    - 출루율: 진루해서 나가는 비율 -->  (안타+볼넷+몸에맞는볼)/(타수+볼넷+몸에맞는볼+희생플라이)
    - 장타율 : 타율에 진루한 베이스 가중치 추가 -->   루타 / 타수
    '''
    
    df['타율'] = df['안타'] / df['타수']
    df['출루율'] = (df['안타'] + df['볼넷'] + df['사구']) / (df['타수'] + df['사구'] + df['희비'])
    df['장타율'] = df['루타'] / df['타수']
    df['OPS'] = df['출루율'] + df['장타율']
    return df


# In[16]:


# data_player_month  데이터의 타자별 주요 실적을 계산합니다. 
player_month_stat = cal_hit(data_player_month)
player_month_stat = player_month_stat.dropna()
player_month_stat


# In[17]:


# 월별 출류율 정리하겠습니다.
month_pivot = player_month_stat.pivot_table(index = ['팀','이름','생일'],
                                            columns = '월', 
                                            values = '출루율')

month_pivot = month_pivot.reset_index()
month_pivot


# ### KBO 출루율 최고타자 데이터 불러오기
# 
# 앞서 정리한 선수별 시즌 출루율 기록을 불러오고, 가장 실적이 좋은 타자들의 월별 출루율을 비교해보겠습니다. 

# In[18]:


# 시즌별 타자 실적 데이터를 불러옵니다. 

file = './data/player_stat.csv'
player_stat = pd.read_csv(file, encoding = 'cp949')
player_stat.head(20)


# In[19]:


# 불러온 시즌 기록과, 월별 출루율 데이터를 병합합니다. 

df = pd.merge(player_stat, month_pivot, how = 'left', left_on = ['팀','이름','생일'], right_on = ['팀','이름','생일'])
df.head(10)


# In[20]:


# 출루율 실적을 기준으로 정렬하고, 출루율 상위 50인의 데이터만 가져오겠습니다. 

df_sort = df.sort_values(by = '출루율', ascending = False).head(50)
df_sort


# In[21]:


# 출루율 관련 실적만 선택하겠습니다. 

df_selected = df_sort[['팀', '이름', '출루율', '03', '04', '05', '06', '07', '08', '09', '10']]
df_selected


# 히트맵을 통해 그래프로 살펴볼 예정입니다.   
# 히트맵 작성시에는 데이터프레임의 values 부분은 모두 숫자형 데이터로만 되어있어야 합니다. 
# 
# 현재 팀, 이름 컬럼이 포함되어있어, 이를 인덱스로 변경하겠습니다. 

# In[49]:


# 팀, 이름 컬럼을 인덱스로 지정합니다. --> 모든 컬럼이 수치형 데이터가 되기 위함입니다. 

df_selected = df_selected.set_index(['팀','이름'])
df_selected


# In[50]:


# 그래프 작성 라이브러리 및 한글 폰트 지정을 위한 코드를 실행합니다. 
import matplotlib
from matplotlib import font_manager, rc
import platform
import matplotlib.pyplot as plt
import seaborn as sns

# 이미지 한글 표시 설정
if platform.system() == 'Windows':  # 윈도우인 경우 맑은고딕
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family = font_name)
else:    # Mac 인 경우 애플고딕
    rc('font', family = 'AppleGothic')

#그래프에서 마이너스 기호가 표시되도록 하는 설정입니다.
matplotlib.rcParams['axes.unicode_minus'] = False   


# In[51]:


# 먼저, 기본이 되는 히트맵을 만들어 보겠습니다. 
sns.heatmap(df_selected)


# In[52]:


# 월별 출루율을 히트맵으로 그려보겠습니다. 
# 출루율 실적을 히트맵에 표현하고,  컬러맵은 Reds 를 활용하여 출루율이 높을 수록 붉은색이 진하게 표현되도록 하였습니다. 

# 그림 사이즈 지정
fig, ax = plt.subplots(figsize = (10,10))
sns.heatmap(data = df_selected, 
            annot = True, fmt = '.3f', 
            cmap = 'Reds')


# In[54]:


# 월별 출루율을  시즌 출루율 대비한 +- 값으로 변경하여, 월별 변화 정도를 살펴보겠습니다. 
# 시즌 전체 대비 월별 실적 
for col in df_selected.columns[1:]:
    df_selected[col] = df_selected[col] - df_selected['출루율'] 
df_selected['출루율'] = 0.0


# In[55]:


df_selected


# In[56]:


#  시즌 전체 대비 월별 출루율 증감 실적을 히트맵으로 표현해보겠습니다.
# 이번에는 컬러맵을 Blue ~ Red 로 나타내기 위해 RdBu_r (방향 변경)로 지정하였습니다. 

# 그림 사이즈 지정
fig, ax = plt.subplots(figsize = (10,10))

sns.heatmap(data = df_selected.head(50), 
            annot = True, fmt = '.3f', 
            cmap = 'RdBu_r')

