#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    slam = LaunchConfiguration("slam", default="True")
    map_yaml = LaunchConfiguration("map", default="")

    custom_rviz_config_path = os.path.join(
        get_package_share_directory("rby1_nav2"), # 본인의 패키지 이름 확인
        "rviz",
        "nav2_restaurant.rviz"
    )

    nav2_params = LaunchConfiguration(
        "params_file",
        default=os.path.join(
            get_package_share_directory("rby1_nav2"), "config", "param_restaurant.yaml"
        ),
    )

    livox_launch_file_dir = os.path.join(
        get_package_share_directory("livox_ros_driver2"), "launch_ROS2"
    )
    livox_to_laserscan_launch_file_dir = os.path.join(
        get_package_share_directory("livox_to_laserscan"), "launch"
    )
    rby1_nav2_launch_file_dir = os.path.join(
        get_package_share_directory("rby1_nav2"), "launch"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            DeclareLaunchArgument(
                "slam",
                default_value="True",
                description="Run SLAM (mapless navigation)",
            ),
            DeclareLaunchArgument(
                "map",
                default_value="",
                description="Map yaml file (unused when slam is true)",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=nav2_params,
                description="Full path to Nav2 param file to load",
            ),

            # Navigation restaurant (Nav2 + SLAM)
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [rby1_nav2_launch_file_dir, "/navigation_explore.launch.py"]
                ),
                launch_arguments={
                    "slam": slam,
                    "map": map_yaml,
                    "use_sim_time": use_sim_time,
                    "params_file": nav2_params,
                }.items(),
            ),


            # Livox MID360 driver
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [livox_launch_file_dir, "/rviz_MID360_launch.py"]
                ),
            ),

            # PointCloud -> LaserScan
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [livox_to_laserscan_launch_file_dir, "/livox_to_laserscan.launch.py"]
                ),
            ),

            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', custom_rviz_config_path], # -d 옵션으로 경로 직접 주입
                parameters=[{'use_sim_time': use_sim_time}],
                output='screen'
            ),

            # Explore Lite (direct node to avoid duplicate DeclareLaunchArgument)
            # Node(
            #     package="explore_lite",
            #     name="explore_node",
            #     executable="explore",
            #     parameters=[
            #         os.path.join(
            #             get_package_share_directory("explore_lite"),
            #             "config",
            #             "params.yaml",
            #         ),
            #         {"use_sim_time": use_sim_time},
            #     ],
            #     output="screen",
            # ),
        ]
    )
