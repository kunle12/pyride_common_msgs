cmake_minimum_required(VERSION 3.5)
project(pyride_common_msgs)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate interfaces using absolute paths
rosidl_generate_interfaces(${PROJECT_NAME}
  msg/NodeStatus.msg
  msg/NodeMessage.msg
  msg/ObjectBound.msg
  msg/TrackedObjectInfo.msg
  msg/TrackedObjectStatusChange.msg
  msg/TrackedObjectUpdate.msg
  msg/AnnotatedView.msg
  srv/RenameObject.srv
  action/ObjectEnrolment.action
  DEPENDENCIES
  std_msgs
  sensor_msgs
  geometry_msgs
  action_msgs
)

# Install scripts
install(PROGRAMS
  scripts/pyride_msg_loopback_router.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
