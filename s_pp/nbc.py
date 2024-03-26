import pandas as pd
import numpy as np

dovish_test_path = './data_list/dovish_test.csv'
hawkish_test_path = './data_list/hawkish_test.csv'
dovish_df = pd.read_csv(dovish_test_path,sep=',')
hawkish_df = pd.read_csv(hawkish_test_path,sep=',')

words = [word.split() for word in dovish_df['words'].tolist()]
df = pd.DataFrame(index=[0], columns=['P', 'N', 'Polarity','Intensity','label'])
print(df)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    news_df['words'], news_df['label'], shuffle=True, test_size=0.2)
X_train, y_train


label_mapping = {'비둘기파': 0,'매파':1}
Y_train = [label_mapping[label] for label in news_df['label'].tolist()]


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
clf = MultinomialNB().fit(X_train_counts, y_train)


print(clf.predict(count_vect.transform(["a"])))
print(clf.predict_proba(count_vect.transform(["i_love"])))