#include "ros/ros.h"
#include <std_msgs/String.h>
#include <string>

int main(int argc, char** argv) {
    ros::init(argc, argv, "hello_node");
    ros::NodeHandle nh;

    std::string msg_to_send = "hello";
    if (argc > 1)
        msg_to_send = argv[1];

    ros::Publisher pub = nh.advertise<std_msgs::String>("hello", 10);

    std_msgs::String msg;
    msg.data = msg_to_send;

    pub.publish(msg);
    return 0;
}
