#!/usr/bin/env python
# coding: utf-8

# ## 자료 받아오기(Open API 활용)

# In[1]:


# API를 이용해 자료를 받아오기 위해 requests 라이브러리를, 자료를 저장하기 위해 pandas 라이브러리를  불러오겠습니다. 

import requests
import pandas as pd


# In[2]:


# 서울열린데이터광장에서 받은 API 인증키를 입력합니다. 
apikey = '424a7064696a6a6134336b476a564c'   # 받은 키 값을 입력하기


# In[3]:


# 요청할 URL 주소를 만들겠습니다. 
# 한번에 최대 1천개까지만 가능하므로, 먼저 1부터 1000번 자전거 정류장의 데이터를 가져오도록 하겠습니다. 
startnum = 1
endnum = 1000
url1 = f'http://openapi.seoul.go.kr:8088/{apikey}/json/bikeList/{startnum}/{endnum}/'


# In[4]:


# 자료를 요청합니다. 
json1 = requests.get(url1).json()


# In[5]:


json1


# In[14]:


# 필요한 정보를 선택하겠습니다. 
json1.keys()


# In[15]:


# 필요한 정보를 선택하겠습니다. 
json1['rentBikeStatus'].keys()


# In[16]:


# 데이터 구조를 확인합니다. 
json1['rentBikeStatus']['list_total_count']  # 데이터의 개수


# In[17]:


# 데이터 구조를 확인합니다. 
json1['rentBikeStatus']['RESULT']  # 오류 여부


# In[18]:


# 데이터 구조를 확인합니다. 
json1['rentBikeStatus']['row']  # 자전거 정류장별 자전거 현황


# In[9]:


# 판다스의 데이터 프레임으로 전환합니다. 
raw1 = pd.DataFrame(json1['rentBikeStatus']['row'])
raw1.head()


# In[6]:


# 다음은 1001번부터 2000번 자전거 정류장의 데이터를 가져오겠습니다. 
startnum = 1001
endnum = 2000
url2 = f'http://openapi.seoul.go.kr:8088/{apikey}/json/bikeList/{startnum}/{endnum}/'
json2 = requests.get(url2).json()


# In[8]:


json2


# In[10]:


# 판다스의 데이터프레임으로 전환합니다. 
raw2 = pd.DataFrame(json2['rentBikeStatus']['row'])
raw2.head()


# In[11]:


# 두 데이터를 통합하겠습니다. 
data = raw1.append(raw2)
data.head()


# In[12]:


data.info()


# In[13]:


# 엑셀 파일로 저장합니다. 
data.to_excel('./data/bycicle.xlsx', index = False)

