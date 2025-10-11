# how to use

## terminal 1

`roscore`  

## terminal 2

`rosrun sorting sorting_node`  

## terminal 3

`rostopic echo /sorted`  

## terminal 4

`rosrun sorting hello_node "string"`

## terminal 5

`rosservice call /ToggleSorting`


# what you should see once every command is typed

1. nothing until `rosrun sorting hello_node "string"` <br>
2. then you should see your string being print as is in terminal 3 <br>
3. once you use `rosservice call /ToggleSorting` on another terminal you should see your string being print sorted <br>
