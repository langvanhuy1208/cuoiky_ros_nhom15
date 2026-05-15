import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='karto_slam_node', 
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'odom_frame': 'odom'},
                {'base_frame': 'base_link'}, 
                {'map_frame': 'map'},
                {'scan_topic': '/scan'},
                {'mode': 'mapping'}
            ]
        )
    ])
