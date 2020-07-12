import os
import warnings
from gensim.models import doc2vec
from gensim.models.doc2vec import TaggedDocument
import pandas as pd
import jpype

d2v_faqs = doc2vec.Doc2Vec.load(os.path.join('./model/d2v_faqs_size200_min5_epoch20_ebs_science_qna.model'))

# 질문-답변 파일 불러오기
df2 = pd.read_excel('./data/df2_20200705_edited.xlsx')
df2.dropna(axis=0)

qna_num = 0  # 질문답변 번호인 qna_num 초기화

from konlpy.tag import Mecab

mecab = Mecab()
text = u"""이제 구글 코랩에서 Mecab-ko라이브러리 사용이 가능합니다. 읽어주셔서 감사합니다."""
nouns = mecab.nouns(text)
print(nouns)

filter_mecab = ['NNG',  # 보통명사
                'NNP',  # 고유명사
                'SL',  # 외국어
                ]

def tokenize_mecab(doc):
    # jpype.attachThreadToJVM()
    token_doc = ['/'.join(word) for word in mecab.pos(doc)]
    return token_doc

def tokenize_mecab_noun(doc):
    # jpype.attachThreadToJVM()
    token_doc = ['/'.join(word) for word in mecab.pos(doc) if word[1] in filter_mecab]
    return token_doc

index_questions = []

for i in range(len(df2)):  # df2가 0부터 시작
    index_questions.append([tokenize_mecab_noun(df2['질문'][i]), i])  # 명사만 추출

# Doc2Vec에서 사용하는 태그문서형으로 변경
tagged_questions = [TaggedDocument(d, [int(c)]) for d, c in index_questions]

# FAQ 답변
def faq_answer(input):
    # 테스트하는 문장도 같은 전처리를 해준다.
    tokened_test_string = tokenize_mecab_noun(input)

    topn = 1  # 가장 유사한 질문 한 개까지만
    test_vector = d2v_faqs.infer_vector(tokened_test_string)
    result = d2v_faqs.docvecs.most_similar([test_vector], topn=topn)

    for i in range(topn):
        print("유사질문 {}위 | 유사도: {:0.3f} | 문장 번호: {} | {}".format(i + 1, result[i][1], result[i][0], df2['질문'][result[i][0]]))
        #print("\t질문 {} | 문장 번호: {} | {}".format(i + 1, result[i][0], df2['답변'][result[i][0]]))
        #print(len(df2['답변'][result[i][0]]))
        #for j in range(len(df2['답변'][result[i][0]])):
        #    #print(j)
        #    print("\t질문 {} | 답글순서 {} | 문장 번호: {} | {}".format(i + 1, j + 1, result[i][0], df2['답변'][result[i][0]][j]))

    return '유사도: {:0.1f}% 질문: '.format(result[i][1] * 100) + df2['질문'][result[i][0]] + '#####################################답변: ' + df2['답변'][result[i][0]]

print('챗봇 불러오기 완료')
