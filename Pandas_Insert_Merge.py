#!/usr/bin/env python
# coding: utf-8

# ## 1. pandas 불러오기

# In[1]:


# pandas 라이브러리를 불러오겠습니다. 
import pandas as pd      # pandas라는 라이브러리를 사용할께.  이름은.. pd 라고 짧게 부를께"  라는 의미입니다. 


# ## 2. 데이터 불러오기

# pd.read('엑셀파일경로+명')

# In[3]:


# 엑셀 파일의 데이터를 읽어오겠습니다. 
fpath = './data/exam.xlsx'
data = pd.read_excel(fpath, index_col = '번호')  # index_col 은 인덱스로 사용할 컬럼을 지정할 수 있습니다(컬럼명, 컬럼번호 지정 가능)


# ### 데이터 살펴보기

# In[3]:


# 데이터를 살펴보겠습니다. head() 명령을 통해 상위 데이터를 살펴볼 수 있습니다. 
data.head()


# In[4]:


# info() 명령을 통해 인덱스/컬럼 구조에 대해 살펴보겠습니다. 
data.info()


# In[5]:


# describe() 명령을 통해, 수치형 데이터가 들어있는 국어/영어/수학 컬럼의 기초통계량을 살펴보겠습니다. 
data.describe()


# ## 5. 데이터 추가하기

# #### df['컬럼명'] = `data`   
# 
# ※ `data`에 들어갈 수 있는 것
#     - 하나의 값: 전체 모두 동일한 값 
#     - 그룹: 리스트, 판다스의 시리즈
#     
# ※ 새로운 컬럼을 만들 경우에는   `df.컬럼명` = data 형태는 사용 불가. (`df['컬럼명']` 으로만 가능)

# In[6]:


# data['컬럼명'] 을 이용해 하나의 컬럼을 선택할 수 있습니다. 
data['수학']


# In[4]:


# 하나의 컬럼을 선택한 뒤, 하나의 값으로 입력할 경우 전체가 동일한 값을 가진 시리즈를 입력할 수 있습니다. 

data['음악'] = 90             
data.head()


# In[5]:


# 여러 개의 값을 그룹(리스트나 시리즈 형태)으로 입력할 경우, 위에서부터 순서대로 해당 값을 가진 시리즈를 입력할 수 있습니다. 
# 여러 개의 값(그룹) 으로 값 입력 할 경우
data['체육'] = [100, 80, 60]
data.head()


# 컬럼 간의 계산을 통해 신규 컬럼을 만들 수도 있습니다. 

# In[11]:


# 사칙연산도 가능함(컬럼끼리 연산)
data['국영수'] = (data['국어'] + data['영어'] + data['수학']) / 3
data.head()


# ## 6. 데이터 표 병합하기

# 두 개의 엑셀파일에서 데이터를 불러온 뒤, 데이터를 병합하겠습니다. 

# In[7]:


# 첫번째 데이터 불러오기
fpath = './data/exam.xlsx'
A = pd.read_excel(fpath, index_col = '번호')
A.head()


# #### 요청! `두 과목 점수가 누락되었어요. 점수를 추가해주세요~!!!!`

# In[8]:


# 두 번째 데이터 불러오기
fpath2 = './data/exam_extra.xlsx'
B = pd.read_excel(fpath2, index_col = '번호')
B.head()


# ### 데이터 병합하기 : pd.`merge`( A,  B, how = `'left'`,  left_on = `'A컬럼명'`, right_index = `True`)
# 
# `how` : 
# 
#     - left(왼쪽 표 기준)  
#     - right(오른쪽 표 기준)   
#     - inner(A,B 둘 다 있는 데이터만)  
#     - outter(A,B 한쪽이라도 있는 데이터)
# 
# `left_on` : A 병합 기준 컬럼 지정 
# 
# `left_index = True`  :  A 병합 기준 인덱스로 지정
# 
# 
# `right_on` : B 병합 기준 컬럼 지정
# 
# `right_index = True ` : B 병합 기준 인덱스로 지정
# 
# 
# `on` :   A & B  같은 이름의 열을 기준으로 지정할 경우  

# In[15]:


# 엑셀의 Vlookup 처럼 합쳐봅시다!
# A, B 테이블을 A테이블에 있는 키 값을 기준으로,   
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하겠습니다. 

total = pd.merge(A, B, how = 'left', left_index = True, right_index = True)
total.head()


# In[17]:


# A, B 테이블을   B테이블에 있는 키 값을 기준으로,   
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하겠습니다. 
pd.merge(A, B, how = 'right', left_index = True, right_index = True)


# In[18]:


# A, B 테이블을   A, B 테이블 양쪽에 모두 존재하는 키 값을 기준으로, 
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하겠습니다. 
pd.merge(A, B, how = 'inner', left_index = True, right_index = True)


# In[19]:


# A, B 테이블을   A, B 테이블 양쪽에 한번이라도 존재하는 모든 키 값을 기준으로, 
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하겠습니다. 
pd.merge(A, B, how = 'outer', left_index= True, right_index=True)


# ## 7. 저장하기

# ### pd.to_excel('파일경로+파일명.xlsx', index = False)

# In[9]:


# 앞에서 병합한 데이터를 살펴보겠습니다. 
total = pd.merge(A, B, how = 'left', left_index = True, right_index = True)
total


# In[10]:


# 현재 폴더 내의 data 폴더 내에 exam_total.xlsx 파일에 저장하겠습니다. 
total.to_excel('./data/exam_total.xlsx')


# In[11]:


# 판다스의 데이터프레임에서는 항상 인덱스 값을 가지게 됩니다.
# 인덱스를 저장하고 싶지 않을때에는  저장시에 index = False 옵션을 사용하시면 됩니다. 
total.to_excel('./data/exam_total_withoutindex.xlsx', index = False)

