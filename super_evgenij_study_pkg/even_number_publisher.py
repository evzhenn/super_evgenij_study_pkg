#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        self.even_pub = self.create_publisher(Int32, 'even_numbers', 10)
        self.overflow_pub = self.create_publisher(Int32, 'overflow', 10)
        self.create_timer(0.1, self.timer_callback)   # 10 Гц
        self.count = 0

    def timer_callback(self):
        if self.count >= 100:
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
        rclpy.shutdown()

if __name__ == '__main__':
    main()
