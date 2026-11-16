#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PKG = 'super_evgenij_study_pkg'


def generate_launch_description():
    rviz_config = os.path.join(get_package_share_directory(PKG), 'rviz', 'tf_lab.rviz')

    return LaunchDescription([
        DeclareLaunchArgument('carrot_radius', default_value='1.0',
                              description='Радиус вращения морковки, м'),
        DeclareLaunchArgument('carrot_frequency', default_value='0.3',
                              description='Частота вращения морковки, об/с'),
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Запускать RViz2'),

        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),

        Node(
            package=PKG,
            executable='turtle_carrot_broadcaster',
            output='screen',
            parameters=[{
                'carrot_radius': LaunchConfiguration('carrot_radius'),
                'carrot_frequency': LaunchConfiguration('carrot_frequency'),
            }],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            additional_env={'LIBGL_ALWAYS_SOFTWARE': '1'},
            condition=IfCondition(LaunchConfiguration('rviz')),
        ),
    ])