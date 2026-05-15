import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'xecuahuy'
    pkg_share = get_package_share_directory(pkg_name)
    

    urdf_file = os.path.join(pkg_share, 'urdf', 'xecuahuy.urdf')
    
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'config.rviz')
    
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()


    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True  
        }]
    )


    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )


    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py'))
    )
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py'))
    )


    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'xecuahuy', '-z', '0.1'],
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

    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        joint_state_publisher_gui,
        spawn_entity,
        rviz2
    ])
