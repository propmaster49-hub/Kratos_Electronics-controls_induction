# Week 3

## Approach to Solving the Problem

ROS2 Basics
Post Dual booting i made myself familiar with the interface of terminator and rviz. First i created 1 publisher and 1 subscriber for the battery level to check if it functions properly, then created 2 more objects for operating mode and emergency_stop status respectively. Then for the second question i defined my own message type ROoverStatus as required and replicated my publishers and subscriber topics from  the previous question.


IKFK and Transforms
I first worked out the protocol to calculate Inverse Kinematocs by hand and then proceeded to attempt the question. I however couldn't apply the Matrix and Jacobian form of Inverse Kinematocs formulae and resorted to triginimetric equations. I then tested if my input changed the position of the arm in RViz and it worked.

## Assumptions
- The rover battery percentage is represented using fixed values for demonstration purposes.
- The rover operates in `"AUTONOMOUS"` mode unless specified otherwise.
- The emergency stop remains inactive (`False`) during testing.
- Sensor values are simulated and are not connected to physical hardware.
- The inverse kinematics solution assumes a planar robotic arm with the dimensions specified in the assignment.


## Challenges Encountered

- Understanding the ROS2 publisher–subscriber communication model.
- Learning the differences between standard ROS2 messages and custom message definitions.
- Configuring `CMakeLists.txt` and `package.xml` correctly for Python nodes and custom messages.
- Initially configured the package as a C++ package before converting it correctly to support Python executables.
- Setting up the development environment inside the provided Docker container and verifying communication using ROS2 CLI tools.
- Couldn't implement matrix/jacobian formulation of inverse kinematics
- Intially the arm would update position according to inputs but then instantaneously switch back to initial position


## Testing Methodology

The implementation was verified using the ROS2 command-line interface in terminator.

### Question 1
- The publisher and subscriber were executed simultaneously, and successful message exchange was verified.

### Question 2
- Verified that the custom message publisher and subscriber exchanged all fields of the `RoverStatus` message correctly.

### IKFK
- Tested the inverse kinematics node by publishing joint states and verifying the resulting arm configuration in RViz.


## Known Limitations

- The published rover status values are static and intended only for demonstration.
- No real rover hardware or sensors are connected.
- The inverse kinematics implementation is limited to the arm configuration provided in the assignment, and to only 2 dimensions and 2 links, any addition in joints or spatial dimensions will lead to malfunctioning of the program
- Program needs to be rewritten in order to increase links, in its current form it is not modular
