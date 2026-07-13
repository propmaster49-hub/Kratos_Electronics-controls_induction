#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float32


class RoverStatusPublisher(Node):
    def __init__(self):
        super().__init__('rover_status_publisher')
        self.battery_publisher = self.create_publisher(Float32, '/battery_level', 10)
        self.rover_status_publisher = self.create_publisher(String, '/rover_mode', 10)
        self.emergency_stop_publisher = self.create_publisher(Bool, '/emergency_stop', 10)
        self.timer = self.create_timer(1.0, self.publish_status)


    def publish_status(self):
        battery_level = Float32()
        battery_level.data = 85.0  # Example battery level
        self.battery_publisher.publish(battery_level)

        rover_mode = String()
        rover_mode.data = "AUTONOMOUS"  # Example rover mode
        self.rover_status_publisher.publish(rover_mode)

        emergency_stop_signal = Bool()
        emergency_stop_signal.data = False  # Example emergency stop signal
        self.emergency_stop_publisher.publish(emergency_stop_signal)


def main(args=None):
    rclpy.init(args=args)

    node = RoverStatusPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()