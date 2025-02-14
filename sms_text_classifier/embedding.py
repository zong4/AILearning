import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 加载预训练的 BERT 模型和分词器
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
# 给 BERT 模型使用一个不同的变量名，比如 bert_model
bert_model = AutoModel.from_pretrained('bert-base-uncased')

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

# 定义函数计算文本的 CLS 嵌入，使用 bert_model
def get_cls_embedding(text):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = bert_model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embedding

# 计算训练集和测试集的嵌入
train_embeddings = [get_cls_embedding(text).flatten() for text in train_data['message']]
test_embeddings = [get_cls_embedding(text).flatten() for text in test_data['message']]
print(test_embeddings)

# 划分训练集和验证集
X_train = train_embeddings
y_train = train_data['label']
X_test = test_embeddings
y_test = test_data['label']

# 训练逻辑回归模型，使用一个不同的变量名，比如 logreg_model
logreg_model = LogisticRegression()
logreg_model.fit(X_train, y_train)

# 预测并评估
y_pred = logreg_model.predict(X_test)
print(classification_report(y_test, y_pred))

def predict_message(pred_text):
    pred_embedding = get_cls_embedding(pred_text).flatten()
    pred_label = logreg_model.predict([pred_embedding])
    label_mapping = {0: 'ham', 1:'spam'}
    return label_mapping[pred_label[0]]

print(predict_message("how are you doing today?"))
print(predict_message("sale today! to stop texts call 98912460324"))
print(predict_message("i dont want to go. can we try it a different day? available sat"))
print(predict_message("our new mobile video service is live. just install on your phone to start watching."))
print(predict_message("you have won £1000 cash! call to claim your prize."))
print(predict_message("i'll bring it tomorrow. don't forget the milk."))
print(predict_message("wow, is your arm alright. that happened to me one time too"))

# Run this cell to test your function and model. Do not modify contents.
test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]