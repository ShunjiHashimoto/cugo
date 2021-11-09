cmake_minimum_required(VERSION 3.0.2)
project(cugo_detection)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(
 INCLUDE_DIRS include
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

find_package(OpenCV REQUIRED)
include_directories(${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})
add_executable(object_detection src/object_detection.cpp)
target_link_libraries(object_detection ${OpenCV_LIBRARIES} ${catkin_LIBRARIES})
