#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float32


class RoverStatusSubscriber(Node):
    def __init__(self):
        super().__init__('rover_status_subscriber')

        self.battery_subscription = self.create_subscription(
            Float32,
            '/battery_level',
            self.battery_callback,
            10
        )

        self.rover_mode_subscription = self.create_subscription(
            String,
            '/rover_mode',
            self.rover_mode_callback,
            10
        )

        self.emergency_stop_subscription = self.create_subscription(
            Bool,
            '/emergency_stop',
            self.emergency_stop_callback,
            10
        )

    def battery_callback(self, msg):
        self.get_logger().info(f'Battery Level: {msg.data}')

    def rover_mode_callback(self, msg):
        self.get_logger().info(f'Rover Mode: {msg.data}')

    def emergency_stop_callback(self, msg):
        self.get_logger().info(f'Emergency Stop: {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    node = RoverStatusSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()