#!/usr/bin/env python
# coding: utf-8

# 리스트 + 리스트

# In[2]:


li1 = ['사과', '감', '바나나', '파인애플']
li2 = [1, 3, 5, 7, 9]

li_total = li1 + li2

print(li1 + li2)
print(li2 + li1)
print(li1)
print(li2)
print(li_total)


# 리스트.append()

# In[3]:


li3 = ['원숭이', '코끼리', '바나나']
li4 = [2, 4, 6, 8, 10]

li3.append(li4)
print(li3)


# In[4]:


print(len(li3))


# In[5]:


data = {
    '일자' : '2020-01-1',
    '이름' : '홍길동',
    '전화번호' : '010-0000-1111'
}


# In[6]:


data


# In[7]:


data.keys()


# In[8]:


data.values()


# In[9]:


data.items()


# In[10]:


# dict[키]
data['이름']


# In[11]:


data['나이'] = 20
data

