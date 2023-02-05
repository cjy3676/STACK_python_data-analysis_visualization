#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 타자/경기별 기록 데이터를 불러오겠습니다. 
import pandas as pd

file  = './data/KBO_2019_player_gamestats.csv'
raw = pd.read_csv(file, encoding = 'cp949')
raw.head()


# - 상대 팀별 기록 정리하기

# In[2]:


# unique() 를 통해, 상대 컬럼에 어떠한 값이 들어있는지 살펴보겠습니다. 
raw['상대'].unique()


# In[3]:


# '상대' 컬럼에서   @가 붙어있는 경우에는 원정경기 / 없으면 홈 경기를 의미합니다. 
# '상대' 컬럼에서 홈/원정 여부,  상대팀을 분리하여 각각 '홈어웨이', '상대팀' 컬럼으로 저장하겠습니다. 
opp_list = [ ]
home_away_list = [ ]

for opp in raw['상대']:
    if "@" in opp:
        home_away = '원정'
        opp = opp.replace('@', '')
    else:
        home_away = '홈'
    home_away_list.append(home_away)
    opp_list.append(opp)

raw['홈어웨이'] = home_away_list
raw['상대팀'] = opp_list
raw.head()


# In[6]:


# 상대 팀별 실적을 정리하기 위해 피벗 테이블을 만들겠습니다. 
# 상대팀별 실적 정리
factors = ['타수','안타','홈런', '루타', '타점','볼넷', '사구', '희비']
data = raw.pivot_table(index = ['팀','이름','생일', '상대팀'],
                       values = factors,
                       aggfunc = 'sum')
data.head()


# In[5]:


# 상대팀별 타수가 0보다 큰 경우의 데이터만 선택하겠습니다. 
cond = data['타수'] > 0 
data = data[cond]
data.head()


# In[6]:


# reset_index()를 이용해 인덱스로 지정되어있는 팀/이름/생일 을 컬럼으로 변경하겠습니다. 
data = data.reset_index()
data.head()


# In[7]:


# 타자 주요 실적을 계산하는 함수입니다. 
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


# In[8]:


# 타자/상대팀별 실적을 계산하겠습니다. 
player_stats_opp = cal_hit(data)
player_stats_opp


# ### XXX 팀 킬러?

# In[9]:


# 특정팀을 상대로 강한 타자를 살펴보겠습니다. 
## 먼저, '두산' 팀을 상대로 타수가 10 타수보다 많은 선수중 출루율 상위 10명을 찾아보겠습니다. 

team = '두산'
cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 10)
player_stats_opp[cond].sort_values(by = '출루율', ascending = False).head(10)


# In[10]:


# 이번에는 롯데를 상대로 타수가 20 타수보다 큰 타자중, 출루율 상위 10명을 살펴보겠습니다. 
team = '롯데'
cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 20)
player_stats_opp[cond].sort_values(by = '출루율', ascending = False).head(10)


# In[12]:


# KBO  전체 팀을 대상으로 팀별 출루율 상위 5인 타자를 살펴보겠습니다. 

hitter_df = pd.DataFrame()

for team in player_stats_opp['상대팀'].unique():
    print(team)
    cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 20)
    df = player_stats_opp[cond].sort_values(by = '출루율', ascending = False).head(5)
    hitter_df = hitter_df.append(df)


# In[13]:


# 특정팀 상대 출루율 Top5 이내 들어있는 타자 리스트는 아래와 같습니다
# unique() 명령을 이용해 복수의 팀을 대상으로 top5 에 들어있을 경우 한번만 나타나게 되어있습니다(중복제거)
hitter_df['이름'].unique()


# In[14]:


# 특정팀 상대 출루율 top5 이내 상위타자들을 대상으로  팀별 출루율 피벗테이블을 만들어보겠습니다. 
cond = player_stats_opp['이름'].isin(hitter_df['이름'].unique())
top_df = player_stats_opp[cond]
top_pivot = top_df.pivot_table(index = ['팀','이름'], values = '출루율', columns = '상대팀', aggfunc = 'sum')
top_pivot


# In[16]:


# 그래프 작성 & 한글 폰트 지정 라이브러리 불러오기
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


# In[17]:


# 한번에 살펴보기 위해 히트맵으로 표시해보겠습니다. 

# 그림 사이즈 지정
fig, ax = plt.subplots(figsize = (10,10))
sns.heatmap(data = top_pivot, 
            annot = True, fmt = '.3f', 
            cmap = 'Reds',
            center = 0.4   # 컬러맵 중간값 지정)


# In[19]:


# 히트맵 사용시 center 옵션을 이용해 컬러맵의 기준(색상 변화의 중간이 되는 지점)을 변경할 수 있습니다. 
# center = 0.6 로 해서 표시할 경우,  지정하지 않은 경우 보다 빨간색으로 표시되는 부분이 적어집니다. 
# 상대적인 크기를 살펴보고자 할때  center를 변경하며 살펴볼 수 있습니다. 

# 그림 사이즈 지정
fig, ax = plt.subplots(figsize = (10,10))
sns.heatmap(data = top_pivot, 
            annot = True, fmt = '.3f', 
            cmap = 'Reds',
            center = 0.6   # 컬러맵 중간값 지정)

