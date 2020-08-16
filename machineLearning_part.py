import pandas as pd
from  sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

df = pd.read_csv('Dataset.csv', encoding='latin-1')             #To encode it in utf-8

df_names = df
df_names.Type.replace({'P':0,'A':1,'L':2,'O': 3},inplace=True)

Xfeatures =df_names['Name']
cv = CountVectorizer()

X = cv.fit_transform(Xfeatures)
y = df_names.Type

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

tree = DecisionTreeClassifier()
tree.fit(X,y)

def MachineLearningAlgo(noun):

    type = ""

    test_name = [noun]

    vector = cv.transform(test_name).toarray()

    if tree.predict(vector) == 0:
        type = "Person"
    elif tree.predict(vector) == 1:
        type = "Animal"
    elif tree.predict(vector) == 2:
        type = "Place"
    elif tree.predict(vector) == 3:
        type = "Object"

    return type

