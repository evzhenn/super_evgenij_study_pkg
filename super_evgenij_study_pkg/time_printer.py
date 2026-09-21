#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
import rclpy
from rclpy.node import Node

TZ = timezone(timedelta(hours=3))

class TimePrinter(Node):
    def __init__(self):
        super().__init__('time_printer')
        self.create_timer(5.0, self.print_time)

    def print_time(self):
        now = datetime.now(TZ).strftime('%H:%M:%S')
        self.get_logger().info(f'Текущее время: {now}')

def main(args=None):
    rclpy.init(args=args)
    node = TimePrinter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
