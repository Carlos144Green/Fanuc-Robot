#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>
#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "move_group_interface_tutorial");
    ros::NodeHandle nh;
    ros::AsyncSpinner spinner(1);
    spinner.start();

    sleep(2.0);

    moveit::planning_interface::MoveGroupInterface group("manipulator");
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

    ros::Publisher display_publisher = nh.advertise<moveit_msgs::DisplayTrajectory>("/move_group/display_planned_path", 1, true);
    moveit_msgs::DisplayTrajectory display_trajectory;


    ROS_INFO("Planning frame: %s", group.getPlanningFrame().c_str());
    ROS_INFO("End Effector Link: %s", group.getEndEffectorLink().c_str());



    group.setNumPlanningAttempts(50);
    group.setPlanningTime(50.0);
    group.clearPoseTargets();

    // Target position
    geometry_msgs::Pose target_pose1;

    target_pose1.orientation.x = 0.7807314;
    target_pose1.orientation.y = -0.21829;
    target_pose1.orientation.z = -0.4355324;
    target_pose1.orientation.w = 0.3913048;

    target_pose1.position.x = 0.4;
    target_pose1.position.y = 0.0;
    target_pose1.position.z = 0.3;

    //If I uncomment the line below, it now works with the link 6 being the tcp. If I replace link_6 with "tool0" it returns the same error.
    //group.setEndEffectorLink("link_6");
    group.setPoseTarget(target_pose1);

    // visualize the planning
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    moveit::planning_interface::MoveItErrorCode success = group.plan(my_plan);

    // move the group arm
    group.move();
    ros::shutdown();

    return 0;

}
