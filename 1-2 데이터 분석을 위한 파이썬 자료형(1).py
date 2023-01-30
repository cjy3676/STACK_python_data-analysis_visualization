#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 변수 = 값/데이터
x = 1 
print(x)


# In[2]:


y = 3
y = 11
print(y)


# In[3]:


# int, float
x = 15
print(type(x))


# In[4]:


y = 9.5
print(type(y))


# In[5]:


a = 9
b = 5

print(a + b)
print(a - b)
print(a * b)
print(a / b)


# In[6]:


print(a // b) # 몫
print(a % b) # 나머지


# In[7]:


# str
s1 = '가가'
print(type(s1))


# In[8]:


s2 = '가나다라마바사'
s2


# In[9]:


s3 = '산'
s4 = '토끼'
print(s3 + s4)


# In[10]:


# list 
# 리스트명 = [원소1, 원소2, ... , 원소n]
li = [1, 2, 3, 4, 5]
print(li)


# In[11]:


li = [1, 2, 3, 5.5, '빨강', '파랑', [1, 2, 3, 4]]
print(li)


# In[13]:


li = ['가', '나', '다', '라', '마']
    #  0    1     2    3     4
    # -5   -4    -3   -2    -1

# 다
print(li[2])
print(li[-3])

# 라 
print(li[3])
print(li[-2])


# In[14]:


li = ['가', '나', '다', '라', '마']
    #  0    1     2    3     4
    # -5   -4    -3   -2    -1
    
# 슬라이싱
# 리스트이름[시작인덱스번호 : 마지막인덱스번호]

# 나, 다, 라
print(li[1 : 4])
print(li[-4 : 4])
print(li[-4 : -1])
print(li[1 : -1])


# In[15]:


print(li[1 : ])
print(li[ : 4])


# In[16]:


print(len(li))


# In[17]:


len('문자열')

