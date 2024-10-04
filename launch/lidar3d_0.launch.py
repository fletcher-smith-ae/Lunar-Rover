from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    launch_arg_prefix = DeclareLaunchArgument(
        'prefix',
        default_value='/world/warehouse/model/robot/link/base_link/sensor/',
        description='Ignition sensor topic prefix')

    prefix = LaunchConfiguration('prefix')

    # Nodes
    node_lidar3d_0_gz_bridge = Node(
        name='lidar3d_0_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='a200_0000/sensors/',
        output='screen',
        arguments=
            [
                [
                    prefix
                    ,
                    'lidar3d_0/scan/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked'
                    ,
                ]
                ,
            ]
        ,
        remappings=
            [
                (
                    [
                        prefix
                        ,
                        'lidar3d_0/scan/points'
                        ,
                    ]
                    ,
                    'lidar3d_0/points'
                )
                ,
            ]
        ,
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                }
                ,
            ]
        ,
    )

    node_lidar3d_0_static_tf = Node(
        name='lidar3d_0_static_tf',
        executable='static_transform_publisher',
        package='tf2_ros',
        namespace='a200_0000',
        output='screen',
        arguments=
            [
                '--frame-id'
                ,
                'lidar3d_0_link'
                ,
                '--child-frame-id'
                ,
                'a200_0000/robot/base_link/lidar3d_0'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/tf'
                    ,
                    'tf'
                )
                ,
                (
                    '/tf_static'
                    ,
                    'tf_static'
                )
                ,
            ]
        ,
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                }
                ,
            ]
        ,
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_arg_prefix)
    ld.add_action(node_lidar3d_0_gz_bridge)
    ld.add_action(node_lidar3d_0_static_tf)
    return ld
