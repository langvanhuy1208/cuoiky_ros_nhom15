from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='hector_slam_node',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'mode': 'mapping'},
                {'map_frame': 'map'},
                {'base_frame': 'base_link'},
                {'odom_frame': 'odom'},
                {'scan_topic': '/scan'},
                {'scan_buffer_size': 100},
                {'map_update_interval': 0.5},
                {'transform_publish_period': 0.02},
                {'lookup_transform_timeout': 1.0},
                {'use_scan_matching': True}
            ]
        )
    ])
