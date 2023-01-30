#!/usr/bin/env python
# coding: utf-8

# # 3. 파이썬 기초 문법

# ### 3.1.반복문

# `
# for name in group:`    <-- "group에서 순서대로 하나씩 꺼낸다. 이때 꺼낸 것을 name 이라고 부른다"
# 
# 이후 들여쓰기가 끝나는 곳까지 반복 실행
#     
#     

# cf) 리스트 : 그룹으로 묶는 것 Vs 반복문 : 하나씩 꺼내어 작업하는 것.

# In[2]:


# 반복문을 통해 리스트에서 원소를 순서대로 하나씩 꺼내어 작업할 수 있습니다. 
fruits = ['바나나','사과','딸기','배','감']

for f in fruits:   
    print(f)


# In[3]:


# 반복문이 실행되는 범위는 들여쓰기를 이용하여 표시합니다. 
fruits = ['바나나','사과','딸기','배','감']

for fruit in fruits:   
    print(fruit)
    
print(5)


# In[4]:


# 반복문이 실행되는 범위는 들여쓰기를 이용하여 표시합니다. 
fruits = ['바나나','사과','딸기','배','감']
for fruit in fruits:   
    print(fruit)
    
    print(1)             # 들여쓰시가 되어있기 때문에 이 라인까지 반복문이 실행됩니다. 
print(5)


# ### 3.2.조건문

# `if 조건1:`
# 
#     조건1이 True 일 경우 실행되는 코드
#     
# `elif 조건2:`
# 
#     조건1이 False 이면서, 조건2가 True 일 경우 실행되는 코드
#     
# `else:`
# 
#     위 조건들이 모두 False 일때, 실행되는 코드

# In[ ]:


#  홀 / 짝 을 판단하고 출력해보겠습니다. 

n = 20   # 자연수 입력

if n <= 0:        # 0이하의 수라면 다시 입력하라는 메세지를 출력하빈다. 
    print('1 이상의 자연수를 입력해주세요')
elif n % 2 == 0:  # 2로 나누었을때 나머지가 0인 경우 -> 짝수입니다. 
    print('짝수 입니다')
else:             # 2로 나누었을때 나머지가 0이 아닌 경우 -> 홀수 입니다. 
    print('홀수 입니다')


# 크기비교

# In[6]:


# > < 부등호를 이용해 크기 비교를 할 수 있습니다. 

shop_A = ['사과','배','파인애플']
shop_B = ['딸기','포도','사과', '배']

if len(shop_A) > len(shop_B):
    print('shop_A의 과일 종류가 더 많다')
elif len(shop_A) < len(shop_B):
    print('shop_B의 과일 종류가 더 많다')
else:
    print('두 매장에서 파는 과일의 종류 수는 동일하다')


# 포함여부

# In[9]:


# 원소 in 그룹 을 이용해 포함여부를 점검할 수 있습니다. 
shop_A = ['사과','배','파인애플']
if "딸기" in shop_A:
    print("shop_A 에서 딸기를 판매한다")
else:
    print("shop_A 에서 딸기를 판매하지 않는다")


# In[8]:


# 원소 not in 그룹 을 이용해 불포함여부를 점검할 수 있습니다. 
shop_A = ['사과','배','파인애플']
if "포도" not in shop_A:
    print("shop_A 에서 포도를 판매하지 않는다")
else:
    print("shop_A 에서 포도를 판매한다")


# 일치 여부

# In[10]:


# ==  기호를 이용해 같은지 여부를 판단할 수 있습니다. 

A = '태극기'
B = '태극기가 바람에 펄럭입니다'

if A == B:
    print('완전 동일')
elif A in B:
    print("A가 B에 포함된다")
else:
    print("다르다")


# ### 3.3.문자열 포매팅/정리하기

# 문자열 포매팅

# In[13]:


# 문자열에서 고정된 값이 아닌, 변수(변하는 값)을 표시하게 할 수도 있습니다. 이를 포매팅이라고 합니다. 

name = '홍길동'
sentence = f'안녕하세요. {name}님 만나서 반갑습니다.'

print(name)
print(sentence)


# In[20]:


# 파이썬 3.6 버전부터  f"문자열 {변수명}" 형태로 사용이 가능합니다. 
# 파이썬 3.5 버전 이하에서는 아래와 같이 사용가능합니다. 

name = '홍길동'
sentence = '안녕하세요. {}님 만나서 반갑습니다.'.format(name)
print(name)
print(sentence)


# In[18]:


# 여러개의 변수도 표현 가능합니다. 
# 이때에는 { } 순서대로 변수를 입력해주어야 합니다. 

month = "12월"
day = "25일"

sentence = "오늘은 {} {} 입니다".format(month, day)   
print(sentence)


# strip()

# In[24]:


# 문자열에서,  줄바꿈문자는 \n으로,  탭 문자는 \t 로 표현합니다
raw = '\n\t 태극기가 바람에 펄럭입니다. \n 하늘 높이 하늘 높이 펄럭입니다. '
print(raw)


# In[26]:


# 문자열.strip() 명령을 통해,  문자열 시작과 끝 부분의 공백문자(줄바꿈/띄어쓰기/탭문자 등)을 제거할 수 있습니다. 
raw_strip = raw.strip()
print(raw_strip)


# replace(변경전, 변경후)

# In[27]:


# 문자열.replace( ) 명령을 통해 특정 문자열을 없애거나 변경할 수 있습니다. 
raw_edit = raw_strip.replace('하늘 높이', '하늘높이')
print(raw_edit)


# split()

# In[29]:


# split()을 이용해 특정 문자열을 기준으로 문자열을 나눌 수 있습니다. 
# split() 결과는 리스트 타입입니다. 
data = "미국/중국/일본/러시아/베트남/태국"
data.split('/')


# ### 3.4. 함수 만들기

# 반복적으로 사용하는 코드들에 이름을 붙여서 쉽게 사용할 수 있게 하는 것을 함수라고 합니다. 
함수는 아래와 같은 구조를 가지게 됩니다. 

def 함수이름(변수1, 변수2, ...변수n):  
    함수 실행내용  
    return 실행결과  
# In[5]:


# 두 수를 곱한 결과 텍스트를 반환하는(알려주는) 함수를 만들어보겠습니다. 
# 이 코드를 실행하면 컴퓨터는 gob() 이라는 명령어에 대해서 알게 됩니다.
# (코드에 이름표를 붙이는 과정이지, 계산을 실행하지는 않습니다. )

def gob(a, b):
    gob = a*b
    text = '{} x {} = {}'.format(a, b, gob)
    return text


# In[6]:


# 이번에는 위에서 정의한 함수를 실행해 볼까요

a = 2
b = 8

text = gob(a,b)
print(text)


# ## 실습) 구구단 출력하기

# In[7]:


for i in [2,3,4,5,6,7,8,9]:
    for j in [1,2,3,4,5,6,7,8,9]:
        text = gob(i,j)
        print(text)
    print("*"*50)   # 단 마다 구분하기 위한 구분선

