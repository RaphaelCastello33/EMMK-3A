cmake_minimum_required(VERSION 3.0.2)
project(sorting)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  sorting_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp std_msgs sorting_msgs
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(sorting_node
  src/sorting_node.cpp
  src/sorting.cpp
)

add_executable(hello_node
  src/hello_node.cpp
  src/sorting.cpp   # on peut surement l'enlever
)

target_link_libraries(sorting_node
  ${catkin_LIBRARIES}
)

target_link_libraries(hello_node
  ${catkin_LIBRARIES}
)
