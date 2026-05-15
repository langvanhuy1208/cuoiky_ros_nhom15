import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_gmapping',
            executable='slam_gmapping',
            name='slam_gmapping',
            output='screen',
            parameters=[{
                'use_sim_time': True,             
                'base_frame': 'base_footprint',   
                'odom_frame': 'odom',             
                'map_frame': 'map',
                'map_update_interval': 1.0,      
                'maxUrange': 10.0,                
                'sigma': 0.05,
                'kernelSize': 1,
                'lstep': 0.05,
                'astep': 0.05,
                'iterations': 5,
                'lsigma': 0.075,
                'ogain': 3.0,
                'lskip': 0,
                'srr': 0.1,
                'srt': 0.2,
                'str': 0.1,
                'stt': 0.2,
                'linearUpdate': 0.1,             
                'angularUpdate': 0.1,             
                'temporalUpdate': -1.0,
                'resampleThreshold': 0.5,
                'particles': 80,                  
                'xmin': -10.0,
                'ymin': -10.0,
                'xmax': 10.0,
                'ymax': 10.0,
                'delta': 0.05                     
            }],
            remappings=[
                ('/scan', '/scan')                
            ]
        )
    ])
