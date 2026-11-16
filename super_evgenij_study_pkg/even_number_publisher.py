#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')

        self.declare_parameter('publish_frequency', 10.0)
        self.declare_parameter('overflow_threshold', 100)
        self.declare_parameter('topic_name', 'even_numbers')
        self.declare_parameter('overflow_topic', 'overflow')

        freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        topic = self.get_parameter('topic_name').value
        overflow_topic = self.get_parameter('overflow_topic').value

        self.even_pub = self.create_publisher(Int32, topic, 10)
        self.overflow_pub = self.create_publisher(Int32, overflow_topic, 10)
        self.create_timer(1.0 / freq, self.timer_callback)
        self.count = 0

        self.get_logger().info(
            f'Старт: {freq} Гц, порог {self.threshold}, топики {topic} и {overflow_topic}')

    def timer_callback(self):
        if self.count >= self.threshold:
            overflow_msg = Int32()
            overflow_msg.data = self.count
            self.overflow_pub.publish(overflow_msg)
            self.get_logger().warn(f'Переполнение: {self.count}, сброс на 0')
            self.count = 0

        msg = Int32()
        msg.data = self.count
        self.even_pub.publish(msg)
        self.get_logger().info(f'{self.count}')
        self.count += 2

def main():
    rclpy.init()
    node = EvenNumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
