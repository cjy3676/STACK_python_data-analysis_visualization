#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 판다스 라이브러리를 불러오겠습니다. 
import pandas as pd


# ## 데이터 불러오기

# In[3]:


# 현재 쥬피터노트북 파일 위치 아래에 있는 data 폴더의 babyNamesUS.csv 파일 데이터를 불러오겠습니다. 
file = './data/babyNamesUS.csv'
raw = pd.read_csv(file)


# In[4]:


# head() 를 이용해 상단의 5개 데이터를 살펴보겠습니다. 
raw.head()


# In[5]:


# info() 명령을 이용해 데이터 구조를 살펴볼 수 있습니다. 
# 전체 1048574개의 데이터를 가지고 있으며(인덱스에서 확인)
# 컬럼은 총 5개로 각각 인덱스 개수와 동일하게 1048574개의 데이터를 가지고 있습니다. 
raw.info()


# ## 8. 집계하기(pivot_table)

# ### pd.pivot_table(index = '컬럼명' , columns = '컬럼명' , values = '컬럼명' , `aggfunc` = 'sum')
# 
# `aggfunc` 옵션: sum, count, mean, ...

# - 이름 사용 빈도수 집계하기

# In[6]:


# state, 성별, 출생연도에 상관없이 이름이 등록된 수를 합하여 정리해보겠습니다. 
# 인덱스는 이름으로, 값은 등록된 수를 모두 더하여 피벗 테이블을 만들겠습니다. 
raw.pivot_table(index = 'Name', values = 'Number', aggfunc = 'sum')


# - 이름/성별 사용 빈도수 집계하기

# In[8]:


# 앞서 생성한 데이터에서, 성별 구분을 컬럼에 추가하여 피벗 테이블을 만들겠습니다. 
# 인덱스는 이름으로(index = 'Name'), 값은 등록된 수의 합계(values = 'Number'), 컬럼은 성별로(columns = 'Sex') 구분하여 피벗 테이블을 만들겠습니다. 

name_df = raw.pivot_table(index = 'Name', values = 'Number', columns = 'Sex', aggfunc = 'sum')
name_df.head()


# In[9]:


# 성별/이름별 데이터는 총 20815개의 이름 데이터가 있으며 
# 여자 이름은 14140개, 남자 이름은 8658 개의 데이터가 있는 것을 확인할 수 있습니다. 
name_df.info()


# ## 9. 비어있는 데이터 채워넣기

# 데이터를 정리하다보면, 비어있는 데이터들이 존재하게 됩니다. 
# 비어있는 데이터 부분을 어떻게 정리할지에 따라 분석 결과가 달라질 수도 있습니다. 
# - 공통된 값을 입력하거나(ex 0)
# - 임의의 수를 입력하거나(ex 평균, 최대값, 최소값, 비어있는 자리 주변의 값 등)
# - 비어있는 데이터는 분석에서 제외하거나  
# 
# 여러 방법으로 처리 할 수 있으며, 어떠한 것을 선택할지는 데이터/분석방향 등에 따라 상이합니다. 

# In[18]:


# 데이터가 비어있다는 의미는, 해당 이름이 한 번도 사용된 적이 없다는 의미이므로, 숫자 0을 입력하겠습니다. 
name_df = name_df.fillna(0)
name_df.head()


# In[10]:


# info() 를 통해 데이터를 살펴보겠습니다. 
# 여자(F)와 남자(M) 컬럼 각각 20815개의 데이터를 가지며 전체 데이터 셋의 개수(인덱스 개수 20815개)와 동일한 것을 확인할 수 있습니다. 
name_df.info()


# #### Q) 남자/여자 가장 많이 사용되는 이름은?

# ## 10. 정렬하기

# - name_df.`sort_values`(by = '컬럼명' , ascending = False)

# In[32]:


# 남자이름 사용순위 Top 5
# 여자이름 사용순위 Top 5


# In[11]:


# 남자 컬럼을 기준으로 정렬하겠습니다. 
# 작은 값 부터 큰 값, 오름차순으로 정렬되는 것을 확인할 수 있습니다. 
name_df.sort_values(by = 'M')


# In[12]:


# ascending = False 옵션을 통해 내림차순으로 정렬할 수 있습니다. 
# 남자 컬럼을 기준으로, 내림차순으로 정렬하겠습니다.  

name_df.sort_values(by = 'M' , ascending = False)


# In[14]:


# 남자 컬럼 기준, 내림차순으로 정렬한 데이터의 상위 5개(head()) 이름(index)을 확인해보겠습니다. 
name_df.sort_values(by = 'M', ascending = False).head().index


# In[13]:


# 유사한 방법으로, 여자이름(F)에서 가장 많이 사용된 이름 5개를 확인해보겠습니다. 
name_df.sort_values(by = 'F' , ascending = False).head().index


# ## 11. 컬럼별 데이터 종류 확인하기

# - df['컬럼'].`unique()`
# 
# - df['컬럼'].`value_counts()`

# In[34]:


# StateCode 컬럼에 어떠한 값이 들어있는지 살펴보겠습니다. 
raw['StateCode'].unique()


# In[35]:


# StateCode 컬럼의 값의 종류별로 몇 번 사용되었는지 확인해보겠습니다. 
raw['StateCode'].value_counts()


# In[37]:


# 연도별 데이터 수를 살펴보겠습니다. 
raw['YearOfBirth'].value_counts()

