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

    // on attend un court instant que ROS connecte le publisher au master
    ros::Duration(0.5).sleep();

    std_msgs::String msg;
    msg.data = msg_to_send;

    pub.publish(msg);
    ROS_INFO_STREAM("Published once on /hello: " << msg_to_send);

    // on laisse un petit délai pour s'assurer que le message parte bien
    ros::Duration(0.5).sleep();

    return 0;
}
