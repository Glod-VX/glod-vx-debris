import tensorflow as tf
from LeNet5_model import LeNet5
from data_preparation import load_and_prepare_data

def main():
    # 设置分布式训练策略
    strategy = tf.distribute.MirroredStrategy()
    print(f'Number of devices: {strategy.num_replicas_in_sync}')

    with strategy.scope():
        # 初始化模型
        model = LeNet5()

        # 加载数据
        (x_train, y_train), (x_test, y_test) = load_and_prepare_data()

        # 训练模型
        model.fit(x_train, y_train, batch_size=64, epochs=10, validation_data=(x_test, y_test))

        # 评估模型
        test_loss, test_acc = model.evaluate(x_test, y_test)
        print(f'Test accuracy: {test_acc:.4f}')

if __name__ == '__main__':
    main()
