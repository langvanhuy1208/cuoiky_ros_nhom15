import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    database_path = os.path.expanduser('~/rtabmap_xecuahuy_3d.db')

    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        arguments=['--delete_db_on_start'],
        parameters=[{
            'use_sim_time': True,
            'frame_id': 'base_footprint',
            'odom_frame_id': 'odom',
            'map_frame_id': 'map',

            'subscribe_depth': True,
            'subscribe_scan': True,

            'approx_sync': True,
            'approx_sync_max_interval': 0.1,


            'database_path': database_path,




            'Grid/3D': 'true',
            'Grid/Sensor': '1',        
            'Grid/RayTracing': 'true',
            'Grid/CellSize': '0.05',
            'Grid/RangeMax': '4.0',


            'Reg/Strategy': '1',
            'Reg/Force3DoF': 'true',


            'RGBD/AngularUpdate': '0.1',
            'RGBD/LinearUpdate': '0.1',




            'Mem/RehearsalSimilarity': '0.45',
            'RGBD/ProximityBySpace': 'true',
            'RGBD/NeighborLinkRefining': 'true',
            'Vis/MinInliers': '15',




            'Cloud/VoxelSize': '0.05',
            'Cloud/NoiseFilteringRadius': '0.1',
            'Cloud/NoiseFilteringMinNeighbors': '5'
        }],
        remappings=[

            ('rgb/image', '/depth_camera/image_raw'),


            ('rgb/camera_info', '/depth_camera/camera_info'),


            ('depth/image', '/depth_camera/depth/image_raw'),


            ('scan', '/scan'),


            ('odom', '/diff_drive_controller/odom'),
        ]
    )

    return LaunchDescription([
        rtabmap_node
    ])
