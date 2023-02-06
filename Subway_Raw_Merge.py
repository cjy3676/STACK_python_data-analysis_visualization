#!/usr/bin/env python
# coding: utf-8

# In[15]:


# 필요한 라이브러리를 불러오겠습니다. 
import pandas as pd 


# # 1. raw 파일 불러오기
# 
# - 일자/노선/지하철역별 승하차고객수
# - 19년 상반기(19년1월~19년6월)

# ./rawfiles 폴더의 파일들을 살펴볼께요

# In[16]:


# 작업할 여러개의 파일 중 하나의 파일을 불러오겠습니다. 
file = './rawfiles/CARD_SUBWAY_MONTH_201901.csv'
raw = pd.read_csv(file)     


# In[17]:


raw.head()


# In[18]:


# info() 를 이용해 데이터 구조를 살펴볼 수 있습니다. 
raw.info()


# ---

# ## 참고) 판다스로 파일 읽어오기

# ### 데이터 파일 읽기: read_excel    /   read_csv
# - `pd.read_excel`('파일경로+파일명.xlsx')
# 
# - pd.read_csv('파일경로+파일명.csv', encoding = 'utf-8')
# - pd.read_csv('파일경로+파일명.csv', encoding = 'cp949')   # MS 엑셀에서 저장한 경우
# 
# #### 자주 사용하는 옵션
# - pd.read_excel('파일경로', `옵션1` = 값1, `옵션2` = 값2 ....)
# - 옵션 종류
#     - index_col  = 컬럼인덱스번호       # 몇번째 컬럼을 인덱스로 지정할 것인지 선택
#     - header = row인덱스번호    # 몇번째 row 부터 표 데이터로 볼 것인지 선택
#     - thousands = ','       # 천 단위 기호 ,  사용 -->  xxx,xxx  문자가 아닌 숫자로 인식
#     
# ##### 참고   https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

# ---

# In[19]:


# 이번엔 여러 파일을 불러오겠습니다. 
# 2개 파일 불러와서 합치기!!!!

raw = pd.DataFrame()  # 빈 데이터 셋을 만들고
raw.head()

# 첫 번째 파일
file = './rawfiles/CARD_SUBWAY_MONTH_201901.csv'
temp = pd.read_csv(file)

# temp.head()
raw = raw.append(temp)  # 추가하기
raw.head()

# 두 번째 파일
file = './rawfiles/CARD_SUBWAY_MONTH_201902.csv'
temp = pd.read_csv(file)
raw = raw.append(temp)  # 추가하기

raw.info()


# ####    Q) 폴더에 있는 모든 파일을 불러와서 병합할 수 있을까?

# In[20]:


# 폴더/파일을 관리하는 os 라이브러리를 불러옵니다. 
import os


# In[21]:


# os.listdir()을 이용해 rawfiles 폴더에 있는 파일 리스트를 살펴보겠습니다. 
dirpath = './rawfiles/'
files = os.listdir(dirpath)
files


# In[22]:


# 여러개의 파일을 병합하겠습니다. 
# 반복문 -> csv 파일 읽기 -> 데이터프레임에 추가하기

# 빈 데이터프레임 준비하기
raw = pd.DataFrame() 

# 파일 하나씩 불러들여 합치기
for file in os.listdir('./rawfiles'):
#     print(file)
    fpath = './rawfiles/' + file
    print(fpath)
    temp = pd.read_csv(fpath)
    raw = raw.append(temp, ignore_index = True)   #ignore_index = True  --> 기존 인덱스는 무시하고
    
# raw = raw.reset_index(drop = True)


# ----

# ### 데이터 살펴보기:  data.head(),  data.info(),  data.describe()

# In[23]:


raw.head(10)


# In[10]:


raw.tail()


# In[11]:


# 데이터는 이렇게 생겼어요. 
raw.info()


# ---

# #### Q) 요일을 추가 할 수 있을까?

# In[26]:


# 일시를 관리하는 datetime 라이브러를 불러오겠습니다. 
from datetime import datetime


# datetime.strptime('날짜str', `str형태`)  : 문자 --> 날짜 타입
# 
# - `str형태` %Y-%m-%d %H:%M:%S
#     - %Y : 연도(4자리)
#     - %m:  월(2자리)
#     - %d:  일자(2자리)
#     
#     - %H : 시간
#     - %M : 분
#     - %S : 초

# In[31]:


# datetime.strptime()를 이용해 str 타입을  날짜 타입으로 변경하겠습니다.
# datetime.strptime('날짜str', 형태)
date_str = str(20230206)     # 숫자가 아닌 문자로 입력되어야 합니다. 
date = datetime.strptime(date_str, "%Y%m%d")
date


# In[32]:


# 날짜 타입을 요일로 변경하기 위해서는 weekday() 를 사용합니다. 
# 월요일 : 0 ~ 일요일 : 6
weekday = date.weekday()
weekday


# In[29]:


# 날짜 컬럼을 불러와서, 순서대로 요일을 점검하여 리스트에 저장하겠습니다. 

weekday_dict = [ '월','화','수','목','금','토','일']
weekday_list = []

for date_str in raw['사용일자']:
    date = datetime.strptime(str(date_str), "%Y%m%d")
    weekday_index  = date.weekday()
    weekday = weekday_dict[weekday_index]
    weekday_list.append(weekday)


# In[30]:


# 요일정보가 저장된 리스트를 컬럼에 추가하겠습니다. 
raw['요일'] = weekday_list
raw.head()


# In[33]:


raw.sample(10)


# In[18]:


# 요일을 사용일자 다음에 나오도록 컬럼 순서를 변경하겠습니다. 

# 현재 컬럼명 확인
raw.columns


# In[34]:


# 요일을 사용일자 다음에 나오도록 컬럼 순서를 변경하겠습니다. 

# 사용하고 싶은 컬럼을 원하는 순서대로 입력합니다. 
new_columns = ['사용일자',  '요일', '노선명', '역ID', '역명', '승차총승객수', '하차총승객수', '등록일자']
raw = raw[new_columns]
raw.head()


# # 2. 정리한 데이터 저장하기

# In[36]:


# 작업한 결과를 data 폴더에 저장하겠습니다. 
fpath = './data/subway_raw.xlsx'
raw.to_excel(fpath, index = False)

