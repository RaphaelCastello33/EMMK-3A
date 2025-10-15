#pragma once
#include "ros/ros.h"
#include <std_msgs/String.h>
#include <sorting_msgs/ToggleSorting.h>
#include <string>

class Sorting {
private:
    bool toggleSorting;             // état du tri (on/off)
    std::string inputMsg;           // message à trier
    ros::Subscriber subscriber;     // Subscribed  to /hello
    ros::Publisher publisherSorted; // publie le message trié dans /sorted
    ros::ServiceServer service;     // service ToggleSorting

public:
    // constructeur
    Sorting(ros::NodeHandle& n_, bool toggleSorting_, const std::string& input_);

    // méthode de tri (statique)
    static std::string sortMsg(const std::string& msg);

    // Subscribers
    void subscribeCallback(const std_msgs::String::ConstPtr& msg);

    // Publishers
    void publishSortedCallback();

    // Services Handlers
    bool serviceCallback(sorting_msgs::ToggleSorting::Request&, sorting_msgs::ToggleSorting::Response& res);
};
