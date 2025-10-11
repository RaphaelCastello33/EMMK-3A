# Setup de ROS
modifier le fichier ~/.bashrc et y ajouter les lignes ci-dessous **A LA FIN** du fichier:
```
source /opt/ros/noetic/setup.bash      # pour pouvoir roscore
source ~/catkin_ws/devel/setup.bash    # pour pouvoir run les pkg ajoutés
export ROS_USER_URL=http://localhost:[le port que t'as shotgun]    # pour que roscore utilise le bon port
alias ssh2023="ssh -X ros2023.zut.ipb.fr"  # pour se connecter au serveur ros de l'école (inutile si t'es sur VM)
alias roscore="roscore -p [le port que t'as shotgun]"  # pour ne plus jamais avoir a écrire tt la ligne a chaque fois (tu peux utiliser roscore mtn)
```


# Se connecter à ROS
`ssh2023` puis entrer votre mdp cas

# Create a package
```
cd ~/catkin_ws/src
catkin_create_pkg [pkg_name] std_msgs rospy roscpp

```

# Commandes Usuelles <br>

## roscore<br>
**@brief:** roscore will start a master node on default port `11311`<br>

### roscore -p<br>
**@brief:** starts a master with a given port<br>
**@note:** I recommand using an alias to automatically use the port you want `alias roscore="roscore -p [PORT]"`<br>
**@attention:** you first need to modify the env variable ROS_MASTER_URL with `export ROS_MASTER_URL=[PORT]` <br>

## rosnode

### list

**@brief:** lists active nodes

### info [node]

**@brief:** shows info about [node] (Publish, Subscription and Services)

### cleanup

**@brief:** removes all unreachable nodes 



## rosrun [pkg] [node's_binary]

**@brief:** runs a pkg's node


## rossrv

### show [srv_type]
**@brief:** shows the args for a given [srv_type]<br>
**@see:** `rosservice type [service]` to get the [srv_type]<br>


## rostopic 

### rostopic pub [options] [topic] [message] [args]

**@brief:** publishes [args] to a topic<br>
**@note:** use rostopic echo first to see the [args] format<br>
**@example:** `rostopic pub -r 1 /turtle1/cmd_vel geometry_msgs/Twist '[1.0, 0.0, 0.0]' '[0.0, 0.0, 2.0]' # ca doit faire un cercle ou un truc du genre`  <br>

#### [options list]:
> -1: only once<br>
> -r [Hz]: recursive at [Hz] frequency<br>

### rostopic list

**@brief:** Shows the list of all topics

## rosservice

### list
**@brief:** lists all active services, you can use rosservice list [node] to list only the [node]'s services

### call [service] [args]
**@brief:** call the service with the provided args<br>
**@see:** `rosservice type [service] | rossrv show` to get the [args]<br>

### type [service]
**@brief:** print [service] [srv_type] (its info so that we know what are its args)
 

### find 
**@brief:** find services by service type

### uri
**@brief:** print service ROSRPC uri


## rosparam

### list

**@brief:** list parameter names

### set
**@brief:** set parameter

### get
**@brief:** get parameter

### dump [yaml]
**@brief:** writes all params (rosparam get /) into [yaml]

### load [src] [node]
**@brief:** get params from [src] and dump it to [node]


# Package.xml

## build_depend

**@brief:** équivalent a un `#include` en c/cpp pour qu'on puisse `catkin_make`

## build_export_depend

**@brief:** l'inverse d'un `#include`, ici c'est pour dire que ton package va etre `#include` par d'autres packages

## exec_depend

**@brief:** il faut les memes que pour build_depend sinon on peut pas `rosrun` 

## exemple minimaliste d'un package.xml

```xml
<?xml version="1.0"?>
<package format="2">
  <name>sorting_msgs</name>
  <version>0.0.1</version>
  <description>Service definitions for sorting</description>

  <maintainer email="rouaf@todo.todo">rouaf</maintainer>
  <license>BSD</license>

  <buildtool_depend>catkin</buildtool_depend>

  <build_depend>pkg1</build_depend>
  <build_depend>pkg2</build_depend>

  <!-- will be used by another package -->
  <build_export_depend>pkg2</build_export_depend>


  <exec_depend>pkg1</exec_depend>
  <exec_depend>pkg2</exec_depend>
</package> 
```

# CMakeLists.txt

## catkin_package

**@brief:** on y mets toutes nos dépendances : `CATKIN_DEPENDS [dep1] [dep2] [dep3]...`

## find_package

**@brief:** on y mets toutes nos dépendances : `catkin REQUIRED COMPONENTS [dep1] [dep2] [dep3]...`

## include_directories

**@brief:** toujours le même (normalement) : 

```Makefile
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)
```

## add_executable

**@brief:** le nom du [binaire] suivi des fichier .cpp<br>
**@note:**  rosrun [pkg] [binaire] <br>
**@example:** <br>

```Makefile
add_executable(sorting_node # binaire
    src/sorting_node.cpp    # fichier cpp 1
    src/sorting.cpp         # fichier cpp 2
)
```

## target_link

**@brief:** le nom du [binaire] suivi de `${catkin_LIBRARIES}`<br>
**@note:**  rosrun [pkg] [binaire] <br>
**@example:** <br>

```Makefile
target_link_libraries(sorting_node
  ${catkin_LIBRARIES}
)
```

## add_dependencies

**@brief:** le nom du [binaire] suivi de `${catkin_EXPORTED_TARGETS}`<br>
**@note:**  rosrun [pkg] [binaire] <br>
**@example:** <br>

```Makefile
add_dependencies(sorting_node
  ${catkin_EXPORTED_TARGETS}
)
```
