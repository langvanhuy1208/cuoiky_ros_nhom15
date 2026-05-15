import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'xecuahuy'
    pkg_share = get_package_share_directory(pkg_name)
    
    urdf_file = os.path.join(pkg_share, 'urdf', 'xecuahuy.urdf')
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'config.rviz')
    aws_warehouse_share = get_package_share_directory('aws_robomaker_small_warehouse_world')
    

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read().replace('$(find xecuahuy)', pkg_share)



    env_model_path = SetEnvironmentVariable('GAZEBO_MODEL_PATH', os.path.join(pkg_share, '..'))
    env_resource_path = SetEnvironmentVariable('GAZEBO_RESOURCE_PATH', '/usr/share/gazebo-11')
    env_ogre = SetEnvironmentVariable('OGRE_RTT_MODE', 'Copy')


    world_file_path = os.path.join(aws_warehouse_share, 'worlds', 'no_roof_small_warehouse.world')

    gazebo_map = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(aws_warehouse_share, 'launch', 'small_warehouse.launch.py')
        ),
        launch_arguments={'world': world_file_path}.items() # Ép nó load file world mình đã sửa
    )


    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )


    spawn = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=['-topic', 'robot_description', '-entity', 'xecuahuy', '-x', '0.0', '-y', '0.0', '-z', '0.5'],
                output='screen'
            )
        ]
    )


    load_jsb = TimerAction(
        period=15.0, 
        actions=[Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"])]
    )

    load_diff = TimerAction(
        period=20.0, 
        actions=[Node(package="controller_manager", executable="spawner", arguments=["diff_drive_controller"])]
    )

    # 5. RViz (Chạy sau cùng)
    rviz = TimerAction(
        period=30.0,
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                arguments=['-d', rviz_config_path],
                parameters=[{'use_sim_time': True}]
            )
        ]
    )

    return LaunchDescription([
        env_model_path,
        env_resource_path,
        env_ogre,
        gazebo_map,
        rsp, 
        spawn, 
        load_jsb, 
        load_diff,
        rviz
    ])
