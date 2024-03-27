import pandas as pd
import numpy as np

dovish_test_path = './data_list/dovish_test.csv'
hawkish_test_path = './data_list/hawkish_test.csv'
dovish_df = pd.read_csv(dovish_test_path,sep=',')
hawkish_df = pd.read_csv(hawkish_test_path,sep=',')

words = [word.split() for word in dovish_df['words'].tolist()]
df = pd.DataFrame(index=[0], columns=['P', 'N', 'P(word|P)','N(word|N)','log(P(word|N))','log(N(word|N))'])



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

def mytokenizer(x):
    return x.split()

X_train, X_test, y_train, y_test = train_test_split(df['document'], df['label'], random_state=0)
count_vect = CountVectorizer(tokenizer=mytokenizer)
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

X_test_tfidf = tfidf_transformer.transform(count_vect.transform(X_test))
predicted_probas = clf.predict_proba(X_test_tfidf)

for idx, doc in enumerate(X_test):
    probas = predicted_probas[idx]
    print(f"{doc}\t{probas[0]}\t{probas[1]}\t{np.log(probas[0])}\t{np.log(probas[1])}")