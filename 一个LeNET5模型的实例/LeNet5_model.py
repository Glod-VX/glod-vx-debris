
import tensorflow as tf
from tensorflow.keras import layers, models

def LeNet5():
    model = models.Sequential()

    # 第一层卷积层
    model.add(layers.Conv2D(6, (5, 5), activation='tanh', input_shape=(28, 28, 1)))
    model.add(layers.AveragePooling2D((2, 2)))

    # 第二层卷积层
    model.add(layers.Conv2D(16, (5, 5), activation='tanh'))
    model.add(layers.AveragePooling2D((2, 2)))

    # 第三层卷积层，卷积核改为 (4, 4)
    model.add(layers.Conv2D(120, (4, 4), activation='tanh'))
    model.add(layers.Flatten())

    # 全连接层
    model.add(layers.Dense(84, activation='tanh'))
    model.add(layers.Dense(10, activation='softmax'))  # 10 类（数字）

    # 编译模型
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

