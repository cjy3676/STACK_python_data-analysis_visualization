#!/usr/bin/env python
# coding: utf-8

# ## 데이터 불러오기

# In[1]:


import pandas as pd


# In[2]:


# 인덱스 번호 다시 매기기
data = pd.read_excel('./data/bycicle.xlsx')


# In[3]:


data.head()


# # 지도 시각화

# In[4]:


import folium


# In[5]:


# 지도 만들기
m = folium.Map(location = ['37.5536067','126.9674308'], zoom_start = 13)   # 서울역 중심
m


# In[6]:


# 지도에 표시할 데이터 준비
for i in range(len(data)):
    lat = data.loc[i, 'stationLatitude']
    long = data.loc[i, 'stationLongitude']
    name = data.loc[i, 'stationName']
    available = data.loc[i, 'parkingBikeTotCnt']
    total = data.loc[i, 'rackTotCnt']
    print(name, available, total, lat, long)


# In[7]:


### 따릉이 지도 만들기 1 ### 

# 지도 생성하기
m = folium.Map(location = ['37.5536067','126.9674308'], zoom_start = 15)

# 마커 추가하기
for i in range(len(data)):
    lat = data.loc[i, 'stationLatitude']
    long = data.loc[i, 'stationLongitude']
    name = data.loc[i, 'stationName']
    available = int(data.loc[i, 'parkingBikeTotCnt'])
    total = int(data.loc[i, 'rackTotCnt'])
    
    # 자전거 수량에 대해 색상으로 표시
    ##  자전거 보유율이 50% 초과일 경우 --> 파란색
    ##  현재 자전거가 2대 보다 적을 경우 --> 빨간색
    ##  그 외의 경우(자전거 2대 이상 이면서, 자전거 보유율 50% 미만) --> 초록색
    if available/total > 0.5:
        color = 'blue'
    elif available < 2 :
        color = 'red'
    else:
        color = 'green'
    icon=folium.Icon(color=color, icon = 'info-sign')
    folium.Marker(location = [lat, long],
                  tooltip = f"{name} : {available}", 
                  icon = icon).add_to(m)
    
m


# In[8]:


# 저장하기
m.save('./map/bicycle_map.html')


# ## 지도시각화(클러스터 & 미니맵)

# In[9]:


from folium.plugins import MiniMap
from folium.plugins import MarkerCluster


# In[22]:


### 따릉이 지도 만들기 2 ### 

# 지도 생성하기
m_ver2 = folium.Map(location = ['37.5536067','126.9674308'], zoom_start = 13)

# 미니맵 추가하기
minimap = MiniMap() 
m_ver2.add_child(minimap)

# 마커 클러스터 만들기
marker_cluster_ver2 = MarkerCluster().add_to(m_ver2)  # 클러스터 추가하기

# 마커 추가하기
for i in range(len(data)):
    lat = data.loc[i, 'stationLatitude']
    long = data.loc[i, 'stationLongitude']
    name = data.loc[i, 'stationName']
    available = int(data.loc[i, 'parkingBikeTotCnt'])
    total = int(data.loc[i, 'rackTotCnt'])
    
    # 자전거 수량에 대해 색상으로 표시
    ##  자전거 보유율이 50% 초과일 경우 --> 파란색
    ##  현재 자전거가 2대 보다 적을 경우 --> 빨간색
    ##  그 외의 경우(자전거 2대 이상 이면서, 자전거 보유율 50% 미만) --> 초록색
    if available/total > 0.5:
        color = 'blue'
    elif available < 2 :
        color = 'red'
    else:
        color = 'green'
    icon=folium.Icon(color = color, icon = 'info-sign')
#     print(name, available, total, lat, long)
    folium.Marker(location = [lat, long],
                  tooltip = f"{name} : {available}", 
                  icon = icon).add_to(marker_cluster_ver2)
    
m_ver2


# In[23]:


# 저장하기
m_ver2.save('./map/bicycle_clustermap.html')

