#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


class TurtleCarrotBroadcaster(Node):
    def __init__(self):
        super().__init__('turtle_carrot_broadcaster')
        self.declare_parameter('turtlename', 'turtle1')
        self.declare_parameter('carrot_radius', 1.0)      # амплитуда, м
        self.declare_parameter('carrot_frequency', 0.5)   # оборотов в секунду

        self.turtle = self.get_parameter('turtlename').value
        self.radius = self.get_parameter('carrot_radius').value
        self.omega = 2 * math.pi * self.get_parameter('carrot_frequency').value

        self.br = TransformBroadcaster(self)
        self.create_subscription(Pose, f'/{self.turtle}/pose', self.pose_callback, 10)
        self.start = self.get_clock().now()
        self.create_timer(0.05, self.carrot_callback)     # 20 Гц

        self.get_logger().info(
            f'world → {self.turtle} → carrot1, радиус {self.radius} м, '
            f'{self.get_parameter("carrot_frequency").value} об/с')

    def pose_callback(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtle

        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        # поворот вокруг оси Z на угол theta -> кватернион
        t.transform.rotation.z = math.sin(msg.theta / 2)
        t.transform.rotation.w = math.cos(msg.theta / 2)

        self.br.sendTransform(t)

    def carrot_callback(self):
        now = self.get_clock().now()
        angle = self.omega * (now - self.start).nanoseconds / 1e9

        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = self.turtle
        t.child_frame_id = 'carrot1'

        t.transform.translation.x = self.radius * math.cos(angle)
        t.transform.translation.y = self.radius * math.sin(angle)
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0

        self.br.sendTransform(t)


def main():
    rclpy.init()
    node = TurtleCarrotBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
