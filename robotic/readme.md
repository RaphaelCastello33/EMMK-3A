# Setup de ROS
todo cat "" > ~/.bashrc
alias ssh2023 
ROS_USER_URL
source /opt/tab/tab/setup.bash

# Se connecter à ROS
ssh2023 et entrer votre mdp cas

# Commandes Usuelles 

## roscore

__**@brief:**__ roscore will start a master on default node `11311`

### roscore -p
__**@brief:**__ starts a master with a given node
__**@note:**__ I recommand using an alias to automatically use the port you want `alias roscore="roscore -p [PORT]"`
__**@attention:**__ you first need to modify the env variable ROS_MASTER_URL with `export ROS_MASTER_URL=[PORT]` 

## rosnode

### rosnode list

__**@brief:**__ lists active nodes

### rosnode info

__**@brief:**__ shows info about a node

### rosnode cleanup

__**@brief:**__ removes all unreachable nodes 



## rosrun

### 

__**@brief:**__ 


## rossrv

### 

__**@brief:**__ 


## rostopic 

### rostopic pub

__**@brief:**__ publishes to a topic


### rostopic echo

__**@brief:**__ subscribes to a topic

### rostopic list

__**@brief:**__ Shows the list of all topics
