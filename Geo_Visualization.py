#!/usr/bin/env python
# coding: utf-8

# # 지도시각화하기

# In[2]:


# 지도시각화를 위해 folium 라이브러리를 사용하겠습니다. 
import folium


# In[1]:


# 설치하기: folium  라이브러리가 설치되어 있지 않다면, 아래 라인의 코드에서 # 기호를 없애 주석 해제하고 실행하시면 됩니다. 
get_ipython().system(' pip install folium')


# ## 지도 시각화
# - 지도생성하기
#     - `m` = folium.Map(location = [위도, 경도],  zoom_start = 확대정도)
# 
# - 정보 추가하기
#     - 마커 추가하기
#         - folium.Marker([위도, 경도]).add_to(`m`)
#     - 원 추가하기
#         -     folium.CircleMarker([위도, 경도],radius= 원크기).add_to(`m`)
#     - 추가옵션: 
#         - tooltip="마우스 올리면 보여질 정보"
#         - popup="클릭하면 보여질 정보"          
#     - 기타) ClickForMarker('체크').add_to(`m`)  지도에서 클릭할 경우 마커 추가하기

# In[5]:


# 지도 생성하기
# 먼저, 지도를 펼쳐야 합니다.  지도에서 어느 부분을 살펴볼 것인지, 지도 중심의 좌표를 위도, 경도를 이용해 지정해야 합니다. 
# 서울역을 기준으로 살펴보겠습니다. 
# zoom_start 옵션을 통해, 처음에 얼마나 확대해서 볼 것인지를 지정할 수 있습니다. 
# 지도가 생성된 뒤에 위치 이동이나 확대/축소를 조정할 수도 있습니다. 
m = folium.Map(location = [37.5536067,126.9674308],   # 기준좌표 : 서울역
               zoom_start = 12)
m


# In[4]:


# Marker( [위도, 경도]).add_to(지도이름) 명령을 통해 지도상에 마커를 추가할 수 있으며
# tooltip, popup 옵션을 통해 설명을 추가할 수 있습니다. 

# 마커 추가하기
folium.Marker([37.5536067,126.9674308] ,    # 서울역위치
              tooltip = "서울역(마우스올리면보여짐)",
              popup = "서울역(클릭하면 보여짐)",
              ).add_to(m)
m


# In[6]:


# CircleMarker( [ 위도, 경도]).add_to(지도이름) 명령을 통해, 동그라미를 지도에 표시할 수 있습니다. 
# 이때 radius 옵션을 통해 동그라미의 크기를 지정할 수 있습니다. 

# 써클마커 추가하기
folium.CircleMarker([37.5536067,126.9674308],
                    radius = 20,
                    tooltip = '마우스올릴경우'
                   ).add_to(m)
m


# ### 미니맵을 추가할 경우 MiniMap

# In[7]:


# folium에는 다양한 효과를 줄 수 있는 plugins 이 존재 하는데, MiniMap 도 그 중 하나 입니다. 
# 미니맵을 지도 우측 하단에 추가하여, 현재 어느 위치를 살펴보고 있는지 점검할 수도 있습니다. 

from folium.plugins import MiniMap

# 지도 생성하기
m = folium.Map(location=[37.5536067,126.9674308],   # 기준좌표 : 서울역
               zoom_start=12)

# 미니맵 추가하기
minimap = MiniMap() 
minimap.add_to(m)


# 마커 추가하기
folium.Marker([37.5536067,126.9674308],    # 서울역위치
              tooltip="서울역(마우스올리면보여짐)",
              popup="서울역(클릭하면 보여짐)",
              ).add_to(m)
m


# ### 지도에서 표시를 추가하고 싶을때: ClickForMarker

# In[12]:


# 모든 정보를 처음부터 지도에 추가하지 않고, 이후에 마우스를 이용해 추가할 수 있도록 만들 수도 있습니다. 

# 지도 생성하기
m = folium.Map(location=[37.5536067,126.9674308],   # 기준좌표: 서울역
               zoom_start=12)

# 써클마커 추가하기
folium.CircleMarker([37.5536067,126.9674308],
                    radius = 20,
                    tooltip = '마우스올릴경우'
               ).add_to(m)
folium.ClickForMarker('체크추가').add_to(m)    
m


# ## 서울 대피소 현황 지도 만들기

# 서울 대피소 현황 자료를 다운받아 이를 지도에 시각화 해보겠습니다. 

# In[8]:


# csv파일의 표 형태 데이터를 읽어오기 위해 판다스를 불러옵니다. 
import pandas as pd


# In[9]:


# 서울열린데이터광장에 있는 서울시 대피소 현황 자료를 다운 받고, 판다스로 조회하겠습니다. 
# 서울 대피소 현황 자료 다운받기
# http://data.seoul.go.kr/dataList/OA-2189/S/1/datasetView.do
file = './data/서울시 대피소 방재시설 현황 (좌표계_ WGS1984).csv'
raw = pd.read_csv(file, encoding = 'cp949')   # encoding = 'cp949' : MS 프로그램 사용시,   그외의 경우 encoding = 'utf-8'  (기본값)


# In[10]:


# 파일에서 읽어온 데이터를 살펴보겠습니다. 
raw.head()


# In[11]:


# 인덱스번호가 0인 경우, 위도와 경도 데이터를 출력해보겠습니다. 

i = 0

lat = raw.loc[i , '위도']
long = raw.loc[i , '경도']
name = raw.loc[i , '대피소명칭']

print(lat , long , name)


# In[12]:


# 모든 인덱스 번호에 대해서 위도,경도, 명칭을 출력해보겠습니다. 
for i in range(len(raw)):
    lat = raw.loc[i , '위도']
    long = raw.loc[i , '경도']
    name = raw.loc[i , '대피소명칭']

    print(name , lat , long)    


# In[21]:


# 지도를 생성한 뒤, 위도/경도에 맞게 지도에 마커를 추가하겠습니다. 

# 지도 생성하기
m = folium.Map(location = [37.5536067 , 126.9674308] , zoom_start = 12)
m
# 대피소 마커 추가하기

for i in range(len(raw)):
    lat = raw.loc[i , '위도']
    long = raw.loc[i , '경도']
    name = raw.loc[i , '대피소명칭']

    folium.Marker([lat , long],tooltip = name).add_to(m)    
m


# ### 마커가 너무 많을때에는 살펴보는 것이 어려울 수 있습니다. 
# ### --> ClusterMarker를 이용해  근처에 있는 마커들끼리는 그룹으로 표현

# In[14]:


# MarkerCluster 라이브러리를 불러오겠습니다. 
from folium.plugins import MarkerCluster


# In[15]:


# MarkerCluster 를 이용해 대피소 정보를 지도에 시각화 하겠습니다. 

# 지도 생성하기
m = folium.Map(location = [37.5536067 , 126.9674308] , zoom_start = 12)
marker_cluster = MarkerCluster().add_to(m)  # 클러스터 추가하기

# 대피소 마커 추가하기

for i in range(len(raw)):
    lat = raw.loc[i , '위도']
    long = raw.loc[i , '경도']
    name = raw.loc[i ,'대피소명칭']
    folium.Marker([lat , long],
                  tooltip = name).add_to(marker_cluster)    
m


# In[16]:


raw.head()


# ### 미니맵 추가하고 싶을때에는
# ## MiniMap

# In[22]:


# 앞서 살펴봤떤 미니맵도 추가해보겠습니다. 
from folium.plugins import MiniMap


# In[23]:


# 미니맵과 클러스터 마커를 이용하여   서울 대피소 지도를 만들겠습니다. 

# 위치명 / 수용인원 등 추가 정보 추가하여 지도 만들기
# 지도 생성하기
m = folium.Map(location = [37.5536067 , 126.9674308] , zoom_start = 12)

# 클러스터 만들기
marker_cluster = MarkerCluster().add_to(m)

# 미니맵 추가하기
minimap = MiniMap() 
m.add_child(minimap)

# 대피소 마커 추가하기

for i in range(len(raw)):
    lat = raw.loc[i , '위도']
    long = raw.loc[i , '경도']
    name = raw.loc[i , '대피소명칭']
    folium.Marker([lat , long] , tooltip = name).add_to(marker_cluster)    
m


# In[20]:


# 이렇게 생성한 지도를 html 확장자로 저장할 경우, 
# 필요할때에는 언제나 다시 열어서 지도를 움직여 가며 정보를 확인할 수 있습니다. 
# 지도를 저장해보겠습니다.

m.save('./data/Sheltermap.html')

