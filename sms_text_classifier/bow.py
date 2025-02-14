import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# 读取数据
train_file_path = "./sms_text_classifier/train-data.tsv"
test_file_path = "./sms_text_classifier/valid-data.tsv"
train_data = pd.read_csv(train_file_path, sep='\t', header=None)
test_data = pd.read_csv(test_file_path, sep='\t', header=None)

# 数据预处理
train_data.columns = ['label', 'message']
test_data.columns = ['label', 'message']
train_data['label'] = train_data['label'].map({'ham': 0, 'spam': 1})
test_data['label'] = test_data['label'].map({'ham': 0, 'spam': 1})

# 提取特征
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_data['message'])
X_test = vectorizer.transform(test_data['message'])

y_train = train_data['label']
y_test = test_data['label']

# 训练模型
model = MultinomialNB()
model.fit(X_train, y_train)

# 预测并评估
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 定义预测函数
def predict_message(pred_text):
    pred_vector = vectorizer.transform([pred_text])
    pred_label = model.predict(pred_vector)
    label_mapping = {0: 'ham', 1:'spam'}
    return label_mapping[pred_label[0]]

# 测试预测函数
test_messages = ["how are you doing today",
                 "sale today! to stop texts call 98912460324",
                 "i dont want to go. can we try it a different day? available sat",
                 "our new mobile video service is live. just install on your phone to start watching.",
                 "you have won £1000 cash! call to claim your prize.",
                 "i'll bring it tomorrow. don't forget the milk.",
                 "wow, is your arm alright. that happened to me one time too"]

for msg in test_messages:
    prediction = predict_message(msg)
    print(f"Message: {msg}, Prediction: {prediction}")