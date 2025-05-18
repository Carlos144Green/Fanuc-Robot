#include <moveit/move_group_interface/move_group_interface.h>

//runs with: rosrun cob_test test_random_cobot_node 
int main(int argc,char **argv)
{
    ros::init(argc, argv, "move_group_interface_demo");

    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::MoveGroupInterface group("manipulator");
 
    group.setRandomTarget();
    group.move();


    ros::waitForShutdown();


}
