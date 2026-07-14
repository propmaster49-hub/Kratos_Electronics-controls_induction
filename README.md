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




# Week 4
## Approach to Solving the Problem

I first understood the kinematics of a Double Ackermann steering system by deriving the steering geometry manually. I identified the Instantaneous Center of Rotation (ICR) and defined the coordinate axis for each wheel and the system as a whole and lateru used the rover wheelbase and track width to determine the steering angles for the inner and outer wheels. I later implemented the required logic computationally within the specified function inside the given ackermann.py file. Once i verified that the logic was sound and that the rover was behaving a necessary on gazebo i added print functions to print the array [fl, fr, rl, rr].

## Assumptions
The rover follows the physical dimensions specified in the assignment:
- Wheelbase = 0.4 m
- Track Width = 0.6 m
- Wheel Radius = 0.12 m
- The controller assumes ideal wheel-ground contact without wheel slip.


## Challenges Encountered
- Understanding the axos definition for each weel to determine steering angle took a lot of time
- For turning in clockwise and anti-clockwise direction i tried to keep the steering angle same and only change the direction of angular velocity but due to errors while testing in gazebo abandoned that idea


## Testing Methodology

Confirmed that steering and drive command arrays were published to their respective controller topics, by printing out the required array
Controlled the rover in gazebo using teleop_twist_keyboard.
-Straight-line motion
-Left turns
-Right turns
-Forward and reverse motion
-Variable speed commands
-Verified rover behaviour visually in Gazebo and monitored the published steering and drive arrays through terminal output.


## Known Limitations
- The controller assumes ideal Ackermann steering geometry and does not account for wheel slip or terrain interaction.
- No feedback from wheel encoders used
- 
