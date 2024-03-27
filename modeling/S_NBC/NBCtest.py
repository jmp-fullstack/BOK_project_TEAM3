from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd
from itertools import chain

# 파일 경로
dovish_test_path = 'data_list/dovish_count_1.csv'
hawkish_test_path = 'data_list/hawkish_count_1.csv'

# 파일 읽기
do_df = pd.read_csv(dovish_test_path, sep=',')
ha_df = pd.read_csv(hawkish_test_path, sep=',')
dw = do_df['Word'].tolist()
hw = ha_df['Word'].tolist()

unique_tokens = list(set(dw + hw))
word2idx = {t:i for i,t in enumerate(unique_tokens)}
# idx2word = {word2idx[t]:t for t in word2idx}

df = pd.DataFrame(index=word2idx,columns=['P(count)', 'N(count)', 'P(word|P)', 'N(word|N)', 'log(P(word|N))', 'log(N(word|N))'])
# # print(df)
# df['P(count)'] = ha_df['Frequency']
# df['N(count)'] = do_df['Frequency']

for i, token in enumerate(unique_tokens):
    df.at[token, 'P(count)'] = ha_df.loc[ha_df['Word'] == token, 'Frequency'].values[0]
    df.at[token, 'N(count)'] = do_df.loc[do_df['Word'] == token, 'Frequency'].values[0]

print(df)
# X_train, X_test, y_train, y_test = train_test_split(df['document'], df['label'], random_state=0)
# count_vect = CountVectorizer(tokenizer=words)
# X_train_counts = count_vect.fit_transform(X_train)
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# clf = MultinomialNB().fit(X_train_tfidf, y_train)

# X_test_tfidf = tfidf_transformer.transform(count_vect.transform(X_test))
# predicted_probas = clf.predict_proba(X_test_tfidf)

# for idx, doc in enumerate(X_test):
#     probas = predicted_probas[idx]
#     print(f"{doc}\t{probas[0]}\t{probas[1]}\t{np.log(probas[0])}\t{np.log(probas[1])}")