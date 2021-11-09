cmake_minimum_required(VERSION 3.0.2)
project(cugo_teleop)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

 generate_messages(
   DEPENDENCIES
   std_msgs
 )

catkin_package(
  LIBRARIES cugo_teleop
  CATKIN_DEPENDS roscpp rospy std_msgs
  DEPENDS system_lib
)

