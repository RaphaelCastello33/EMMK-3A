cmake_minimum_required(VERSION 3.0.2)
project(sorting_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
)

## Déclare les fichiers de service
add_service_files(
  FILES
  ToggleSorting.srv
)

## Génère le code C++ associé
generate_messages(
  DEPENDENCIES
  std_msgs
)

## Déclare le package catkin
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs
)
