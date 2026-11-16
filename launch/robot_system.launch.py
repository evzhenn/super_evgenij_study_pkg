#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PKG = 'super_evgenij_study_pkg'

MODES = {
    'fast': {'publish_frequency': 20.0, 'overflow_threshold': 50, 'topic_name': '/even_numbers_fast'},
    'slow': {'publish_frequency': 5.0, 'overflow_threshold': 150, 'topic_name': '/even_numbers_slow'},
}


def launch_setup(context):
    def arg(name):
        return LaunchConfiguration(name).perform(context)

    params_file = os.path.join(get_package_share_directory(PKG), 'params', 'robot_params.yaml')

    mode = arg('mode')
    if mode in MODES:
        overrides = dict(MODES[mode])
    elif mode == 'normal':
        overrides = {}
    else:
        raise RuntimeError(f"Неизвестный mode '{mode}'. Допустимо: normal, fast, slow")

    if arg('publish_frequency'):
        overrides['publish_frequency'] = float(arg('publish_frequency'))
    if arg('overflow_threshold'):
        overrides['overflow_threshold'] = int(arg('overflow_threshold'))
    if arg('topic_name'):
        overrides['topic_name'] = arg('topic_name')
    overrides['overflow_topic'] = arg('overflow_topic')

    publisher = Node(
        package=PKG,
        executable='even_number_publisher',
        name=arg('publisher_name'),
        output='screen',
        parameters=[params_file, overrides],
    )

    listener = Node(
        package=PKG,
        executable='overflow_listener',
        name=arg('listener_name'),
        output='screen',
        parameters=[{'overflow_topic': arg('overflow_topic')}],
    )

    return [publisher, listener]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='normal',
                              description='Режим: normal (из YAML), fast или slow'),
        DeclareLaunchArgument('publish_frequency', default_value='',
                              description='Частота публикации, Гц (пусто = из YAML или mode)'),
        DeclareLaunchArgument('overflow_threshold', default_value='',
                              description='Порог переполнения (пусто = из YAML или mode)'),
        DeclareLaunchArgument('topic_name', default_value='',
                              description='Топик чётных чисел (пусто = из mode или even_numbers)'),
        DeclareLaunchArgument('overflow_topic', default_value='overflow',
                              description='Топик переполнения'),
        DeclareLaunchArgument('publisher_name', default_value='even_pub',
                              description='Имя узла-публикатора'),
        DeclareLaunchArgument('listener_name', default_value='overflow_listener',
                              description='Имя узла-слушателя'),
        OpaqueFunction(function=launch_setup),
    ])
