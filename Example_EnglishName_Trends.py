#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 판다스 라이브러리를 불러옵니다. 
import pandas as pd


# In[2]:


# 엑셀 파일을 불러오겠습니다.  
# 현재 쥬피터노트북 파일 위치 기준으로(./) data 폴더 내의 babyNamesUS.csv 파일입니다. 
file = './data/babyNamesUS.csv'
raw = pd.read_csv(file)


# In[3]:


raw.head()


# In[4]:


raw.info()


# ## Q) 남자 여자 구분없이 사용되는 공통 이름은?  

# In[6]:


# 남성, 여성별 등록된 이름 횟수를 정리하겠습니다. 

# 피벗 테이블을 이용해 이름/성별에 따른 등록 회수를 정리합니다. 
name_df = raw.pivot_table(index = 'Name' , columns = 'Sex' , values = 'Number' , aggfunc = 'sum')

# 비어있는 데이터에 0을 입력합니다. 
name_df = name_df.fillna(0)

# 소수점 형태의 실수 형태로 되어있어, 이를 int 정수형으로 변경합니다. 
name_df = name_df.astype(int)
name_df.head()


# - 남자/여자 비율 차이가 적을수록 --> 성별 구분 없는 이름! 

# In[7]:


## 남자/여자 이름 등록수 합계를 계산합니다. 
name_df['Sum'] = name_df['M'] + name_df['F']
name_df.head()


# In[9]:


# 남자/여자 등록 비율을 계산합니다. 
name_df['F_ratio'] = name_df['F'] / name_df['Sum']
name_df['M_ratio'] = name_df['M'] / name_df['Sum']

# 두 비율의 차이를 계산합니다. 
name_df['M_F_Gap'] = abs(name_df['F_ratio'] - name_df['M_ratio'])    # abs() --> 절대값
name_df.head()


# In[10]:


# 이름이 가장 많이 사용된 수를 기준으로 내림차순으로 정렬합니다. 
name_df = name_df.sort_values(by = 'Sum' , ascending = False)
name_df.head(20)


# In[11]:


# 남자/여자 사용비율의 차이가 0.1보다 작은 경우를 찾습니다. 
cond = name_df['M_F_Gap'] < 0.1
name_df[cond].head(10)


# In[12]:


### 남자/여자 구분없이 가장 많이 사용되는 이름은 아래와 같습니다. 
name_df[cond].head(10).index


# ### James, Mary 가 가장 대표적인 미국 이름???   

# ## Q) 가장 대표적인 미국이름은??  
# 
# - 전 기간 합계
# - 최근 트렌드에 따른

# In[14]:


raw.head()


# In[15]:


# unique() 를 통해, 기간에 들어가는 값들을 살펴봅니다. 
raw['YearOfBirth'].unique()


# #### 세대 기준으로 그룹 만들기
# 한 세대 나누는 기준 30년 :  2020년 기준 30년씩 구분
# - 1930년대 이전 
# - 1960년대 이전 
# - 1990년대 이전 
# - 2020년 이전

# In[20]:


# 출생연도 시리즈에서 순서대로 해당하는 세대 그룹명에 매칭하고 그 결과를 리스트에 저장합니다. 
year_class_list = [ ]

for year in raw['YearOfBirth']:
    if year <= 1930: 
        year_class = '1930년이전'
    elif year <= 1960: 
        year_class = '1960년이전'
    elif year <= 1990:
        year_class = '1990년이전'
    else:
        year_class = '2020년이전'
    year_class_list.append(year_class)


# In[21]:


# 세대 그룹명이 저장된 리스트를 컬럼으로 추가합니다. 
raw['year_class'] = year_class_list
raw.head()


# In[19]:


# pivot_table()을 활용하여 이름/성별, 세대별 이름 등록수 합계 표를 구합니다. 
# index = ['Name', 'Sex'] , columns = 'year_class' , values = 'Number' , aggfunc = 'sum'
name_period = raw.pivot_table(index = ['Name', 'Sex'] , columns = 'year_class' , values = 'Number' , aggfunc = 'sum')

# 비어있는 값에 0 추가 fillna(0)
name_period = name_period.fillna(0)
name_period = name_period.astype(int)
name_period.head()


# #### 전체 컬럼 합계 계산하기
# - 모든 컬럼을 하나씩 더하기 : df['컬럼1'] + df['컬럼2'] + ... + df['컬럼n']  
# - sum() 활용하기: df.`sum(axis = 1)`
#     - 참고) df.sum() 을 활용하면, 기본값으로 axis = 0 으로 지정되며, 컬럼별 합계가 아닌 row 별 합계가 계산됩니다. 

# In[22]:


# sum(axis = 1)을 활용하여 컬럼별 합계를 추가합니다. 
name_period['sum'] = name_period.sum(axis = 1)
name_period.head()


# In[24]:


# 모든 컬럼을 컬럼별 합계로 나누어, 세대별 등록 비율을 계산합니다. 
# 계산된 값은 기존컬럼 뒤에 "비율" 이름을 추가한 신규컬럼에 저장합니다. 

for col in name_period.columns:
    col_new = col + "비율"
    name_period[col_new] = name_period[col] / name_period['sum']
    
name_period.head()


# In[25]:


# 이름 사용수 합계, 2020년 이전 비율, 1990년이전 비율 기준으로 내림차순하여 정리합니다. 
name_period = name_period.sort_values(by = ['sum' , '2020년이전비율' , '1990년이전비율'], ascending = False)
name_period


# In[32]:


# 인덱스가 여러 레벨로 되어있을 경우, 인덱스를 활용해 컨트롤 하는 것은 복잡하기때문에 
# reset_index()를 활용하여 인덱스로 설정된 이름과 성별을 컬럼으로 변경합니다. 

name_period = name_period.reset_index()


# In[28]:


# 남자 이름만 선택해서 살펴봅니다. 
cond = name_period['Sex'] == 'M'
name_period[cond].head(10)

# => 상위로 사용되는 James, Robert, John의 경우 1960년대 사용비율이 40% 이상으로, 최근에는 사용 비율이 적다. 


# In[31]:


# 이번에는 여자이름을 살펴보겠습니다. 
cond = name_period['Sex'] == 'F'
name_period[cond].head(10)

# => Mary는 60년대 이전이 50% 이상 사용되었습니다. 최근에는 사용 비율이 낮습니다. 
# => 순위 상위권에서 보면 Jessica, Sarah, Ashley 가 눈에 띄네요, 2020년 이전 사용 비율이 높습니다. 


# In[29]:


# 2020년 이전 비율이 30% 보다 큰 경우에 해당하는 이름만 살펴볼까요?
# => 남자의 경우에는 아래와 같습니다. 

cond_age = name_period['2020년이전비율'] > 0.3
cond_sex = name_period['Sex'] == 'M'
cond = cond_age & cond_sex
name_period[cond].head(5)


# In[30]:


# 2020년 이전 비율이 30% 보다 큰 경우에 해당하는 이름만 살펴볼까요?
# => 여자의 경우에는 아래와 같습니다. 

cond_age = name_period['2020년이전비율'] > 0.3
cond_sex = name_period['Sex'] == 'F'
cond = cond_age & cond_sex
name_period[cond].head(5)

