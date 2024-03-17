
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os
from launch_ros import parameter_descriptions
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration, Command



def generate_launch_description():

  packageName = "arm_urdf"
  roboName = 'arm_desc.xacro'
  xacroPath = os.path.join(get_package_share_directory(packageName),  'urdf', roboName)


  robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{
      'robot_description': parameter_descriptions.ParameterValue(Command(['xacro',' ', xacroPath]), value_type=str)
    }])

  worldName = "raceway.world"
  worldPath = os.path.join(get_package_share_directory(packageName), "worlds", worldName)
  gazebo = ExecuteProcess(
      cmd=['gazebo', '--verbose',  worldPath ,  '-s', 'libgazebo_ros_init.so', 
      '-s', 'libgazebo_ros_factory.so'],
      output='screen')
  
  
  spawn=Node(
		package="gazebo_ros",
		executable="spawn_entity.py",
		arguments=[
            "-entity", "arm",
			"-topic",  "/robot_description"
        ]
	)
    
  jointStatePub = Node(
		package="joint_state_publisher_gui",
		executable="joint_state_publisher_gui",
	)

  rviz = Node(
      package="rviz2",
      executable="rviz2",
      name="rviz2",
      arguments=['-d', os.path.join(get_package_share_directory(packageName), 'rviz', 'arm_rover_config.rviz')] )
    
  return LaunchDescription({
      robot_state_publisher,
      gazebo,
      rviz,
      # jointStatePub,
      spawn  
    })