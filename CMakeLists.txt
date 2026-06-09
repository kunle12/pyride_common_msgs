cmake_minimum_required(VERSION 3.20)
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
find_package(builtin_interfaces REQUIRED)
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
  msg/AudioData.msg
  msg/AudioTranscription.msg
  msg/AudioFormat.msg
  msg/WakeWordData.msg
  msg/FaceId.msg
  msg/FaceIdWithImg.msg
  srv/RenameObject.srv
  srv/ImgToFace.srv
  srv/RegisterFace.srv
  srv/CompareFace.srv
  srv/CompareFaceWithImg.srv
  srv/KnownFaces.srv
  srv/UnregisterFace.srv
  action/ObjectEnrolment.action
  action/RecordAudio.action
  action/AudioFilePlay.action
  action/TextToSpeech.action
  DEPENDENCIES
  std_msgs
  sensor_msgs
  geometry_msgs
  builtin_interfaces
)

# Install scripts
install(PROGRAMS
  scripts/pyride_msg_loopback_router.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

ament_package()
