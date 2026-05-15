# cuoiky_ros_nhom15
# Di chuyển về thư mục gốc của workspace
d ~/xecuahuy_ws
colcon build
colcon build --packages-select xecuahuy
source install/setup.bash

# lenh dieu khien
ros2 run xecuahuy teleop_node.py

# lenh chay moi truong turtlebot3
ros2 launch xecuahuy full_system.launch.py 

# lenh goi moi truong nha kho
ros2 launch xecuahuy spawn_huy_warehouse.launch.py

# lenh goi moi truong nha
ros2 launch xecuahuy full_system.launch.py world:=map3.world

# lenh goi map
ros2 launch xecuahuy gmapping_community.launch.py


ros2 launch xecuahuy cartographer.launch.py


ros2 launch xecuahuy hector_slam.launch.py


ros2 launch xecuahuy karto_slam.launch.py


ros2 launch xecuahuy rtabmap_only.launch.py
