
import os
import sys

# from ament_index_python.packages import get_package_share_directory

import launch
import launch_ros
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription



def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='rover').find('rover')
    # Set paths for URDF and RViz configuration files
    urdfModelPath = os.path.join(pkgPath, 'urdf', 'rover.urdf')  # Ensure this file exists
    rvizConfigPath = os.path.join(pkgPath, 'rviz', 'config.rviz')  # Ensure this file exists

    print(urdfModelPath)
    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()
    
    params = {'robot_description': robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package = 'robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
        arguments=[urdfModelPath]
    )

    # joint_state_publisher_node = launch_ros.actions.Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     parameters=[params],
    #     arguments=[urdfModelPath]
    # )
    
    # joint_state_publisher_gui_node = launch_ros.actions.Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     arguments=[urdfModelPath],
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),

        robot_state_publisher_node
    ])