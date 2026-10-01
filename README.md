# ROS Python Motion Services

A Python and ROS robotics coursework project developed during my university studies to explore communication between distributed robot-control components using **topics, services and actions**.

The project contains several ROS nodes intended to coordinate drone/robot motion, execute a square-flight manoeuvre, monitor odometry, record poses and control take-off and landing.

The repository preserves the original coursework implementation and represents an early stage in my development with ROS and distributed robotics software.

---

## Project Overview

Rather than implementing all robot behaviour within a single program, the project separates functionality across several ROS nodes.

The recovered system contains components for:

- Drone take-off
- Velocity-based motion control
- Square trajectory execution
- Distance-based motion
- Odometry monitoring
- Pose recording
- ROS service communication
- ROS action communication
- Action feedback and preemption
- Drone landing
- High-level coordination of multiple ROS components

Conceptually:

```text
                         MAIN PROGRAM
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
      /motion_service                  /dist_motion_service
             |                                 |
             v                                 v
       SquareMotion                     Distance Motion
             |                                 |
             v                                 v
     square_motion_as                         /odom
             |
       +-----+-----+
       |           |
       v           v
   /cmd_vel      /land


                    /rec_pose_as
                         |
                         v
                  Record Odometry
                         |
                         v
                   Return Poses
```

A separate take-off node publishes the command required to begin the flight.

---

## Technologies

- Python
- ROS
- `rospy`
- ROS Topics
- ROS Services
- ROS Actions
- `actionlib`
- `geometry_msgs`
- `nav_msgs`
- Odometry
- Velocity control
- Autonomous robot/drone control

---

## Repository Structure

```text
ros-python-motion-services/
│
├── README.md
├── LICENSE
│
└── src/
    ├── main.py
    ├── motion_service.py
    ├── distance_motion_service.py
    ├── check_distance_action.py
    ├── drone_takeoff.py
    └── square_motion.py
```

---

## ROS Communication Architecture

A central purpose of the coursework was exploring several communication mechanisms provided by ROS.

```text
ROS
│
├── Topics
│   ├── /cmd_vel
│   ├── /odom
│   ├── /takeoff
│   └── /land
│
├── Services
│   ├── /motion_service
│   └── /dist_motion_service
│
└── Actions
    ├── square_motion_as
    └── /rec_pose_as
```

These mechanisms allow different parts of the robotics system to operate as independent processes while exchanging commands, sensor information and execution results.

---

## Main Program

`main.py` acts as a high-level coordinator for several components of the system.

The intended execution sequence is:

```text
START
  |
  v
Wait for /motion_service
  |
  v
Request Motion Behaviour
  |
  v
Wait for /dist_motion_service
  |
  v
Request Distance-Controlled Motion
  |
  v
Connect to /rec_pose_as
  |
  v
Request Pose Recording
  |
  v
Wait for Action Result
  |
  v
Display Recorded Pose
```

The node uses ROS service proxies to communicate with the motion services and an `actionlib.SimpleActionClient` to communicate with the pose-recording action server.

This demonstrates how a higher-level ROS node can coordinate behaviours provided by several independent components.

---

## Motion Service

`motion_service.py` creates the ROS service:

```text
/motion_service
```

using the standard ROS `Empty` service type.

When the service receives a request, its callback creates a `SquareMotion` controller.

Conceptually:

```text
Service Client
      |
      | Request
      v
/motion_service
      |
      v
Service Callback
      |
      v
SquareMotion()
      |
      v
Square Motion Action Server
```

This provides a service-based mechanism for initiating the larger motion behaviour.

---

## Square Motion Controller

`square_motion.py` contains one of the main robot-control behaviours in the project.

The `SquareMotion` class creates a ROS action server:

```text
square_motion_as
```

and uses velocity commands to move the drone through an intended square trajectory.

The controller also manages:

- Take-off
- Forward motion
- Turning
- Action feedback
- Action cancellation/preemption
- Motion stopping
- Landing

---

## Drone Take-Off

Before beginning the square manoeuvre, the controller calls:

```python
drone_takeoff()
```

from the separate `drone_takeoff.py` module.

That node creates a publisher for:

```text
/takeoff
```

and publishes an `Empty` message.

Conceptually:

```text
SquareMotion
     |
     v
drone_takeoff()
     |
     v
 /takeoff
     |
     v
    Drone
```

This provides a simple example of ROS topic-based command communication.

---

## Square Flight Behaviour

Once the drone has taken off, the action goal determines how long it should move along each side of the square.

The controller then repeats a movement-and-turn sequence four times:

```text
Move Forward
     |
     v
Wait sideSeconds
     |
     v
Turn
     |
     v
Wait 1.8 Seconds
     |
     v
Next Side
```

Conceptually, the desired trajectory is:

```text
        2 ───────────> 3
        ^               |
        |               |
        |               v
        1               4
        ^               |
        |               |
        +---------------+
```

Forward movement is produced using a ROS `Twist` command with a linear velocity.

Turning is produced by setting the angular velocity.

The implementation therefore demonstrates basic differential/mobile robot motion using:

```text
geometry_msgs/Twist
```

---

## Velocity Commands

The controller publishes motion commands to:

```text
/cmd_vel
```

using the ROS `Twist` message.

A `Twist` contains:

```text
Twist
│
├── linear
│   ├── x
│   ├── y
│   └── z
│
└── angular
    ├── x
    ├── y
    └── z
```

The project uses `linear.x` for forward movement and `angular.z` for turning.

This provided practical experience with one of the standard command interfaces used throughout ROS mobile-robot systems.

---

## Action Feedback

The square-motion behaviour is implemented as an action rather than simply as a service.

During execution, the controller publishes feedback after each side of the square.

Conceptually:

```text
Action Client
      |
      | Goal
      v
square_motion_as
      |
      +----> Side 1 ----> Feedback
      |
      +----> Side 2 ----> Feedback
      |
      +----> Side 3 ----> Feedback
      |
      +----> Side 4 ----> Feedback
      |
      v
    Result
```

This allows a client to monitor the progress of a longer-running behaviour.

---

## Action Preemption

The square-motion controller also checks whether cancellation has been requested by the action client.

If a preemption request is detected, the action server marks the goal as preempted and stops progressing through the remaining square trajectory.

This demonstrates one of the important advantages of ROS actions over ordinary services:

```text
SERVICE
Request -> Execute -> Response


ACTION
Goal -> Execute
          |
          +--> Feedback
          |
          +--> Can Be Cancelled
          |
          v
        Result
```

---

## Completion and Landing

After successfully completing all four sides, the action server calculates an approximate total execution time from the configured side and turn durations.

The action is then marked as successful.

The controller subsequently:

```text
Complete Square
      |
      v
Return Action Result
      |
      v
Stop Motion
      |
      v
Publish /land
      |
      v
Land Drone
```

The landing command is published several times to increase the likelihood that it is received by the corresponding controller.

---

## Distance Motion Service

`distance_motion_service.py` explores motion based on odometry feedback rather than relying entirely on fixed movement times.

The node interacts with:

```text
/cmd_vel
```

for velocity commands and:

```text
/odom
```

for odometry feedback.

The intended control relationship is:

```text
       Velocity Command
              |
              v
            Robot
              |
              v
            /odom
              |
              v
      Distance Estimate
              |
              v
       Distance >= 8 m?
          /       \
        No         Yes
        |           |
        +--> Move   |
                    v
                   Stop
```

The implementation was intended to continue movement until approximately eight metres had been travelled.

A 60-second time condition is also present to identify motion that takes longer than expected.

---

## Odometry

The project subscribes to ROS odometry information using:

```text
nav_msgs/Odometry
```

Odometry provides estimated robot motion and pose information.

This introduces an important robotics control relationship:

```text
Command
   |
   v
Robot Motion
   |
   v
Measurement
   |
   v
Controller Decision
```

Rather than assuming that issuing a motion command guarantees the required movement, sensor/state feedback can be used to determine what the robot has actually done.

---

## Pose Recording Action

`check_distance_action.py` creates another ROS action server:

```text
/rec_pose_as
```

The intended purpose of this action is to record positions obtained from odometry over a defined period.

The process can be represented as:

```text
Action Client
     |
     | Goal
     v
 /rec_pose_as
     |
     v
Subscribe to Odometry
     |
     v
Record Positions
     |
     v
Wait 20 Seconds
     |
     v
Return Recorded Positions
     |
     v
Action Client
```

The main program then retrieves the action result and attempts to display the final recorded position.

This demonstrates using an action to represent a longer-running data-acquisition operation.

---

## Topics vs Services vs Actions

One of the most useful aspects of this coursework was working with three different ROS communication patterns.

### Topics

Topics provide asynchronous message communication.

Examples within the project include:

```text
/cmd_vel
/odom
/takeoff
/land
```

These are appropriate for continuously generated information or event-based commands.

### Services

Services provide request/response communication.

Examples include:

```text
/motion_service
/dist_motion_service
```

A client requests an operation and receives a response from the corresponding service server.

### Actions

Actions are useful for longer-running operations.

Examples include:

```text
square_motion_as
/rec_pose_as
```

They support concepts such as:

- Goals
- Execution
- Feedback
- Results
- Cancellation/preemption

The three communication models can therefore be viewed as:

```text
TOPIC                 SERVICE                 ACTION

Publish               Request                 Goal
   |                     |                     |
   v                     v                     v
Subscriber             Server              Action Server
                         |                     |
                         v                     +--> Feedback
                      Response                 |
                                               +--> Preemption
                                               |
                                               v
                                             Result
```

---

## System Behaviour

Taken together, the recovered source demonstrates the beginnings of a distributed robotics architecture:

```text
                         ROS SYSTEM
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
     SERVICES              ACTIONS              TOPICS
        |                    |                    |
        |             +------+-------+       +----+----+
        |             |              |       |         |
        v             v              v       v         v
 Motion Control   Square Motion   Pose     Commands   State
                                Recording
        |             |              |       |         |
        +-------------+--------------+-------+---------+
                             |
                             v
                       ROBOT / DRONE
```

This was a significant change from earlier robotics projects where most behaviour existed within a single controller.

---

## Concepts Demonstrated

This project provided practical experience with:

- ROS
- Python robotics development
- ROS nodes
- Publishers
- Subscribers
- Topics
- Services
- Service servers
- Service proxies
- Actions
- Action clients
- Action servers
- Action feedback
- Action preemption
- Odometry
- Velocity commands
- `Twist` messages
- `Odometry` messages
- Robot/drone motion
- Take-off and landing
- Distributed robotics software
- Feedback-based movement
- Inter-node communication

---

## Original Implementation

The files in this repository preserve the original university coursework implementation.

The project was still under development and contains incomplete or inconsistent sections. It is therefore **not presented as a production-ready or currently executable ROS package**.

The source has deliberately not been rewritten to make it appear representative of my current ROS programming practices.

Instead, it is retained as an authentic example of my early practical experience with ROS architecture and robot-control communication.

---

## Known Limitations

The recovered source contains several areas that would require further work before the project could be run as a complete ROS system.

These include:

- Some service definitions and service types are inconsistent between client and server code.
- The distance-motion implementation contains unfinished control logic.
- Some odometry callback and distance-calculation logic requires restructuring.
- The pose-recording action contains overlapping odometry subscription logic.
- The recovered files do not include the complete original ROS package definition.
- The original launch files are not currently preserved.
- The custom message, service and action definition files used by `basics_exam` are not included.
- The square-motion controller uses time-based movement and turning rather than closed-loop pose control.
- Several fixed delays are used during take-off, movement and landing.
- Motion commands do not currently use odometry feedback to correct the square trajectory.

These limitations are intentionally documented rather than hidden or rewritten.

---

## Retrospective

Despite being incomplete, this coursework was valuable because it introduced several concepts that became fundamental to my later robotics work.

### Distributed Robot Software

Earlier robotics projects largely placed sensing, decision-making and control within a single application.

ROS introduced a different architecture:

```text
EARLIER CONTROLLER

Sensors
   |
   v
Control Program
   |
   v
Motors


ROS

              ROS COMMUNICATION GRAPH
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
 Sensor Node      Motion Node      Action Node
       |               |               |
       +---------------+---------------+
                       |
                       v
                     Robot
```

Individual capabilities can be implemented independently and communicate through defined ROS interfaces.

### Interface Consistency

The original implementation contains mismatches between some service clients and servers.

With my current experience, I would define each ROS interface first and treat it as a software contract between components.

For example:

```text
/dist_motion_service

Request
└── target_distance

Response
├── success
└── distance_moved
```

Both the client and service implementation would then use the same custom service definition consistently.

### Closed-Loop Square Motion

The original square controller uses elapsed time to estimate how far the drone has travelled and how far it has rotated.

For example:

```text
Move for N seconds
      |
      v
Turn for 1.8 seconds
```

This is simple but open-loop.

A more robust implementation would use odometry or another pose estimate:

```text
Command Motion
      |
      v
Read Pose
      |
      v
Target Reached?
   /      \
 No        Yes
 |          |
 +--Loop    v
         Next Segment
```

This would allow the controller to compensate for variations in actual vehicle motion.

### Distance Tracking

The original distance-control code experiments with deriving movement from odometry and velocity.

A modern implementation would store the starting position and calculate planar displacement consistently:

```text
distance =
sqrt(
    (x_current - x_start)^2
    +
    (y_current - y_start)^2
)
```

This would provide a clearer measurement of displacement from the starting pose.

### State and Callbacks

ROS callback state would be maintained explicitly as class attributes rather than defining overlapping callback implementations inside other methods.

This would make node behaviour easier to understand, test and debug.

### Non-Blocking Behaviour

The square controller relies heavily on fixed `sleep()` calls.

For a more capable robotics system, I would avoid blocking execution where possible and instead use:

- ROS rates
- Timers
- State machines
- Odometry callbacks
- Action feedback
- Explicit motion states

A state-based square controller could resemble:

```text
TAKEOFF
   |
   v
MOVE_SIDE_1
   |
   v
TURN_1
   |
   v
MOVE_SIDE_2
   |
   v
TURN_2
   |
   v
MOVE_SIDE_3
   |
   v
TURN_3
   |
   v
MOVE_SIDE_4
   |
   v
TURN_4
   |
   v
LAND
```

### Testing Strategy

Today I would test each ROS interface independently before integrating the complete system:

```text
1. Test /takeoff
        |
        v
2. Test /cmd_vel publishing
        |
        v
3. Test /odom subscription
        |
        v
4. Test /land
        |
        v
5. Test square_motion_as
        |
        v
6. Test /motion_service
        |
        v
7. Test distance service
        |
        v
8. Test pose-recording action
        |
        v
9. Integrate main coordinator
```

This would isolate failures and make integration considerably easier.

---

## Portfolio Context

This project represents an important stage in my progression toward robotics and autonomous systems.

My earlier projects primarily focused on individual embedded or simulated controllers:

```text
Arduino
   |
   v
Sensors + Actuators
   |
   v
Webots
   |
   v
Autonomous Robot Controllers
   |
   v
ROS
   |
   v
Distributed Robotics Software
```

Although the original implementation was incomplete, the project introduced concepts that became increasingly important in my later robotics development:

- Breaking a robotics application into separate components
- Designing interfaces between those components
- Publishing actuator commands
- Subscribing to robot-state information
- Using services for request/response behaviour
- Using actions for longer-running robot tasks
- Providing action feedback
- Supporting cancellation
- Using odometry as feedback
- Coordinating multiple robot behaviours

It is retained in this portfolio as an authentic record of that progression rather than being rewritten to appear more complete than it originally was.
