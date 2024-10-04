import os
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='rover').find('rover')
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # urdf_file_name = 'sdf/rover.sdf'
    urdf_file_name = 'urdf/rover.urdf'

    print("urdf_file_name : {}".format(urdf_file_name))

    # urdf = os.path.join(pkgPath, 'sdf', 'rover.sdf')
    urdf = os.path.join(pkgPath, 'urdf', 'rover.urdf')
    rvizConfigPath = os.path.join(pkgPath, 'rviz', 'config.rviz')

    package_name='rover'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )
    print("HELLO",get_package_share_directory(package_name),'launch','rsp.launch.py')

    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    # launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )
    
    gazebo = ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')
    
    forward_position_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_controller"],
    )

    forward_velocity_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_velocity_controller"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    rviz = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rvizConfigPath]
    ) 

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        forward_position_controller,
        forward_velocity_controller,
        joint_broad_spawner
        # rviz
        # DeclareLaunchArgument(
        #     'use_sim_time',
        #     default_value='false',
        #     description='Use simulation (Gazebo) clock if true'
        # ),

        # ExecuteProcess(
        #     cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
        #     output='screen'
        # ),

        # Node(
        #     package='robot_state_publisher',
        #     executable='robot_state_publisher',
        #     name='robot_state_publisher',
        #     output='screen',
        #     parameters=[{'use_sim_time': use_sim_time}],
        #     arguments=[urdf]
        # ),

        # Node(
        #     package='joint_state_publisher',
        #     executable='joint_state_publisher',
        #     name='joint_state_publisher',
        #     output='screen',
        #     parameters=[{'use_sim_time': use_sim_time}]
        # ),

        # Node(
        #     package='gazebo_ros',
        #     executable='spawn_entity.py',
        #     name='urdf_spawner',
        #     output='screen',
        #     arguments=["-topic", "/robot_description", "-entity", "rover", "-z", "1.0"]
        # ),

        # # Start the controller manager
        # Node(
        #     package='controller_manager',
        #     executable='ros2_control_node',
        #     name='controller_manager',
        #     output='screen'
        # ),

        # # Start the joint state controller
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     name='joint_state_controller',
        #     output='screen',
        #     arguments=['joint_state_controller']
        # ),

        # # Position controllers for the wheels
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     name='back_left_wheel_position_controller',
        #     output='screen',
        #     arguments=['back_left_wheel_position_controller']
        # ),
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     name='back_right_wheel_position_controller',
        #     output='screen',
        #     arguments=['back_right_wheel_position_controller']
        # ),
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     name='front_left_wheel_position_controller',
        #     output='screen',
        #     arguments=['front_left_wheel_position_controller']
        # ),
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     name='front_right_wheel_position_controller',
        #     output='screen',
        #     arguments=['front_right_wheel_position_controller']
        # ),
        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     arguments=['forward_position_controller']
        # ),

        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     arguments=['forward_velocity_controller']
        # ),

        # Node(
        #     package='controller_manager',
        #     executable='spawner',
        #     arguments=['joint_broad']
        # ),

        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     arguments=['-d', rvizConfigPath]
        # )    
    ])