#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

class DoubleAckermannController(Node):
    def __init__(self):
        super().__init__('double_ackermann_controller')
        
        # Subscribe to teleop/joystick commands
        self.cmd_sub = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_callback, 
            10
        )
        
        # Publisher for the 4 steering hinges (Position in Radians)
        # Order matches YAML: [fl_steer, fr_steer, rl_steer, rr_steer]
        self.steer_pub = self.create_publisher(
            Float64MultiArray, 
            '/steering_controller/commands', 
            10
        )

        # Publisher for the 4 wheel axles (Velocity in Rad/s)
        # Order matches YAML: [fl_drive, fr_drive, rl_drive, rr_drive]
        self.drive_pub = self.create_publisher(
            Float64MultiArray, 
            '/drive_controller/commands', 
            10
        )

        # Rover Physical Constants
        self.wheelbase = 0.4
        self.track_width = 0.6
        self.wheel_radius = 0.12

        self.get_logger().info("Double Ackermann Controller Node Started. Waiting for /cmd_vel...")

    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Initialize outputs
        fl_angle = fr_angle = rl_angle = rr_angle = 0.0
        fl_vel = fr_vel = rl_vel = rr_vel = 0.0

        # -----------------------------
        # Straight motion
        # -----------------------------
        if abs(angular_z) < 1e-6:

            wheel_speed = linear_x / self.wheel_radius

            fl_vel = wheel_speed
            fr_vel = wheel_speed
            rl_vel = wheel_speed
            rr_vel = wheel_speed

        # -----------------------------
        # Turning motion
        # -----------------------------
        else:

            # Turning radius of rover center
            R = linear_x / angular_z

            # Rear wheel turning radii
            rear_inner = max(abs(R) - self.track_width / 2.0, 1e-6)
            rear_outer = abs(R) + self.track_width / 2.0

            # Steering angles
            inner_angle = math.atan(
                self.wheelbase / rear_inner
            )

            outer_angle = math.atan(
                self.wheelbase / rear_outer
            )

            # Left turn
            if angular_z > 0:

                fl_angle = inner_angle
                fr_angle = outer_angle

                rl_angle = -inner_angle
                rr_angle = -outer_angle

            # Right turn
            else:

                fl_angle = -outer_angle
                fr_angle = -inner_angle

                rl_angle = outer_angle
                rr_angle = inner_angle

            # Clamp steering
            fl_angle = max(-1.57, min(1.57, fl_angle))
            fr_angle = max(-1.57, min(1.57, fr_angle))
            rl_angle = max(-1.57, min(1.57, rl_angle))
            rr_angle = max(-1.57, min(1.57, rr_angle))

            # Front wheel turning radii
            front_inner = math.sqrt(
                rear_inner**2 +
                self.wheelbase**2
            )

            front_outer = math.sqrt(
                rear_outer**2 +
                self.wheelbase**2
            )

            # Linear wheel speeds
            front_inner_speed = abs(angular_z) * front_inner
            front_outer_speed = abs(angular_z) * front_outer

            rear_inner_speed = abs(angular_z) * rear_inner
            rear_outer_speed = abs(angular_z) * rear_outer

            # Convert to wheel angular velocity
            front_inner_speed /= self.wheel_radius
            front_outer_speed /= self.wheel_radius

            rear_inner_speed /= self.wheel_radius
            rear_outer_speed /= self.wheel_radius

            # Assign wheel speeds
            if angular_z > 0:

                fl_vel = front_inner_speed
                fr_vel = front_outer_speed

                rl_vel = rear_inner_speed
                rr_vel = rear_outer_speed

            else:

                fl_vel = front_outer_speed
                fr_vel = front_inner_speed

                rl_vel = rear_outer_speed
                rr_vel = rear_inner_speed

            # Reverse motion
            if linear_x < 0:

                fl_vel *= -1
                fr_vel *= -1
                rl_vel *= -1
                rr_vel *= -1

        # Publish steering commands
        steer_msg = Float64MultiArray()
        steer_msg.data = [
            fl_angle,
            fr_angle,
            rl_angle,
            rr_angle
        ]
        self.steer_pub.publish(steer_msg)

        # Publish drive commands
        drive_msg = Float64MultiArray()
        drive_msg.data = [
            fl_vel,
            fr_vel,
            rl_vel,
            rr_vel
        ]
        self.drive_pub.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DoubleAckermannController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
