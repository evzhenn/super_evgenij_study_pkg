#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node

class TimePrinter(Node):
    def __init__(self):
        super().__init__('time_printer')
        self.create_timer(5.0, self.print_time)   # вызывать print_time каждые 5 секунд

    def print_time(self):
        now = time.strftime('%H:%M:%S')
        self.get_logger().info(f'Текущее время: {now}')

def main(args=None):
    rclpy.init(args=args)
    node = TimePrinter()
    rclpy.spin(node)          # держим узел живым, чтобы таймер срабатывал
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
