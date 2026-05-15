import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'xecuahuy'
    pkg_share = get_package_share_directory(pkg_name)

    urdf_file = os.path.join(pkg_share, 'urdf', 'xecuahuy.urdf')
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'config.rviz')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')


    world_name_arg = DeclareLaunchArgument(
        'world',
        default_value='map1.world',
        description='Ten file world trong thu muc worlds'
    )

    world_path = PathJoinSubstitution([
        pkg_share,
        'worlds',
        LaunchConfiguration('world')
    ])
    # --------------------------------

    with open(urdf_file, 'r') as infp:
        robot_desc_raw = infp.read()

    robot_desc = robot_desc_raw.replace('$(find xecuahuy)', pkg_share)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }]
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={
            'world': world_path  
        }.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py')
        )
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'xecuahuy',
            '-z', '0.1'
        ],
        output='screen'
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}]
    )

    load_jsb = TimerAction(
        period=3.0,
        actions=[Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"])]
    )

    load_diff_drive = TimerAction(
        period=5.0,
        actions=[Node(package="controller_manager", executable="spawner", arguments=["diff_drive_controller"])]
    )

    load_arm = TimerAction(
        period=7.0,
        actions=[Node(package="controller_manager", executable="spawner", arguments=["arm_controller"])]
    )

    balancing_script_path = os.path.join(pkg_share, 'scripts', 'balancing_node.py')

    load_balancing_node = TimerAction(
        period=9.0,
        actions=[
            Node(
                package=pkg_name,
                executable='/usr/bin/python3',
                arguments=[balancing_script_path],
                output='screen',
                parameters=[{'use_sim_time': True}]
            )
        ]
    )

    return LaunchDescription([
        world_name_arg,      
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        spawn_entity,
        rviz2,
        load_jsb,
        load_diff_drive,
        load_arm,
        load_balancing_node
    ])
