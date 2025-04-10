class CDataDispatch:
    def __init__(self):
        """初始化分发器"""
        self.subscribers = []  # 存储订阅者（其他类实例）
        return

    def add_subscriber(self, subscriber):
        """
        添加订阅者
        :param subscriber: 订阅者（需实现 process_data 方法）
        """
        if hasattr(subscriber, "process_data") and callable(subscriber.process_data):
            self.subscribers.append(subscriber)
        else:
            print(f"订阅者 {subscriber} 没有实现 process_data 方法，无法添加。")

        return

    def remove_subscriber(self, subscriber):
        """移除订阅者"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

        return

    def dispatch(self, data):
        """
        分发数据给所有订阅者
        :param data: 要分发的数据
        """
        for subscriber in self.subscribers:
            try:
                subscriber.process_data(data)
            except Exception as e:
                print(f"订阅者 {subscriber} 处理数据时出现错误: {e}")
        return
