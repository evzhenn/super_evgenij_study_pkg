from setuptools import find_packages, setup

package_name = 'super_evgenij_study_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'time_printer = super_evgenij_study_pkg.time_printer:main',
            'even_number_publisher = super_evgenij_study_pkg.even_number_publisher:main',
            'overflow_listener = super_evgenij_study_pkg.overflow_listener:main',
        ],
    },


)
