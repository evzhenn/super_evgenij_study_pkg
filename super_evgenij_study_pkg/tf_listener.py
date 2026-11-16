#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener, TransformException


class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.declare_parameter('target_frame', 'base_link')
        self.declare_parameter('source_frame', 'laser_link')
        self.target = self.get_parameter('target_frame').value
        self.source = self.get_parameter('source_frame').value

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.create_timer(2.0, self.on_timer)

    def on_timer(self):
        try:
            t = self.buffer.lookup_transform(self.target, self.source, Time())
        except TransformException as e:
            self.get_logger().warn(f'Нет трансформации {self.target} → {self.source}: {e}')
            return

        tr = t.transform.translation
        dist = math.sqrt(tr.x ** 2 + tr.y ** 2 + tr.z ** 2)
        self.get_logger().info(
            f'{self.target} → {self.source}: x={tr.x:.2f} y={tr.y:.2f} z={tr.z:.2f}, '
            f'расстояние {dist:.3f} м')


def main():
    rclpy.init()
    node = TFListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
