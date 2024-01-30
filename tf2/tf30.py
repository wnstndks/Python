# -*- coding: utf-8 -*-
"""tf30.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IAIUGRDB713HgeZePduqVSxmUkBX0jLo

# 글자 수준의 LSTM 텍스트 생성 모델 구현

https://ml-ko.kr/dl-with-python/8.1-text-generation-with-lstm.html 참고
"""

import keras
import numpy as np

# path = keras.utils.get_file(
#     'nietzsche.txt',
#     origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
# text = open(path, encoding='utf-8').read().lower()

path ='rnn_short_toji.txt'
f = open(path, encoding='utf-8')
text=f.read()
print('말뭉치 크기(행의 개수):', len(text))

import re
text= re.sub('[^가-힣 ]','',text)
print(set(text))
chars= sorted(list(set(text)))
print(chars)
print('사용 가능한 문자수:',len(chars))
print()

char_index = dict((c,i) for i, c in enumerate(chars))
index_char = dict((i,c) for i, c in enumerate(chars))
print('char_index : ',char_index)
print('index_char : ',index_char)

# 30개 글자로 된 시퀀스를 추출합니다.
maxlen = 30

# 세 글자씩 건너 뛰면서 새로운 시퀀스를 샘플링합니다. 어차피 패턴을 찾는 것이기에 3글자씩 끊어 써도 된다.
step = 1 # 고정이 아님

# 추출한 시퀀스를 담을 리스트
sentences = []

# 타깃(시퀀스 다음 글자)을 담을 리스트
next_chars = []

for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('시퀀스 개수:', len(sentences)) #시퀀스 - 순서가 있는 데이터의 개수

# 말뭉치에서 고유한 글자를 담은 리스트
chars = sorted(list(set(text)))
print('고유한 글자:', len(chars)) #니체의 글자에서 있는
# chars 리스트에 있는 글자와 글자의 인덱스를 매핑한 딕셔너리
char_indices = dict((char, chars.index(char)) for char in chars)


# 글자를 원-핫 인코딩하여 0과 1의 이진 배열로 바꿉니다.
print('벡터화...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
y = np.zeros((len(sentences), len(chars)), dtype=bool) #python의 bool 사용

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1 # x[면, 행, 열]=1
    y[i, char_indices[next_chars[i]]] = 1 # y[행, 열] =1

from keras import layers

model = keras.models.Sequential() #글자 단위이이기에 embedding이 빠졌다.
model.add(layers.LSTM(128, input_shape=(maxlen, len(chars)),activation='tanh'))
model.add(layers.Dense(len(chars), activation='softmax'))
# 글자단위일때는 임베딩을 쓰지 않는다. 유닛의 개수는 정해져 있지 않음

optimizer = keras.optimizers.RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

print(model.summary())


# SOFT MAX 함수를 수식을 이용해 작성하고 있다.
def sample(preds, temperature=1.0): # temperature로 확률분포의 가중치를 조정하고 있음
    # array() : 원본 생성시 복사본은 변경이 안됨, asarray(): 원본 생성시 복사본은 변경이 됨
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature #log : 큰수를 작게 만들고(비율) 복잡한 계산을 단순화
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# variety등 다양한 값을 넣어보는 것 - 결과가 조금씩 나오게 됨

random.seed(42)
start_index = random.randint(0, len(text) - maxlen - 1)

# 60 에포크 동안 모델을 훈련합니다 - 편의상 언제끝날지 모르게에 60정도는 돌려야 하지만 에폭을 줄임 - 
for epoch in range(1, 6): # 편의상 5 에폭동안 모델을 훈련
    print('에포크', epoch)
    # 데이터에서 한 번만 반복해서 모델을 학습합니다
    model.fit(x, y, batch_size=128, epochs=1)

    # 무작위로 시드 텍스트를 선택합니다
    seed_text = text[start_index: start_index + maxlen]
    print('--- 시드 텍스트: "' + seed_text + '"')

    # 여러가지 샘플링 다양성를 시도합니다
    for temperature in [0.2, 0.5,  1.2]:
        print('------ 다양성 확률 값:', temperature)
        generated_text = seed_text
        sys.stdout.write(generated_text)

        # 시드 텍스트에서 시작해서 500개의 글자를 생성합니다
        for i in range(500):
            # 지금까지 생성된 글자를 원-핫 인코딩으로 바꿉니다
            sampled = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = 1.

            # 다음 글자를 샘플링합니다 - 글자단위로
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]

            generated_text += next_char
            generated_text = generated_text[1:]

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

        #학습량이 늘어나며 우리가 더 알아보기 쉬운 글들로 바뀐다.