import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# 生成圆上的数据点
num_points = 1000
theta = np.linspace(0, 2 * np.pi, num_points)
radius1 = 1
radius2 = 2
x1 = radius1 * np.cos(theta)
y1 = radius1 * np.sin(theta)
x2 = radius2 * np.cos(theta)
y2 = radius2 * np.sin(theta)

data = np.column_stack((np.concatenate((x1, x2)), np.concatenate((y1, y2))))

# 划分训练集和测试集
train_size = int(0.8 * num_points)
train_data = data[:train_size]
test_data = data[train_size:]

# 构建模型
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(2,)),
    layers.Dropout(0.5),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(2)
])

model.compile(optimizer=keras.optimizers.Adam(0.001), loss='mse')

test_data_x = radius1 * np.cos(theta) * 0.5
test_data_y = radius1 * np.sin(theta) * 0.5
test_data = np.column_stack((test_data_x, test_data_y))

# 训练模型
history = model.fit(train_data, train_data, epochs=100, verbose=1)

# 进行预测
predictions = model.predict(test_data)

# 可视化结果
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(test_data[:, 0], test_data[:, 1], label='True Data', color='blue')
plt.title('True Data')
plt.subplot(1, 2, 2)
plt.scatter(predictions[:, 0], predictions[:, 1], label='Predicted Data', color='red')
plt.title('Predicted Data')
plt.show()