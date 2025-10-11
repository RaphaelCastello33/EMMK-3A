/**
 * @author: Raph
 * @date:   10/10/2025
 * @brief:  todo
 */

#include "ros/ros.h"
#include "../include/sorting.hpp"
#include <cstdlib>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "sorting");
    ros::NodeHandle n;

    // tri OFF au démarrage (false), message = argv[1]
    Sorting sorter(n, false, "");

    ros::Rate loop_rate(1); 
    while (ros::ok()) {
        // publie en boucle, comme talker
        sorter.publishSortedCallback();
        ros::spinOnce(); // spinOnce car il subscribe a rien
        loop_rate.sleep();
    }
    return 0;
}
