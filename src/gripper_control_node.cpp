#include <franka_gripper/MoveAction.h>
#include <actionlib/client/simple_action_client.h>

using MoveClient = actionlib::SimpleActionClient<franka_gripper::MoveAction>;

int main(int argc, char **argv)
{
    ros::init(argc, argv, "gripper_control_node");
    ros::NodeHandle nh;

    // 创建一个MoveClient对象
    MoveClient move_client("gripper/move", true);

    // 等待动作服务器启动
    ROS_INFO("Waiting for action server to start.");
    move_client.waitForServer();

    // 创建一个MoveGoal对象，并设置目标宽度
    franka_gripper::MoveGoal goal;
    goal.width = 0.04; // 设置夹爪的目标宽度为0.04m
    goal.speed = 0.1;  // 设置夹爪的移动速度为0.1m/s

    // 发送目标给动作服务器
    ROS_INFO("Sending goal.");
    move_client.sendGoal(goal);

    // 等待动作结果
    bool finished_before_timeout = move_client.waitForResult(ros::Duration(30.0));

    if (finished_before_timeout)
    {
        actionlib::SimpleClientGoalState state = move_client.getState();
        ROS_INFO("Action finished: %s", state.toString().c_str());
    }
    else
    {
        ROS_INFO("Action did not finish before the time out.");
    }

    return 0;
}