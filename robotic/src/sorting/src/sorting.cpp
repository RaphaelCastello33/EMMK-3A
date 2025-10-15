/**
 * @author: Raph
 * @date:   10/10/2025
 * @brief:  todo
 */
#include "../include/sorting.hpp"
#include <algorithm> // to sort the string #easierThatWay

Sorting::Sorting(ros::NodeHandle& n_, bool toggleSorting_, const std::string& input_)   // la est passe partout car copiable
: toggleSorting(toggleSorting_), inputMsg(input_) {
    publisherSorted = n_.advertise<std_msgs::String>("sorting", 10);                    // créer un advertiser appelé /sorting
    subscriber = n_.subscribe("hello", 10, &Sorting::subscribeCallback, this);          // se subscribe au topic /hello
    service = n_.advertiseService("ToggleSorting", &Sorting::serviceCallback, this);    // créer un service appelé /ToggleSorting
}

/**
 * @brief returns the sorted input
 */
std::string Sorting::sortMsg(const std::string& msg) {
    std::string s = msg;
    std::sort(s.begin(), s.end());
    return s;
}

void Sorting::publishSortedCallback(){
    std_msgs::String out;
    out.data = (toggleSorting ? sortMsg(this->inputMsg) : this->inputMsg);
    publisherSorted.publish(out);
}


void Sorting::subscribeCallback(const std_msgs::String::ConstPtr& msg){
    this->inputMsg = msg->data;   // on stocke la dernière string reçue
}

bool Sorting::serviceCallback(sorting_msgs::ToggleSorting::Request&, // légal en cpp, il faut qu'il soit là pour match le callback de ros
                              sorting_msgs::ToggleSorting::Response& res) {
    toggleSorting = !toggleSorting;
    res.toggleSort = toggleSorting;
    ROS_INFO("Sorting %s", toggleSorting ? "ON" : "OFF");
    return true;
}
