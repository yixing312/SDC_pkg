#include <ros/ros.h>
#include <std_msgs/String.h>
int main(int argc, char *argv[])
{
    ros::init(argc, argv, "sensor_node");
    // code for setup
    ros::NodeHandle node_1;
    ros::Publisher pub_1 = node_1.advertise<std_msgs::String>("topic_1",10);
    while (ros::ok())
    {
        // code for loop
        std_msgs::String msg;
        msg.data = "some massages";
        pub_1.publish(msg);
    }
    // code for end
    return 0;
}
